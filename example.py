#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JPG与RAW文件同步删除工具 - 使用示例
"""

import os
import subprocess
import tempfile
from pathlib import Path


def create_test_files():
    """创建测试文件结构"""
    # 创建临时目录
    test_dir = tempfile.mkdtemp(prefix="jpg_del_raw_test_")
    jpg_dir = os.path.join(test_dir, "jpg")
    raw_dir = os.path.join(test_dir, "raw")
    
    os.makedirs(jpg_dir)
    os.makedirs(raw_dir)
    
    # 创建测试文件
    jpg_files = ["photo001.jpg", "photo002.jpg", "photo005.jpg"]
    raw_files = ["photo001.rw2", "photo002.rw2", "photo003.rw2", "photo004.rw2", "photo005.rw2"]
    
    # 创建JPG文件
    for jpg_file in jpg_files:
        with open(os.path.join(jpg_dir, jpg_file), 'w') as f:
            f.write("fake jpg content")
    
    # 创建RAW文件
    for raw_file in raw_files:
        with open(os.path.join(raw_dir, raw_file), 'w') as f:
            f.write("fake raw content" * 1000)  # 让文件稍微大一些
    
    print(f"测试文件已创建在: {test_dir}")
    print(f"JPG文件: {jpg_files}")
    print(f"RAW文件: {raw_files}")
    print("预期删除: photo003.rw2, photo004.rw2 (因为没有对应的JPG文件)")
    
    return test_dir, jpg_dir, raw_dir


def run_example():
    """运行示例"""
    print("JPG与RAW文件同步删除工具 - 使用示例")
    print("=" * 50)
    
    # 创建测试文件
    test_dir, jpg_dir, raw_dir = create_test_files()
    
    try:
        print(f"\n运行命令:")
        print(f"python jpg_del_raw.py --jpg-dir '{jpg_dir}' --raw-dir '{raw_dir}' --raw-ext .rw2")
        
        # 运行脚本（预览模式）
        result = subprocess.run([
            "python", "jpg_del_raw.py", 
            "--jpg-dir", jpg_dir,
            "--raw-dir", raw_dir,
            "--raw-ext", ".rw2"
        ], capture_output=True, text=True)
        
        print("\n输出结果:")
        print(result.stdout)
        
        if result.stderr:
            print("错误信息:")
            print(result.stderr)
        
    finally:
        # 清理测试文件
        import shutil
        shutil.rmtree(test_dir)
        print(f"\n测试文件已清理: {test_dir}")


if __name__ == "__main__":
    run_example()
