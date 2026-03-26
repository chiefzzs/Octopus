#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试工具类
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import asyncio
import json
import time
from typing import Dict, Any, List
import aiohttp
import websockets

from tests.config import TestConfig


class TestHelper:
    """测试辅助类"""
    
    def __init__(self):
        """初始化测试辅助类"""
        self.session = None
        self.ws_connections = []
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
        for ws in self.ws_connections:
            await ws.close()
    
    async def get(self, url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """发送GET请求
        
        Args:
            url: 请求URL
            params: 请求参数
            
        Returns:
            响应数据
        """
        async with self.session.get(url, params=params, timeout=TestConfig.REQUEST_TIMEOUT) as response:
            return await response.json()
    
    async def post(self, url: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """发送POST请求
        
        Args:
            url: 请求URL
            data: 请求数据
            
        Returns:
            响应数据
        """
        async with self.session.post(url, json=data, timeout=TestConfig.REQUEST_TIMEOUT) as response:
            return await response.json()
    
    async def stream_post(self, url: str, data: Dict[str, Any] = None) -> List[str]:
        """发送流式POST请求
        
        Args:
            url: 请求URL
            data: 请求数据
            
        Returns:
            流式响应数据列表
        """
        results = []
        async with self.session.post(url, json=data, timeout=TestConfig.REQUEST_TIMEOUT) as response:
            async for line in response.content:
                if line:
                    results.append(line.decode('utf-8'))
        return results
    
    async def websocket_connect(self, url: str) -> websockets.WebSocketClientProtocol:
        """连接WebSocket
        
        Args:
            url: WebSocket URL
            
        Returns:
            WebSocket连接
        """
        ws = await asyncio.wait_for(websockets.connect(url), timeout=TestConfig.WS_TIMEOUT)
        self.ws_connections.append(ws)
        return ws
    
    async def websocket_send(self, ws: websockets.WebSocketClientProtocol, data: Dict[str, Any]) -> Dict[str, Any]:
        """发送WebSocket消息
        
        Args:
            ws: WebSocket连接
            data: 消息数据
            
        Returns:
            响应数据
        """
        await ws.send(json.dumps(data))
        response = await ws.recv()
        return json.loads(response)
    
    def wait_for_service(self, url: str, max_retries: int = 30, retry_interval: float = 1.0) -> bool:
        """等待服务启动
        
        Args:
            url: 服务URL
            max_retries: 最大重试次数
            retry_interval: 重试间隔（秒）
            
        Returns:
            服务是否可用
        """
        import requests
        
        for i in range(max_retries):
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    return True
            except:
                pass
            time.sleep(retry_interval)
        
        return False
    
    def generate_test_data(self, count: int = 1) -> List[Dict[str, Any]]:
        """生成测试数据
        
        Args:
            count: 数据数量
            
        Returns:
            测试数据列表
        """
        data = []
        for i in range(count):
            data.append({
                "id": f"test_{i}",
                "message": f"Test message {i}",
                "timestamp": time.time()
            })
        return data


class TestReporter:
    """测试报告类"""
    
    def __init__(self):
        """初始化测试报告"""
        self.test_results = []
        self.start_time = time.time()
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
    
    def add_result(self, test_name: str, passed: bool, error: str = None):
        """添加测试结果
        
        Args:
            test_name: 测试名称
            passed: 是否通过
            error: 错误信息
        """
        self.test_results.append({
            "test_name": test_name,
            "passed": passed,
            "error": error,
            "duration": time.time() - self.start_time
        })
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
    
    def generate_report(self) -> str:
        """生成测试报告
        
        Returns:
            测试报告HTML
        """
        duration = time.time() - self.start_time
        pass_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; margin-bottom: 20px; }}
                .summary {{ display: flex; justify-content: space-between; }}
                .summary-item {{ text-align: center; }}
                .summary-value {{ font-size: 24px; font-weight: bold; }}
                .summary-label {{ color: #666; }}
                .test-results {{ margin-top: 20px; }}
                .test-result {{ padding: 10px; margin-bottom: 10px; border-radius: 5px; }}
                .passed {{ background-color: #d4edda; }}
                .failed {{ background-color: #f8d7da; }}
                .error {{ color: #721c24; margin-top: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Test Report</h1>
                <div class="summary">
                    <div class="summary-item">
                        <div class="summary-value">{self.total_tests}</div>
                        <div class="summary-label">Total Tests</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value">{self.passed_tests}</div>
                        <div class="summary-label">Passed</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value">{self.failed_tests}</div>
                        <div class="summary-label">Failed</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value">{pass_rate:.1f}%</div>
                        <div class="summary-label">Pass Rate</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value">{duration:.2f}s</div>
                        <div class="summary-label">Duration</div>
                    </div>
                </div>
            </div>
            <div class="test-results">
                <h2>Test Results</h2>
        """
        
        for result in self.test_results:
            status_class = "passed" if result["passed"] else "failed"
            error_html = f'<div class="error">{result["error"]}</div>' if result["error"] else ""
            
            html += f"""
                <div class="test-result {status_class}">
                    <strong>{result["test_name"]}</strong> - {"PASSED" if result["passed"] else "FAILED"}
                    {error_html}
                </div>
            """
        
        html += """
            </div>
        </body>
        </html>
        """
        
        return html
    
    def save_report(self, filename: str = None):
        """保存测试报告
        
        Args:
            filename: 报告文件名
        """
        if filename is None:
            filename = os.path.join(TestConfig.REPORT_DIR, TestConfig.REPORT_FILE)
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.generate_report())
