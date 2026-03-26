#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
模型客户端模块
"""

import asyncio
import json
from typing import Dict, Any, AsyncGenerator, Optional

import aiohttp


class ModelClient:
    """模型客户端类"""
    
    def __init__(self, config):
        """初始化模型客户端"""
        self.config = config
        self.model_config = config.get_model_config()
        self.session = None
    
    async def __aenter__(self):
        """进入上下文管理器"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器"""
        if self.session:
            await self.session.close()
    
    async def _ensure_session(self):
        """确保会话存在"""
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def generate(self, prompt: str, streaming: bool = False) -> AsyncGenerator[str, None]:
        """生成文本
        
        Args:
            prompt: 提示文本
            streaming: 是否流式输出
            
        Returns:
            生成的文本
        """
        await self._ensure_session()
        
        # 构建请求数据
        data = {
            "model": self.model_config['model_name'],
            "messages": [
                {"role": "system", "content": "你是八爪鱼，一个智能助手。请以友好、专业的方式回答用户问题。"},
                {"role": "user", "content": prompt}
            ],
            "stream": streaming
        }
        
        # 构建请求头
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.model_config['api_key']}"
        }
        
        # 发送请求
        async with self.session.post(
            f"{self.model_config['api_url']}/chat/completions",
            json=data,
            headers=headers
        ) as response:
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"API请求失败: {error_text}")
            
            if streaming:
                # 流式输出
                async for chunk in response.content:
                    if chunk:
                        chunk_str = chunk.decode('utf-8')
                        for line in chunk_str.split('\n'):
                            line = line.strip()
                            if line.startswith('data: '):
                                data_str = line[6:]
                                if data_str == '[DONE]':
                                    break
                                try:
                                    data_json = json.loads(data_str)
                                    if 'choices' in data_json and data_json['choices']:
                                        delta = data_json['choices'][0].get('delta', {})
                                        content = delta.get('content', '')
                                        if content:
                                            yield content
                                except json.JSONDecodeError:
                                    pass
            else:
                # 非流式输出
                response_data = await response.json()
                if 'choices' in response_data and response_data['choices']:
                    content = response_data['choices'][0].get('message', {}).get('content', '')
                    yield content
    
    async def close(self):
        """关闭会话"""
        if self.session:
            await self.session.close()
