#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
控制服务测试脚本
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
    test_name = "控制服务健康检查"
    try:
        response = await helper.get(f"{TestConfig.CONTROL_SERVICE_URL}/health")
        assert response["status"] == "healthy", f"健康检查失败: {response}"
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def test_user_registration(helper: TestHelper, reporter: TestReporter):
    """测试用户注册"""
    test_name = "控制服务用户注册"
    try:
        user_data = {
            "username": f"test_user_{int(asyncio.get_event_loop().time())}",
            "password": "test_password",
            "email": "test@example.com"
        }
        response = await helper.post(f"{TestConfig.CONTROL_SERVICE_URL}/api/auth/register", user_data)
        assert "user_id" in response or "success" in response, f"用户注册失败: {response}"
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def test_user_login(helper: TestHelper, reporter: TestReporter):
    """测试用户登录"""
    test_name = "控制服务用户登录"
    try:
        login_data = {
            "username": TestConfig.TEST_USER["username"],
            "password": TestConfig.TEST_USER["password"]
        }
        response = await helper.post(f"{TestConfig.CONTROL_SERVICE_URL}/api/auth/login", login_data)
        assert "token" in response or "success" in response, f"用户登录失败: {response}"
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def test_session_creation(helper: TestHelper, reporter: TestReporter):
    """测试会话创建"""
    test_name = "控制服务会话创建"
    try:
        session_data = {
            "user_id": "test_user",
            "session_type": "chat"
        }
        response = await helper.post(f"{TestConfig.CONTROL_SERVICE_URL}/api/session/create", session_data)
        assert "session_id" in response or "session" in response, f"会话创建失败: {response}"
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def test_session_management(helper: TestHelper, reporter: TestReporter):
    """测试会话管理"""
    test_name = "控制服务会话管理"
    try:
        # 创建会话
        session_data = {
            "user_id": "test_user",
            "session_type": "chat"
        }
        create_response = await helper.post(f"{TestConfig.CONTROL_SERVICE_URL}/api/session/create", session_data)
        session_id = create_response.get("session_id", "test_session_id")
        
        # 获取会话信息
        get_response = await helper.get(f"{TestConfig.CONTROL_SERVICE_URL}/api/session/{session_id}")
        assert get_response is not None, "获取会话信息失败"
        
        # 更新会话
        update_data = {
            "session_id": session_id,
            "status": "active"
        }
        update_response = await helper.post(f"{TestConfig.CONTROL_SERVICE_URL}/api/session/update", update_data)
        assert update_response is not None, "更新会话失败"
        
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def test_message_routing(helper: TestHelper, reporter: TestReporter):
    """测试消息路由"""
    test_name = "控制服务消息路由"
    try:
        message = {
            "type": "text",
            "content": "Test routing message",
            "user_id": "test_user",
            "session_id": "test_session"
        }
        response = await helper.post(f"{TestConfig.CONTROL_SERVICE_URL}/api/router/route", message)
        assert "route" in response or "success" in response, f"消息路由失败: {response}"
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def test_realtime_output(helper: TestHelper, reporter: TestReporter):
    """测试实时输出"""
    test_name = "控制服务实时输出"
    try:
        output_data = {
            "session_id": "test_session",
            "type": "model_output",
            "content": "This is a realtime output test"
        }
        response = await helper.post(f"{TestConfig.CONTROL_SERVICE_URL}/api/realtime/output", output_data)
        assert "success" in response or response is not None, f"实时输出失败: {response}"
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def test_concurrent_sessions(helper: TestHelper, reporter: TestReporter):
    """测试并发会话"""
    test_name = "控制服务并发会话"
    try:
        # 创建多个并发会话
        tasks = []
        for i in range(TestConfig.CONCURRENT_USERS):
            session_data = {
                "user_id": f"test_user_{i}",
                "session_type": "chat"
            }
            task = helper.post(f"{TestConfig.CONTROL_SERVICE_URL}/api/session/create", session_data)
            tasks.append(task)
        
        # 等待所有请求完成
        responses = await asyncio.gather(*tasks)
        
        assert len(responses) == TestConfig.CONCURRENT_USERS, f"响应数量不正确: {len(responses)}"
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def test_user_permissions(helper: TestHelper, reporter: TestReporter):
    """测试用户权限"""
    test_name = "控制服务用户权限"
    try:
        # 测试不同权限级别的用户
        permission_levels = ["admin", "user", "guest"]
        
        for permission in permission_levels:
            user_data = {
                "username": f"test_{permission}",
                "password": "test_password",
                "permission": permission
            }
            response = await helper.post(f"{TestConfig.CONTROL_SERVICE_URL}/api/auth/check_permission", user_data)
            assert response is not None, f"{permission}权限检查失败"
        
        reporter.add_result(test_name, True)
        print(f"[PASS] {test_name} - PASSED")
    except Exception as e:
        reporter.add_result(test_name, False, str(e))
        print(f"[FAIL] {test_name} - FAILED: {e}")


async def run_control_service_tests():
    """运行控制服务测试"""
    print("=" * 60)
    print("开始运行控制服务测试")
    print("=" * 60)
    
    reporter = TestReporter()
    
    async with TestHelper() as helper:
        # 等待服务启动
        print("等待控制服务启动...")
        if not helper.wait_for_service(f"{TestConfig.CONTROL_SERVICE_URL}/health"):
            print("控制服务启动失败，请检查服务是否正常运行")
            return
        
        print("控制服务已启动，开始测试...")
        print()
        
        # 运行所有测试
        await test_health_check(helper, reporter)
        await test_user_registration(helper, reporter)
        await test_user_login(helper, reporter)
        await test_session_creation(helper, reporter)
        await test_session_management(helper, reporter)
        await test_message_routing(helper, reporter)
        await test_realtime_output(helper, reporter)
        await test_concurrent_sessions(helper, reporter)
        await test_user_permissions(helper, reporter)
    
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
    success = asyncio.run(run_control_service_tests())
    sys.exit(0 if success else 1)
