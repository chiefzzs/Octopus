#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
接入服务测试脚本
"""

import asyncio
import json
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from tests.config import TestConfig
from tests.utils import TestHelper, TestReporter


async def test_health_check(helper: TestHelper, reporter: TestReporter):
    """测试健康检查端点"""
    test_name = "接入服务健康检查"
    try:
        response = await helper.get(f"{TestConfig.ACCESS_SERVICE_URL}/health")
        assert response["status"] == "healthy", f"健康检查失败: {response}"
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def test_http_message(helper: TestHelper, reporter: TestReporter):
    """测试HTTP消息处理"""
    test_name = "接入服务HTTP消息处理"
    try:
        message = {
            "type": "text",
            "content": "This is a test message",
            "user_id": "test_user"
        }
        response = await helper.post(f"{TestConfig.ACCESS_SERVICE_URL}/api/access/message", message)
        assert "result" in response or "message" in response, f"响应格式不正确: {response}"
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def test_streaming_api(helper: TestHelper, reporter: TestReporter):
    """测试流式API"""
    test_name = "接入服务流式API"
    try:
        message = {
            "type": "text",
            "content": "This is a streaming test message",
            "user_id": "test_user"
        }
        results = await helper.stream_post(f"{TestConfig.ACCESS_SERVICE_URL}/api/access/stream", message)
        assert len(results) > 0, "流式响应为空"
        assert any("start" in result for result in results), "缺少开始消息"
        assert any("end" in result for result in results), "缺少结束消息"
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def test_websocket_connection(helper: TestHelper, reporter: TestReporter):
    """测试WebSocket连接"""
    test_name = "接入服务WebSocket连接"
    try:
        ws = await helper.websocket_connect(TestConfig.ACCESS_WS_URL)
        
        # 发送测试消息
        message = {
            "type": "text",
            "content": "WebSocket test message",
            "user_id": "test_user"
        }
        response = await helper.websocket_send(ws, message)
        
        assert response is not None, "WebSocket响应为空"
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def test_concurrent_requests(helper: TestHelper, reporter: TestReporter):
    """测试并发请求"""
    test_name = "接入服务并发请求"
    try:
        # 创建多个并发请求
        tasks = []
        for i in range(TestConfig.CONCURRENT_REQUESTS):
            message = {
                "type": "text",
                "content": f"Concurrent test message {i}",
                "user_id": f"test_user_{i}"
            }
            task = helper.post(f"{TestConfig.ACCESS_SERVICE_URL}/api/access/message", message)
            tasks.append(task)
        
        # 等待所有请求完成
        responses = await asyncio.gather(*tasks)
        
        assert len(responses) == TestConfig.CONCURRENT_REQUESTS, f"响应数量不正确: {len(responses)}"
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def test_message_formatting(helper: TestHelper, reporter: TestReporter):
    """测试消息格式化"""
    test_name = "接入服务消息格式化"
    try:
        # 测试不同类型的消息
        message_types = ["text", "image", "file", "command"]
        
        for msg_type in message_types:
            message = {
                "type": msg_type,
                "content": f"Test {msg_type} message",
                "user_id": "test_user"
            }
            response = await helper.post(f"{TestConfig.ACCESS_SERVICE_URL}/api/access/message", message)
            assert response is not None, f"{msg_type}类型消息处理失败"
        
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def run_access_service_tests():
    """运行接入服务测试"""
    print("=" * 60)
    print("开始运行接入服务测试")
    print("=" * 60)
    
    reporter = TestReporter()
    
    async with TestHelper() as helper:
        # 等待服务启动
        print("等待接入服务启动...")
        if not helper.wait_for_service(f"{TestConfig.ACCESS_SERVICE_URL}/health"):
            print("接入服务启动失败，请检查服务是否正常运行")
            return
        
        print("接入服务已启动，开始测试...")
        print()
        
        # 运行所有测试
        await test_health_check(helper, reporter)
        await test_http_message(helper, reporter)
        await test_streaming_api(helper, reporter)
        await test_websocket_connection(helper, reporter)
        await test_concurrent_requests(helper, reporter)
        await test_message_formatting(helper, reporter)
    
    # 生成测试报告
    print()
    print("=" * 60)
    print("测试完成")
    print("=" * 60)
    print(f"总测试数: {reporter.total_tests}")
    print(f"通过: {reporter.passed_tests}")
    print(f"失败: {reporter.failed_tests}")
    print(f"通过率: {(reporter.passed_tests / reporter.total_tests * 100):.1f}%")
    print()
    
    # 保存测试报告
    reporter.save_report()
    print(f"测试报告已保存到: {os.path.join(TestConfig.REPORT_DIR, TestConfig.REPORT_FILE)}")
    
    return reporter.failed_tests == 0


if __name__ == "__main__":
    success = asyncio.run(run_access_service_tests())
    sys.exit(0 if success else 1)
