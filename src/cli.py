#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
命令行接口模块
"""

import asyncio
from typing import List, Dict, Any


class CLI:
    """命令行接口类"""
    
    def __init__(self, model_client, config):
        """初始化命令行接口"""
        self.model_client = model_client
        self.config = config
        self.history = []
    
    def print_header(self):
        """打印头部信息"""
        print("=" * 50)
        print(f"{self.config.app_name}（Octopus）- AI智能体执行框架 {self.config.version}")
        print("=" * 50)
        print("输入 'exit' 或 'quit' 退出")
        print("输入 'help' 查看帮助信息")
        print("=" * 50)
        print()
    
    def print_help(self):
        """打印帮助信息"""
        print("可用命令:")
        print("  help - 显示帮助信息")
        print("  exit - 退出程序")
        print("  quit - 退出程序")
        print()
    
    def add_to_history(self, role: str, content: str):
        """添加到聊天历史"""
        self.history.append({"role": role, "content": content})
        # 保持历史记录在最大限制内
        if len(self.history) > self.config.max_history:
            self.history = self.history[-self.config.max_history:]
    
    async def run(self):
        """运行命令行交互"""
        self.print_header()
        
        try:
            while True:
                # 获取用户输入
                user_input = input("用户> ")
                
                # 处理命令
                if user_input.lower() in ['exit', 'quit']:
                    print("正在退出...")
                    break
                elif user_input.lower() == 'help':
                    self.print_help()
                    continue
                
                # 添加用户输入到历史
                self.add_to_history("user", user_input)
                
                # 显示思考中信息
                print("八爪鱼正在思考...")
                print()
                
                # 生成响应
                print("八爪鱼>", end=" ")
                response_content = ""
                
                # 使用流式输出
                async for chunk in self.model_client.generate(user_input, streaming=True):
                    print(chunk, end="", flush=True)
                    response_content += chunk
                
                print()
                print()
                
                # 添加响应到历史
                self.add_to_history("assistant", response_content)
                
        except KeyboardInterrupt:
            print("\n正在退出...")
        finally:
            # 关闭模型客户端
            await self.model_client.close()
