#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
控制服务入口
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from common.utils.logger import get_logger
from services.control.auth import AuthManager
from services.control.router import RouterManager
from services.control.session import SessionManager
from services.control.realtime import RealtimeOutputManager


class ControlService:
    """控制服务类"""
    
    def __init__(self):
        """初始化控制服务"""
        self.logger = get_logger(__name__)
        self.app = FastAPI(title="八爪鱼控制服务", version="0.2.0")
        self.auth_manager = AuthManager()
        self.router_manager = RouterManager()
        self.session_manager = SessionManager()
        self.realtime_manager = RealtimeOutputManager()
        
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
        
        # 认证路由
        @self.app.post("/api/auth/register")
        async def register(user_data: dict):
            """用户注册"""
            return await self.auth_manager.register(user_data)
        
        @self.app.post("/api/auth/login")
        async def login(credentials: dict):
            """用户登录"""
            return await self.auth_manager.login(credentials)
        
        @self.app.post("/api/auth/logout")
        async def logout(token: str):
            """用户登出"""
            return await self.auth_manager.logout(token)
        
        @self.app.post("/api/auth/check_permission")
        async def check_permission(user_data: dict):
            """检查用户权限"""
            return await self.auth_manager.check_permission(user_data)
        
        # 会话管理路由
        @self.app.post("/api/session/create")
        async def create_session(session_data: dict):
            """创建会话"""
            user_id = session_data.get("user_id")
            if not user_id:
                return {"status": "error", "message": "user_id is required"}
            return await self.session_manager.create_session(user_id)
        
        @self.app.get("/api/session/{session_id}")
        async def get_session(session_id: str):
            """获取会话"""
            return await self.session_manager.get_session(session_id)
        
        @self.app.post("/api/session/update")
        async def update_session(session_data: dict):
            """更新会话"""
            session_id = session_data.get("session_id")
            if not session_id:
                return {"status": "error", "message": "session_id is required"}
            return await self.session_manager.update_session(session_id, session_data)
        
        # 路由管理路由
        @self.app.post("/api/router/route")
        async def route_message(message: dict):
            """路由消息"""
            return await self.router_manager.route_message(message)
        
        # 消息处理路由
        @self.app.post("/api/control/process")
        async def process_message(message: dict):
            """处理用户消息"""
            return await self._process_message(message)
        
        # 实时输出管理路由
        @self.app.post("/api/realtime/output")
        async def send_realtime_message(message: dict):
            """发送实时消息"""
            return await self.realtime_manager.send_message(message)
    
    async def _process_message(self, message: dict):
        """处理用户消息，调用执行服务"""
        try:
            import aiohttp
            content = message.get("message", "")
            self.logger.info(f"处理用户消息: {content}")
            
            # 调用执行服务
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://localhost:8002/api/execution/execute",
                    json={"user_input": content, "session_id": "default"},
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "status": "success",
                            "result": result
                        }
                    else:
                        return {
                            "status": "error",
                            "message": f"执行服务返回错误: {response.status}"
                        }
        except Exception as e:
            self.logger.error(f"处理消息失败: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def run(self, host="0.0.0.0", port=8001):
        """运行服务"""
        self.logger.info(f"控制服务启动，监听 {host}:{port}")
        uvicorn.run(self.app, host=host, port=port)


if __name__ == "__main__":
    service = ControlService()
    service.run()
