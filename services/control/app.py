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
        @self.app.post("/api/control/auth/login")
        async def login(credentials: dict):
            """用户登录"""
            return await self.auth_manager.login(credentials)
        
        @self.app.post("/api/control/auth/logout")
        async def logout(token: str):
            """用户登出"""
            return await self.auth_manager.logout(token)
        
        # 会话管理路由
        @self.app.post("/api/control/session/create")
        async def create_session(user_id: str):
            """创建会话"""
            return await self.session_manager.create_session(user_id)
        
        @self.app.get("/api/control/session/{session_id}")
        async def get_session(session_id: str):
            """获取会话"""
            return await self.session_manager.get_session(session_id)
        
        # 路由管理路由
        @self.app.post("/api/control/route")
        async def route_message(message: dict):
            """路由消息"""
            return await self.router_manager.route_message(message)
        
        # 实时输出管理路由
        @self.app.post("/api/control/realtime/send")
        async def send_realtime_message(message: dict):
            """发送实时消息"""
            return await self.realtime_manager.send_message(message)
    
    def run(self, host="0.0.0.0", port=8001):
        """运行服务"""
        self.logger.info(f"控制服务启动，监听 {host}:{port}")
        uvicorn.run(self.app, host=host, port=port)


if __name__ == "__main__":
    service = ControlService()
    service.run()
