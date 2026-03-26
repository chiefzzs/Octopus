#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
流式管理模块
"""

from typing import Dict, Any, AsyncGenerator

from fastapi.responses import StreamingResponse

from common.utils.logger import get_logger


class StreamingManager:
    """流式管理类"""
    
    def __init__(self):
        """初始化流式管理器"""
        self.logger = get_logger(__name__)
    
    def create_stream(self, message: Dict[str, Any]) -> StreamingResponse:
        """创建流式响应
        
        Args:
            message: 消息数据
            
        Returns:
            流式响应
        """
        async def stream_response():
            """流式响应生成器"""
            import asyncio
            
            # 发送开始消息
            yield b"data: {\"type\": \"start\", \"message\": \"Start processing\"}\n\n"
            await asyncio.sleep(0.5)
            
            # 发送中间消息
            yield b"data: {\"type\": \"processing\", \"message\": \"Processing...\"}\n\n"
            await asyncio.sleep(1)
            
            # 发送模型输出
            for i, char in enumerate("This is the real-time output of the large model..."):
                yield f"data: {{\"type\": \"model_output\", \"content\": \"{char}\"}}\n\n".encode('utf-8')
                await asyncio.sleep(0.1)
            
            # 发送结束消息
            yield b"data: {\"type\": \"end\", \"message\": \"Processing complete\"}\n\n"
            await asyncio.sleep(0.5)
            
            # 发送完成标志
            yield b"data: [DONE]\n\n"
        
        return StreamingResponse(
            stream_response(),
            media_type="text/event-stream"
        )
