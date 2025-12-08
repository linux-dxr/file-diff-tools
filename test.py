#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试脚本
用于测试文件差异比较功能
"""

import os
import sys
import pandas as pd
from file_diff import two_file_diff


def test_file_diff():
    """测试文件差异比较功能"""

    # 添加当前目录到Python路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    examples_dir = os.path.join(current_dir, "examples")

    # 测试用例1: 员工信息表比较
    print("测试用例1: 员工信息表比较")
    file1 = os.path.join(examples_dir, "employees_original.xlsx")
    file2 = os.path.join(examples_dir, "employees_modified.xlsx")

    if os.path.exists(file1) and os.path.exists(file2):
        result = two_file_diff(file1, file2)
        print(f"  - 比较完成，共发现 {len(result)} 处差异")

        # 保存结果
        output_file = os.path.join(examples_dir, "employees_diff_result.csv")
        result.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"  - 结果已保存到: {output_file}")
    else:
        print("  - 测试文件不存在，跳过测试")

    print()

    # 测试用例2: 产品销售表比较
    print("测试用例2: 产品销售表比较")
    file1 = os.path.join(examples_dir, "products_original.xlsx")
    file2 = os.path.join(examples_dir, "products_modified.xlsx")

    if os.path.exists(file1) and os.path.exists(file2):
        result = two_file_diff(file1, file2)
        print(f"  - 比较完成，共发现 {len(result)} 处差异")

        # 保存结果
        output_file = os.path.join(examples_dir, "products_diff_result.csv")
        result.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"  - 结果已保存到: {output_file}")
    else:
        print("  - 测试文件不存在，跳过测试")

    print("\n所有测试完成!")


def test_gui():
    """测试GUI界面"""
    print("\n启动GUI界面测试...")
    print("请在GUI界面中:")
    print("1. 选择 examples/employees_original.xlsx 作为第一个文件")
    print("2. 选择 examples/employees_modified.xlsx 作为第二个文件")
    print("3. 点击'比较'按钮")
    print("4. 检查比较结果是否正确显示")
    print("5. 尝试导出结果功能")

    # 导入GUI模块
    try:
        from file_diff_gui import ExcelDiffGUI
        import sys
        from PyQt6.QtWidgets import QApplication

        app = QApplication(sys.argv)
        window = ExcelDiffGUI()
        window.show()
        sys.exit(app.exec())
    except ImportError as e:
        print(f"无法导入GUI模块: {e}")
        print("请确保已安装PyQt6: pip install pyqt6")


if __name__ == "__main__":
    # 运行命令行测试
    test_file_diff()

    # 询问是否运行GUI测试
    choice = input("\n是否运行GUI测试? (y/n): ").lower()
    if choice == "y":
        test_gui()
