#!/usr/bin/env python3
"""
文件差异比较工具 - 主入口脚本
用于启动GUI界面
"""

import sys
import os

# 添加当前目录到Python路径，确保可以导入项目模块
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 导入GUI模块
from file_diff_gui import ExcelDiffGUI
from PyQt6.QtWidgets import QApplication


def main():
    """主函数"""
    # 创建应用实例
    app = QApplication(sys.argv)

    # 设置应用信息
    app.setApplicationName("文件差异比较工具")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("FileDiffTools")

    # 创建并显示主窗口
    window = ExcelDiffGUI()
    window.show()

    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
