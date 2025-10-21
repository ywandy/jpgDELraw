#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JPG与RAW文件同步删除工具
用于将RAW目录中不存在对应JPG文件的RAW文件移动到系统回收站

依赖:
  pip install send2trash
"""

import os
import glob
import argparse
from pathlib import Path

try:
    from send2trash import send2trash
    TRASH_AVAILABLE = True
except ImportError:
    TRASH_AVAILABLE = False


def get_file_basename(filepath):
    """获取文件的基础名称（不包含扩展名）"""
    return Path(filepath).stem


def find_files_with_pattern(pattern):
    """使用通配符模式查找文件"""
    return glob.glob(pattern)


def get_jpg_basenames(jpg_pattern):
    """获取JPG目录中所有文件的基础名称集合"""
    jpg_files = find_files_with_pattern(jpg_pattern)
    jpg_basenames = set()
    
    for jpg_file in jpg_files:
        basename = get_file_basename(jpg_file)
        jpg_basenames.add(basename)
    
    print(f"在JPG目录中找到 {len(jpg_files)} 个文件")
    return jpg_basenames


def find_orphaned_raw_files(raw_pattern, jpg_basenames):
    """查找在JPG目录中没有对应文件的RAW文件"""
    raw_files = find_files_with_pattern(raw_pattern)
    orphaned_files = []
    
    for raw_file in raw_files:
        basename = get_file_basename(raw_file)
        if basename not in jpg_basenames:
            orphaned_files.append(raw_file)
    
    print(f"在RAW目录中找到 {len(raw_files)} 个文件")
    print(f"其中 {len(orphaned_files)} 个文件在JPG目录中没有对应文件")
    
    return orphaned_files


def preview_deletion(orphaned_files):
    """预览将要移动到回收站的文件"""
    if not orphaned_files:
        print("没有找到需要移动到回收站的文件。")
        return False
    
    print("\n以下RAW文件将被移动到回收站：")
    print("-" * 50)
    for i, file_path in enumerate(orphaned_files, 1):
        file_size = os.path.getsize(file_path)
        file_size_mb = file_size / (1024 * 1024)
        print(f"{i:3d}. {file_path} ({file_size_mb:.2f} MB)")
    
    total_size = sum(os.path.getsize(f) for f in orphaned_files)
    total_size_mb = total_size / (1024 * 1024)
    print("-" * 50)
    print(f"总计: {len(orphaned_files)} 个文件，{total_size_mb:.2f} MB")
    
    return True


def delete_files(orphaned_files, dry_run=False):
    """将文件移动到回收站"""
    if not orphaned_files:
        return
    
    if dry_run:
        print("\n[预览模式] 不会实际删除文件")
        return
    
    if not TRASH_AVAILABLE:
        print("\n错误: 未安装 send2trash 库，无法使用回收站功能")
        print("请运行: pip install send2trash")
        return
    
    deleted_count = 0
    failed_count = 0
    
    print("\n开始将文件移动到回收站...")
    for file_path in orphaned_files:
        try:
            send2trash(file_path)
            print(f"✓ 已移动到回收站: {file_path}")
            deleted_count += 1
        except Exception as e:
            print(f"✗ 移动失败: {file_path} - {e}")
            failed_count += 1
    
    print(f"\n操作完成: 成功移动到回收站 {deleted_count} 个，失败 {failed_count} 个")


def confirm_deletion():
    """确认删除操作"""
    while True:
        response = input("\n确定要将这些文件移动到回收站吗? (y/n): ").lower().strip()
        if response in ['y', 'yes', '是']:
            return True
        elif response in ['n', 'no', '否']:
            return False
        else:
            print("请输入 y(是) 或 n(否)")


def main():
    parser = argparse.ArgumentParser(
        description="删除JPG目录中不存在对应文件的RAW文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python jpg_del_raw.py --jpg-dir "./testpath/*.jpg" --raw-dir "./testpath/*.raw"
  python jpg_del_raw.py --jpg-dir "./photos/*.jpeg" --raw-dir "./raw/*.cr2"
  python jpg_del_raw.py --jpg-dir "./jpg/*.jpg" --raw-dir "./raw/*.rw2" --delete --auto-confirm
        """
    )
    
    parser.add_argument('--jpg-dir', 
                       required=True,
                       help='JPG文件模式，例如: ./testpath/*.jpg')
    parser.add_argument('--raw-dir', 
                       required=True,
                       help='RAW文件模式，例如: ./testpath/*.raw')
    parser.add_argument('--delete', 
                       action='store_true',
                       help='将文件移动到回收站（默认为预览模式）')
    parser.add_argument('--auto-confirm', 
                       action='store_true',
                       help='自动确认删除，不提示用户')
    
    args = parser.parse_args()
    
    # 直接使用传入的文件模式
    jpg_pattern = args.jpg_dir
    raw_pattern = args.raw_dir
    
    print("JPG与RAW文件同步删除工具")
    print("=" * 40)
    print(f"JPG文件模式: {args.jpg_dir}")
    print(f"RAW文件模式: {args.raw_dir}")
    print(f"运行模式: {'回收站模式' if args.delete else '预览模式'}")
    print()
    
    # 检查文件模式是否有效（通过检查是否能找到匹配的文件）
    # 这个检查会在后面的文件查找步骤中进行
    
    # 检查是否有匹配的文件
    if not find_files_with_pattern(jpg_pattern):
        print(f"错误: 没有找到匹配的JPG文件: {jpg_pattern}")
        return 1
    
    if not find_files_with_pattern(raw_pattern):
        print(f"错误: 没有找到匹配的RAW文件: {raw_pattern}")
        return 1
    
    # 获取JPG文件的基础名称
    jpg_basenames = get_jpg_basenames(jpg_pattern)
    
    # 查找孤立的RAW文件
    orphaned_files = find_orphaned_raw_files(raw_pattern, jpg_basenames)
    
    # 预览删除列表
    if not preview_deletion(orphaned_files):
        return 0
    
    # 如果不是删除模式，只预览
    if not args.delete:
        print("\n[预览模式] 如需将文件移动到回收站，请添加 --delete 参数")
        return 0
    
    # 确认删除
    if not args.auto_confirm:
        if not confirm_deletion():
            print("操作已取消")
            return 0
    
    # 执行删除
    delete_files(orphaned_files, dry_run=False)
    
    return 0


if __name__ == "__main__":
    exit(main())
