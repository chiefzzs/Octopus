#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
接入服务入口
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

from common.utils.logger import get_logger
from services.access.gateway import AccessGateway
from services.access.streaming import StreamingAPI
from services.realtime.websocket import WebSocketManager


class AccessService:
    """接入服务类"""
    
    def __init__(self):
        """初始化接入服务"""
        self.logger = get_logger(__name__)
        self.app = FastAPI(title="八爪鱼接入服务", version="0.2.0")
        self.gateway = AccessGateway()
        self.streaming_api = StreamingAPI()
        self.websocket_manager = WebSocketManager()
        
        # 配置CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # 注册路由
        self._register_routes()
    
    def _register_routes(self):
        """注册路由"""
        # 健康检查
        @self.app.get("/health")
        async def health_check():
            """健康检查"""
            return {"status": "healthy"}
        
        # HTTP路由
        @self.app.post("/api/access/message")
        async def receive_message(message: dict):
            """接收消息"""
            response = await self.gateway.process_message(message)
            # 模拟响应
            if not response:
                response = {"message": "已收到您的消息，正在处理中..."}
            return response
        
        # WebSocket路由
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket端点"""
            try:
                await websocket.accept()
                try:
                    while True:
                        data = await websocket.receive_json()
                        await self._process_websocket_message(websocket, data)
                except WebSocketDisconnect:
                    self.logger.info("WebSocket连接断开")
                except Exception as e:
                    self.logger.error(f"WebSocket错误: {e}")
            except Exception as e:
                self.logger.error(f"WebSocket初始化错误: {e}")
        
        # 流式API路由
        @self.app.post("/api/access/stream")
        async def stream_message(message: dict):
            """流式消息处理"""
            return self.streaming_api.process_stream(message)
        
        # Web静态文件服务 - 最后注册作为兜底
        web_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
        if os.path.exists(web_dir):
            @self.app.get("/")
            async def root():
                """根路径返回index.html"""
                return FileResponse(os.path.join(web_dir, "index.html"))
            
            @self.app.get("/css/{filename:path}")
            async def serve_css(filename: str):
                """提供CSS文件"""
                return FileResponse(os.path.join(web_dir, "css", filename))
            
            @self.app.get("/js/{filename:path}")
            async def serve_js(filename: str):
                """提供JS文件"""
                return FileResponse(os.path.join(web_dir, "js", filename))
            
            @self.app.get("/{filename}")
            async def serve_root_files(filename: str):
                """提供根目录文件"""
                file_path = os.path.join(web_dir, filename)
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    return FileResponse(file_path)
                return FileResponse(os.path.join(web_dir, "index.html"))
    
    async def _process_websocket_message(self, websocket: WebSocket, data: dict):
        """处理WebSocket消息"""
        try:
            msg_type = data.get("type", "message")
            if msg_type == "message":
                content = data.get("content", "")
                self.logger.info(f"收到用户消息: {content}")
                
                # 发送正在输入的状态
                await websocket.send_json({"type": "typing"})
                
                try:
                    # 调用控制服务处理请求
                    import aiohttp
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            "http://localhost:8001/api/control/process",
                            json={"message": content},
                            timeout=aiohttp.ClientTimeout(total=60)
                        ) as response:
                            if response.status == 200:
                                result = await response.json()
                                self.logger.info(f"控制服务返回: {result}")
                                
                                # 提取执行结果
                                exec_result = result.get("result", {})
                                response_content = self._format_response(exec_result)
                            else:
                                response_content = f"控制服务返回错误: {response.status}"
                except Exception as e:
                    self.logger.error(f"调用控制服务失败: {e}")
                    response_content = f"抱歉，处理您的请求时出现错误: {str(e)}"
                
                # 发送响应
                await websocket.send_json({
                    "type": "message",
                    "content": response_content
                })
        except Exception as e:
            self.logger.error(f"处理WebSocket消息失败: {e}")
    
    def _format_response(self, exec_result: dict) -> str:
        """格式化执行结果为用户友好的响应
        
        Args:
            exec_result: 执行服务返回的结果
            
        Returns:
            格式化的响应文本
        """
        if not isinstance(exec_result, dict):
            return str(exec_result) if exec_result else "处理完成"
        
        parts = []
        
        # 提取意图信息
        intent_info = exec_result.get("intent", {})
        if intent_info and isinstance(intent_info, dict):
            intent_type = intent_info.get("intent", "")
            confidence = intent_info.get("confidence", 0)
            if intent_type:
                parts.append(f"**意图识别**: {intent_type} (置信度: {confidence:.0%})")
        
        # 提取任务列表
        tasks = exec_result.get("tasks", [])
        if tasks:
            parts.append(f"\n**任务规划**: 共 {len(tasks)} 个任务")
            for i, task in enumerate(tasks, 1):
                task_desc = task.get("description", f"任务{i}")
                parts.append(f"  {i}. {task_desc}")
        
        # 提取任务结果
        result = exec_result.get("result", {})
        if isinstance(result, dict):
            # 提取最终答案
            final_answer = result.get("final_answer")
            if final_answer:
                parts.append(f"\n**最终答案**:\n{final_answer}")
            
            # 提取任务结果列表
            results = result.get("results", [])
            if results:
                parts.append("\n**执行详情**:")
                for i, r in enumerate(results, 1):
                    task_desc = r.get("description", f"任务{i}")
                    status = r.get("status", "未知")
                    answer = r.get("final_answer", "")
                    parts.append(f"\n{i}. {task_desc}")
                    parts.append(f"   状态: {status}")
                    if answer:
                        parts.append(f"   结果: {answer}")
            
            # 如果没有详细结果，显示整个result
            if not results and not final_answer:
                status = result.get("status", "")
                if status:
                    parts.append(f"\n**状态**: {status}")
        else:
            parts.append(f"\n**结果**: {str(result) if result else '处理完成'}")
        
        return "\n".join(parts) if parts else "处理完成"
    
    def run(self, host="0.0.0.0", port=8000):
        """运行服务"""
        self.logger.info(f"接入服务启动，监听 {host}:{port}")
        self.logger.info(f"Web界面可通过 http://localhost:{port} 访问")
        uvicorn.run(self.app, host=host, port=port)


if __name__ == "__main__":
    service = AccessService()
    service.run()
