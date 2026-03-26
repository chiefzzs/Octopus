#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
八爪鱼（Octopus）- AI智能体执行框架
主程序入口
"""

import asyncio
import os
import sys
from typing import List, Dict, Any

from config import Config
from model_client import ModelClient
from cli import CLI


def main():
    """主函数"""
    # 初始化配置
    config = Config()
    
    # 初始化模型客户端
    model_client = ModelClient(config)
    
    # 初始化命令行接口
    cli = CLI(model_client, config)
    
    # 运行命令行交互
    asyncio.run(cli.run())


if __name__ == "__main__":
    main()
