#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试配置文件
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 测试配置
class TestConfig:
    """测试配置类"""
    
    # 服务配置
    ACCESS_SERVICE_URL = "http://localhost:8000"
    CONTROL_SERVICE_URL = "http://localhost:8001"
    REALTIME_SERVICE_URL = "http://localhost:8002"
    EXECUTION_SERVICE_URL = "http://localhost:8003"
    CAPABILITY_SERVICE_URL = "http://localhost:8004"
    
    # WebSocket配置
    ACCESS_WS_URL = "ws://localhost:8000/ws"
    REALTIME_WS_URL = "ws://localhost:8002/ws/realtime"
    EXECUTION_WS_URL = "ws://localhost:8003/ws/execution"
    CAPABILITY_WS_URL = "ws://localhost:8004/ws/capability"
    
    # 测试超时配置
    REQUEST_TIMEOUT = 30
    WS_TIMEOUT = 10
    
    # 测试数据
    TEST_USER = {
        "username": "test_user",
        "password": "test_password",
        "email": "test@example.com"
    }
    
    TEST_MESSAGE = {
        "type": "text",
        "content": "This is a test message"
    }
    
    # 日志配置
    LOG_LEVEL = "DEBUG"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 测试报告配置
    REPORT_DIR = "test_reports"
    REPORT_FILE = "test_report.html"
    
    # 并发测试配置
    CONCURRENT_REQUESTS = 10
    CONCURRENT_USERS = 5
