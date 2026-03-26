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
            return await self.gateway.process_message(message)
        
        # WebSocket路由
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket端点"""
            await self.websocket_manager.connect(websocket)
            try:
                while True:
                    data = await websocket.receive_json()
                    await self.gateway.process_websocket_message(websocket, data)
            except WebSocketDisconnect:
                self.websocket_manager.disconnect(websocket)
        
        # 流式API路由
        @self.app.post("/api/access/stream")
        async def stream_message(message: dict):
            """流式消息处理"""
            return self.streaming_api.process_stream(message)
    
    def run(self, host="0.0.0.0", port=8000):
        """运行服务"""
        self.logger.info(f"接入服务启动，监听 {host}:{port}")
        uvicorn.run(self.app, host=host, port=port)


if __name__ == "__main__":
    service = AccessService()
    service.run()
