#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
主测试脚本 - 运行所有测试并生成综合报告
"""

import asyncio
import subprocess
import sys
import os
import time
from datetime import datetime

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from tests.config import TestConfig


class TestRunner:
    """测试运行器"""
    
    def __init__(self):
        """初始化测试运行器"""
        self.test_scripts = [
            "tests/test_access_service.py",
            "tests/test_control_service.py",
            "tests/test_realtime_service.py",
            "tests/test_execution_service.py",
            "tests/test_capability_service.py"
        ]
        self.results = []
        self.start_time = time.time()
    
    async def run_test_script(self, script_path: str) -> dict:
        """运行单个测试脚本
        
        Args:
            script_path: 测试脚本路径
            
        Returns:
            测试结果
        """
        print(f"\n{'=' * 60}")
        print(f"运行测试脚本: {script_path}")
        print(f"{'=' * 60}")
        
        try:
            # 运行测试脚本
            result = subprocess.run(
                [sys.executable, script_path],
                cwd=project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            success = result.returncode == 0
            
            return {
                "script": script_path,
                "success": success,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "script": script_path,
                "success": False,
                "stdout": "",
                "stderr": "测试超时",
                "returncode": -1
            }
        except Exception as e:
            return {
                "script": script_path,
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }
    
    async def run_all_tests(self):
        """运行所有测试"""
        print("=" * 60)
        print("开始运行所有测试")
        print("=" * 60)
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # 运行所有测试脚本
        for script in self.test_scripts:
            result = await self.run_test_script(script)
            self.results.append(result)
            
            # 打印测试结果
            if result["success"]:
                print(f"[PASS] {script} - PASSED")
            else:
                print(f"[FAIL] {script} - FAILED")
                if result["stderr"]:
                    print(f"  错误: {result['stderr'][:200]}")
            
            print()
        
        # 计算总体结果
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["success"])
        failed_tests = total_tests - passed_tests
        duration = time.time() - self.start_time
        
        # 打印总体结果
        print("=" * 60)
        print("测试完成")
        print("=" * 60)
        print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"总测试脚本数: {total_tests}")
        print(f"通过: {passed_tests}")
        print(f"失败: {failed_tests}")
        print(f"通过率: {(passed_tests / total_tests * 100):.1f}%")
        print(f"总耗时: {duration:.2f}秒")
        print()
        
        # 生成综合测试报告
        self.generate_comprehensive_report()
    
    def generate_comprehensive_report(self):
        """生成综合测试报告"""
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["success"])
        failed_tests = total_tests - passed_tests
        duration = time.time() - self.start_time
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Comprehensive Test Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; margin-bottom: 20px; }}
                .summary {{ display: flex; justify-content: space-between; flex-wrap: wrap; }}
                .summary-item {{ text-align: center; flex: 1; min-width: 150px; margin: 10px; }}
                .summary-value {{ font-size: 24px; font-weight: bold; }}
                .summary-label {{ color: #666; }}
                .test-results {{ margin-top: 20px; }}
                .test-result {{ padding: 15px; margin-bottom: 15px; border-radius: 5px; border-left: 4px solid #ccc; }}
                .passed {{ background-color: #d4edda; border-left-color: #28a745; }}
                .failed {{ background-color: #f8d7da; border-left-color: #dc3545; }}
                .test-name {{ font-size: 18px; font-weight: bold; margin-bottom: 10px; }}
                .test-details {{ margin-top: 10px; font-size: 14px; }}
                .error {{ color: #721c24; margin-top: 10px; padding: 10px; background-color: #f5c6cb; border-radius: 3px; }}
                .stdout {{ color: #155724; margin-top: 10px; padding: 10px; background-color: #c3e6cb; border-radius: 3px; white-space: pre-wrap; }}
                .timestamp {{ color: #666; font-size: 12px; margin-top: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Comprehensive Test Report</h1>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <div class="summary">
                    <div class="summary-item">
                        <div class="summary-value">{total_tests}</div>
                        <div class="summary-label">Total Test Scripts</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value">{passed_tests}</div>
                        <div class="summary-label">Passed</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value">{failed_tests}</div>
                        <div class="summary-label">Failed</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value">{pass_rate:.1f}%</div>
                        <div class="summary-label">Pass Rate</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value">{duration:.2f}s</div>
                        <div class="summary-label">Total Duration</div>
                    </div>
                </div>
            </div>
            <div class="test-results">
                <h2>Test Results</h2>
        """
        
        for i, result in enumerate(self.results, 1):
            status_class = "passed" if result["success"] else "failed"
            status_text = "PASSED" if result["success"] else "FAILED"
            
            error_html = ""
            if result["stderr"]:
                error_html = f'<div class="error"><strong>Error:</strong><br>{result["stderr"]}</div>'
            
            stdout_html = ""
            if result["stdout"]:
                stdout_html = f'<div class="stdout"><strong>Output:</strong><br>{result["stdout"][:500]}</div>'
            
            html += f"""
                <div class="test-result {status_class}">
                    <div class="test-name">{i}. {result["script"]} - {status_text}</div>
                    <div class="test-details">
                        <div>Return Code: {result["returncode"]}</div>
                        <div class="timestamp">Tested at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
                    </div>
                    {error_html}
                    {stdout_html}
                </div>
            """
        
        html += """
            </div>
        </body>
        </html>
        """
        
        # 保存综合测试报告
        report_file = os.path.join(TestConfig.REPORT_DIR, "comprehensive_test_report.html")
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"综合测试报告已保存到: {report_file}")


async def main():
    """主函数"""
    runner = TestRunner()
    await runner.run_all_tests()
    
    # 返回测试是否全部通过
    all_passed = all(r["success"] for r in runner.results)
    return all_passed


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
