#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置管理模块
"""

import os
from typing import Dict, Any


class Config:
    """配置管理类"""
    
    def __init__(self):
        """初始化配置"""
        # 模型配置
        self.model_name = os.environ.get('MODEL_NAME')
        self.api_key = os.environ.get('API_KEY')
        self.api_url = os.environ.get('API_URL')
        
        # 应用配置
        self.app_name = "八爪鱼"
        self.version = "v0.1.0"
        self.debug = os.environ.get('DEBUG', 'False').lower() == 'true'
        
        # 聊天历史配置
        self.max_history = 10
    
    def get_model_config(self) -> Dict[str, Any]:
        """获取模型配置"""
        return {
            'model_name': self.model_name,
            'api_key': self.api_key,
            'api_url': self.api_url
        }
    
    def get_app_config(self) -> Dict[str, Any]:
        """获取应用配置"""
        return {
            'app_name': self.app_name,
            'version': self.version,
            'debug': self.debug,
            'max_history': self.max_history
        }
