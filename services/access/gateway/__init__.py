#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
接入网关模块
"""

from typing import Dict, Any, Optional

from common.utils.logger import get_logger
from services.access.format import MessageFormatter
from services.control.realtime import RealtimeOutputManager


class AccessGateway:
    """接入网关类"""
    
    def __init__(self):
        """初始化接入网关"""
        self.logger = get_logger(__name__)
        self.formatter = MessageFormatter()
        self.realtime_manager = RealtimeOutputManager()
    
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """处理HTTP消息
        
        Args:
            message: 消息数据
            
        Returns:
            处理结果
        """
        try:
            # 格式化消息
            formatted_message = self.formatter.format_message(message)
            
            # 处理消息（这里简化处理，实际需要调用控制服务）
            result = {
                "status": "success",
                "message": "消息处理成功",
                "data": formatted_message
            }
            
            return result
        except Exception as e:
            self.logger.error(f"处理消息失败: {e}")
            return {
                "status": "error",
                "message": f"处理消息失败: {str(e)}"
            }
    
    async def process_websocket_message(self, websocket, message: Dict[str, Any]):
        """处理WebSocket消息
        
        Args:
            websocket: WebSocket连接
            message: 消息数据
        """
        try:
            # 格式化消息
            formatted_message = self.formatter.format_message(message)
            
            # 处理消息
            result = {
                "status": "success",
                "message": "消息处理成功",
                "data": formatted_message
            }
            
            # 发送实时响应
            await websocket.send_json(result)
        except Exception as e:
            self.logger.error(f"处理WebSocket消息失败: {e}")
            await websocket.send_json({
                "status": "error",
                "message": f"处理消息失败: {str(e)}"
            })
