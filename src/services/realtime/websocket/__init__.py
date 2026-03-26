#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WebSocket管理模块
"""

from typing import Dict, Any
from fastapi import WebSocket

from common.utils.logger import get_logger


class WebSocketManager:
    """WebSocket管理类"""
    
    def __init__(self):
        """初始化WebSocket管理器"""
        self.logger = get_logger(__name__)
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket):
        """连接WebSocket
        
        Args:
            websocket: WebSocket连接
        """
        await websocket.accept()
        # 生成连接ID
        connection_id = str(id(websocket))
        self.active_connections[connection_id] = websocket
        self.logger.info(f"WebSocket连接建立: {connection_id}")
        
        # 发送连接成功消息
        await websocket.send_json({
            "type": "connection",
            "status": "connected",
            "connection_id": connection_id
        })
    
    def disconnect(self, websocket: WebSocket):
        """断开WebSocket
        
        Args:
            websocket: WebSocket连接
        """
        connection_id = str(id(websocket))
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
            self.logger.info(f"WebSocket连接断开: {connection_id}")
    
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """发送个人消息
        
        Args:
            message: 消息数据
            websocket: WebSocket连接
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            self.logger.error(f"发送个人消息失败: {e}")
    
    async def broadcast(self, message: Dict[str, Any]):
        """广播消息
        
        Args:
            message: 消息数据
        """
        for connection in self.active_connections.values():
            try:
                await connection.send_json(message)
            except Exception as e:
                self.logger.error(f"广播消息失败: {e}")
