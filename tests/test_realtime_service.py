#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
实时输出服务测试脚本
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
    test_name = "实时输出服务健康检查"
    try:
        response = await helper.get(f"{TestConfig.REALTIME_SERVICE_URL}/health")
        assert response["status"] == "healthy", f"健康检查失败: {response}"
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def test_streaming_api(helper: TestHelper, reporter: TestReporter):
    """测试流式API"""
    test_name = "实时输出服务流式API"
    try:
        message = {
            "type": "text",
            "content": "This is a realtime streaming test message",
            "session_id": "test_session"
        }
        results = await helper.stream_post(f"{TestConfig.REALTIME_SERVICE_URL}/api/realtime/stream", message)
        assert len(results) > 0, "流式响应为空"
        assert any("start" in result for result in results), "缺少开始消息"
        assert any("end" in result for result in results), "缺少结束消息"
        assert any("model_output" in result for result in results), "缺少模型输出消息"
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def test_send_message(helper: TestHelper, reporter: TestReporter):
    """测试发送消息"""
    test_name = "实时输出服务发送消息"
    try:
        message = {
            "type": "text",
            "content": "Test send message",
            "session_id": "test_session"
        }
        response = await helper.post(f"{TestConfig.REALTIME_SERVICE_URL}/api/realtime/send", message)
        assert "success" in response or response is not None, f"发送消息失败: {response}"
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def test_broadcast_message(helper: TestHelper, reporter: TestReporter):
    """测试广播消息"""
    test_name = "实时输出服务广播消息"
    try:
        message = {
            "type": "text",
            "content": "Test broadcast message",
            "session_id": "test_session"
        }
        response = await helper.post(f"{TestConfig.REALTIME_SERVICE_URL}/api/realtime/broadcast", message)
        assert "success" in response or response is not None, f"广播消息失败: {response}"
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def test_websocket_connection(helper: TestHelper, reporter: TestReporter):
    """测试WebSocket连接"""
    test_name = "实时输出服务WebSocket连接"
    try:
        ws = await helper.websocket_connect(TestConfig.REALTIME_WS_URL)
        
        # 发送测试消息
        message = {
            "type": "text",
            "content": "WebSocket test message",
            "session_id": "test_session"
        }
        response = await helper.websocket_send(ws, message)
        
        assert response is not None, "WebSocket响应为空"
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def test_concurrent_streams(helper: TestHelper, reporter: TestReporter):
    """测试并发流式请求"""
    test_name = "实时输出服务并发流式请求"
    try:
        # 创建多个并发流式请求
        tasks = []
        for i in range(TestConfig.CONCURRENT_REQUESTS):
            message = {
                "type": "text",
                "content": f"Concurrent streaming test message {i}",
                "session_id": f"test_session_{i}"
            }
            task = helper.stream_post(f"{TestConfig.REALTIME_SERVICE_URL}/api/realtime/stream", message)
            tasks.append(task)
        
        # 等待所有请求完成
        responses = await asyncio.gather(*tasks)
        
        assert len(responses) == TestConfig.CONCURRENT_REQUESTS, f"响应数量不正确: {len(responses)}"
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def test_message_types(helper: TestHelper, reporter: TestReporter):
    """测试不同类型的消息"""
    test_name = "实时输出服务消息类型"
    try:
        # 测试不同类型的消息
        message_types = ["start", "processing", "model_output", "end"]
        
        for msg_type in message_types:
            message = {
                "type": msg_type,
                "content": f"Test {msg_type} message",
                "session_id": "test_session"
            }
            response = await helper.post(f"{TestConfig.REALTIME_SERVICE_URL}/api/realtime/send", message)
            assert response is not None, f"{msg_type}类型消息处理失败"
        
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def test_streaming_performance(helper: TestHelper, reporter: TestReporter):
    """测试流式输出性能"""
    test_name = "实时输出服务流式性能"
    try:
        import time
        
        message = {
            "type": "text",
            "content": "Performance test message",
            "session_id": "test_session"
        }
        
        start_time = time.time()
        results = await helper.stream_post(f"{TestConfig.REALTIME_SERVICE_URL}/api/realtime/stream", message)
        end_time = time.time()
        
        duration = end_time - start_time
        assert len(results) > 0, "流式响应为空"
        assert duration < 10, f"流式响应时间过长: {duration}秒"
        
        print(f"  流式响应时间: {duration:.2f}秒")
        print(f"  响应数据块数量: {len(results)}")
        
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def test_websocket_multiple_connections(helper: TestHelper, reporter: TestReporter):
    """测试多个WebSocket连接"""
    test_name = "实时输出服务多个WebSocket连接"
    try:
        # 创建多个WebSocket连接
        connections = []
        for i in range(TestConfig.CONCURRENT_USERS):
            ws = await helper.websocket_connect(TestConfig.REALTIME_WS_URL)
            connections.append(ws)
        
        # 向每个连接发送消息
        for i, ws in enumerate(connections):
            message = {
                "type": "text",
                "content": f"Multiple connection test message {i}",
                "session_id": f"test_session_{i}"
            }
            response = await helper.websocket_send(ws, message)
            assert response is not None, f"连接{i}响应为空"
        
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def test_message_broker(helper: TestHelper, reporter: TestReporter):
    """测试消息代理"""
    test_name = "实时输出服务消息代理"
    try:
        # 测试消息代理的消息处理
        messages = [
            {"type": "start", "content": "Start message", "session_id": "test_session"},
            {"type": "processing", "content": "Processing message", "session_id": "test_session"},
            {"type": "end", "content": "End message", "session_id": "test_session"}
        ]
        
        for message in messages:
            response = await helper.post(f"{TestConfig.REALTIME_SERVICE_URL}/api/realtime/send", message)
            assert response is not None, f"消息代理处理失败: {message['type']}"
        
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def run_realtime_service_tests():
    """运行实时输出服务测试"""
    print("=" * 60)
    print("开始运行实时输出服务测试")
    print("=" * 60)
    
    reporter = TestReporter()
    
    async with TestHelper() as helper:
        # 等待服务启动
        print("等待实时输出服务启动...")
        if not helper.wait_for_service(f"{TestConfig.REALTIME_SERVICE_URL}/health"):
            print("实时输出服务启动失败，请检查服务是否正常运行")
            return
        
        print("实时输出服务已启动，开始测试...")
        print()
        
        # 运行所有测试
        await test_health_check(helper, reporter)
        await test_streaming_api(helper, reporter)
        await test_send_message(helper, reporter)
        await test_broadcast_message(helper, reporter)
        await test_websocket_connection(helper, reporter)
        await test_concurrent_streams(helper, reporter)
        await test_message_types(helper, reporter)
        await test_streaming_performance(helper, reporter)
        await test_websocket_multiple_connections(helper, reporter)
        await test_message_broker(helper, reporter)
    
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
    success = asyncio.run(run_realtime_service_tests())
    sys.exit(0 if success else 1)
