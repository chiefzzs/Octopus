#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
批量替换测试文件中的Unicode字符
"""

import os
import glob

# 查找所有测试文件
test_files = glob.glob("tests/*.py")

# 替换Unicode字符
replacements = {
    "✓": "[PASS]",
    "✗": "[FAIL]"
}

for file_path in test_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换Unicode字符
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已处理文件: {file_path}")

print("所有文件处理完成")
