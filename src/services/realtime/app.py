#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
实时输出服务入口
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from common.utils.logger import get_logger
from services.realtime.websocket import WebSocketManager
from services.realtime.streaming import StreamingManager
from services.realtime.broker import MessageBroker


class RealtimeService:
    """实时输出服务类"""
    
    def __init__(self):
        """初始化实时输出服务"""
        self.logger = get_logger(__name__)
        self.app = FastAPI(title="八爪鱼实时输出服务", version="0.2.0")
        self.websocket_manager = WebSocketManager()
        self.streaming_manager = StreamingManager()
        self.message_broker = MessageBroker()
        
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
        # WebSocket路由
        @self.app.websocket("/ws/realtime")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket端点"""
            await self.websocket_manager.connect(websocket)
            try:
                while True:
                    data = await websocket.receive_json()
                    await self.message_broker.process_message(data)
            except WebSocketDisconnect:
                self.websocket_manager.disconnect(websocket)
        
        # 健康检查
        @self.app.get("/health")
        async def health_check():
            """健康检查"""
            return {"status": "healthy"}
        
        # 发送消息路由
        @self.app.post("/api/realtime/send")
        async def send_message(message: dict):
            """发送实时消息"""
            return await self.message_broker.send_message(message)
        
        # 广播消息路由
        @self.app.post("/api/realtime/broadcast")
        async def broadcast_message(message: dict):
            """广播实时消息"""
            return await self.message_broker.broadcast_message(message)
        
        # 流式API路由
        @self.app.post("/api/realtime/stream")
        async def stream_message(message: dict):
            """流式消息处理"""
            return self.streaming_manager.create_stream(message)
    
    def run(self, host="0.0.0.0", port=8004):
        """运行服务"""
        self.logger.info(f"实时输出服务启动，监听 {host}:{port}")
        uvicorn.run(self.app, host=host, port=port)


if __name__ == "__main__":
    service = RealtimeService()
    service.run()
