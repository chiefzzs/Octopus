#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
消息格式转换模块
"""

from typing import Dict, Any

from common.utils.logger import get_logger


class MessageFormatter:
    """消息格式转换类"""
    
    def __init__(self):
        """初始化消息格式转换器"""
        self.logger = get_logger(__name__)
    
    def format_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """格式化消息
        
        Args:
            message: 原始消息
            
        Returns:
            格式化后的消息
        """
        try:
            # 标准化消息格式
            formatted_message = {
                "id": message.get("id", ""),
                "type": message.get("type", "text"),
                "content": message.get("content", ""),
                "channel": message.get("channel", "unknown"),
                "user_id": message.get("user_id", ""),
                "timestamp": message.get("timestamp", ""),
                "metadata": message.get("metadata", {})
            }
            
            return formatted_message
        except Exception as e:
            self.logger.error(f"格式化消息失败: {e}")
            return message
    
    def format_response(self, response: Dict[str, Any], channel: str) -> Dict[str, Any]:
        """格式化响应
        
        Args:
            response: 原始响应
            channel: 渠道类型
            
        Returns:
            格式化后的响应
        """
        try:
            # 根据渠道类型格式化响应
            if channel == "wechat":
                # 微信格式
                return {
                    "msgtype": "text",
                    "text": {
                        "content": response.get("content", "")
                    }
                }
            elif channel == "dingtalk":
                # 钉钉格式
                return {
                    "msgtype": "text",
                    "text": {
                        "content": response.get("content", "")
                    }
                }
            elif channel == "feishu":
                # 飞书格式
                return {
                    "content": response.get("content", "")
                }
            else:
                # 默认格式
                return response
        except Exception as e:
            self.logger.error(f"格式化响应失败: {e}")
            return response
