import sys
import os
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QTabWidget,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QCheckBox,
    QTextEdit,
    QFileDialog,
    QProgressBar,
    QMessageBox,
    QSplitter,
    QFrame,
    QScrollArea,
    QGridLayout,
    QSpinBox,
    QRadioButton,
    QButtonGroup,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor, QPixmap
from typing import Dict, List, Union
from datetime import datetime

# 导入我们的差异比较函数
from file_diff import two_file_diff


class DiffWorkerThread(QThread):
    """差异比较工作线程"""

    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    progress = pyqtSignal(str)

    def __init__(self, params):
        super().__init__()
        self.params = params

    def run(self):
        try:
            self.progress.emit("开始比较文件...")
            result = two_file_diff(**self.params)
            self.progress.emit("比较完成！")
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class ExcelDiffGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文件差异比较工具")
        self.setGeometry(100, 100, 600, 800)

        # 设置应用图标
        icon_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "assets", "icons", "app.ico"
        )
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # 设置样式
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #c0c0c0;
                background-color: white;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background-color: #e1e1e1;
                border: 1px solid #c0c0c0;
                padding: 8px 16px;
                margin-right: 2px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                border-bottom: 1px solid white;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QLineEdit, QComboBox, QSpinBox {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
            QTextEdit {
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
            QProgressBar {
                border: 1px solid #cccccc;
                border-radius: 3px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 2px;
            }
        """
        )

        self.init_ui()

    def init_ui(self):
        # 主窗口部件
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # 创建标题
        title_label = QLabel("文件差异比较工具")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #333333; margin: 10px;")
        main_layout.addWidget(title_label)

        # 创建选项卡
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # 创建文件比较选项卡
        self.create_file_comparison_tab()

        # 创建结果选项卡
        self.create_results_tab()

        # 创建状态栏
        self.create_status_bar()

        # 初始化UI状态
        self.on_file_type_changed()

    def create_file_comparison_tab(self):
        # 文件比较选项卡
        file_tab = QWidget()
        file_layout = QVBoxLayout()
        file_tab.setLayout(file_layout)

        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_content.setLayout(scroll_layout)

        # 比较模式选择
        mode_group = QGroupBox("比较模式")
        mode_layout = QHBoxLayout()
        mode_group.setLayout(mode_layout)

        self.file_mode_radio = QRadioButton("文件比较模式")
        self.file_mode_radio.setChecked(True)
        self.file_mode_radio.toggled.connect(self.on_mode_changed)
        self.sheet_mode_radio = QRadioButton("Sheet比较模式")
        self.sheet_mode_radio.toggled.connect(self.on_mode_changed)

        mode_layout.addWidget(self.file_mode_radio)
        mode_layout.addWidget(self.sheet_mode_radio)
        mode_layout.addStretch()

        scroll_layout.addWidget(mode_group)

        # 文件类型选择
        file_type_group = QGroupBox("文件类型")
        file_type_layout = QHBoxLayout()
        file_type_group.setLayout(file_type_layout)

        self.file_type_combo = QComboBox()
        self.file_type_combo.addItems(["excel", "csv", "txt"])
        self.file_type_combo.currentIndexChanged.connect(self.on_file_type_changed)

        file_type_layout.addWidget(QLabel("文件类型:"))
        file_type_layout.addWidget(self.file_type_combo)
        file_type_layout.addStretch()

        scroll_layout.addWidget(file_type_group)

        # 文件选择区域
        self.file_selection_group = QGroupBox("文件选择")
        file_selection_layout = QGridLayout()
        self.file_selection_group.setLayout(file_selection_layout)

        # 第一个文件
        file_selection_layout.addWidget(QLabel("文件1:"), 0, 0)
        self.file1_path_edit = QLineEdit()
        self.file1_path_edit.setPlaceholderText("选择第一个文件...")
        file_selection_layout.addWidget(self.file1_path_edit, 0, 1)
        self.file1_browse_btn = QPushButton("浏览...")
        self.file1_browse_btn.clicked.connect(self.browse_file1)
        file_selection_layout.addWidget(self.file1_browse_btn, 0, 2)

        # 第二个文件
        self.file2_label = QLabel("文件2:")
        file_selection_layout.addWidget(self.file2_label, 1, 0)
        self.file2_path_edit = QLineEdit()
        self.file2_path_edit.setPlaceholderText("选择第二个文件...")
        file_selection_layout.addWidget(self.file2_path_edit, 1, 1)
        self.file2_browse_btn = QPushButton("浏览...")
        self.file2_browse_btn.clicked.connect(self.browse_file2)
        file_selection_layout.addWidget(self.file2_browse_btn, 1, 2)

        # Sheet选择（初始隐藏）
        self.sheet_selection_group = QGroupBox("Sheet选择")
        sheet_selection_layout = QGridLayout()
        self.sheet_selection_group.setLayout(sheet_selection_layout)
        self.sheet_selection_group.hide()

        sheet_selection_layout.addWidget(QLabel("Sheet1:"), 0, 0)
        self.sheet1_combo = QComboBox()
        sheet_selection_layout.addWidget(self.sheet1_combo, 0, 1)

        sheet_selection_layout.addWidget(QLabel("Sheet2:"), 1, 0)
        self.sheet2_combo = QComboBox()
        sheet_selection_layout.addWidget(self.sheet2_combo, 1, 1)

        scroll_layout.addWidget(self.file_selection_group)
        scroll_layout.addWidget(self.sheet_selection_group)

        # 比较选项
        options_group = QGroupBox("比较选项")
        options_layout = QGridLayout()
        options_group.setLayout(options_layout)

        options_layout.addWidget(QLabel("关键列:"), 0, 0)
        self.key_column_edit = QLineEdit()
        self.key_column_edit.setPlaceholderText("输入用于匹配行的关键列名...")
        options_layout.addWidget(self.key_column_edit, 0, 1)

        # 分隔符标签和输入框 - 保存为实例变量以便后续控制
        self.delimiter_label = QLabel("分隔符:")
        self.delimiter_edit = QLineEdit(",")
        options_layout.addWidget(self.delimiter_label, 1, 0)
        options_layout.addWidget(self.delimiter_edit, 1, 1)

        self.output_report_check = QCheckBox("生成差异报告")
        self.output_report_check.setChecked(True)
        options_layout.addWidget(self.output_report_check, 2, 0, 1, 2)

        self.report_path_edit = QLineEdit()
        self.report_path_edit.setPlaceholderText("报告保存路径（留空自动生成）...")
        options_layout.addWidget(self.report_path_edit, 3, 1)
        self.report_browse_btn = QPushButton("浏览...")
        self.report_browse_btn.clicked.connect(self.browse_report_path)
        options_layout.addWidget(self.report_browse_btn, 3, 2)

        scroll_layout.addWidget(options_group)

        # 操作按钮
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        self.compare_btn = QPushButton("开始比较")
        self.compare_btn.clicked.connect(self.start_comparison)
        self.compare_btn.setMinimumHeight(40)
        self.compare_btn.setMinimumWidth(150)
        buttons_layout.addWidget(self.compare_btn)

        scroll_layout.addLayout(buttons_layout)
        scroll_layout.addStretch()

        scroll_area.setWidget(scroll_content)
        file_layout.addWidget(scroll_area)

        self.tab_widget.addTab(file_tab, "文件比较")

    def create_results_tab(self):
        # 结果选项卡
        results_tab = QWidget()
        results_layout = QVBoxLayout()
        results_tab.setLayout(results_layout)

        # 创建筛选和控制面板
        filter_control_group = QGroupBox("筛选与显示控制")
        filter_control_layout = QVBoxLayout()
        filter_control_group.setLayout(filter_control_layout)

        # 筛选输入框
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("差异筛选:"))
        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText("输入关键字筛选差异项...")
        self.filter_edit.textChanged.connect(self.apply_filter)
        filter_layout.addWidget(self.filter_edit)

        self.filter_btn = QPushButton("应用筛选")
        self.filter_btn.clicked.connect(self.apply_filter)
        filter_layout.addWidget(self.filter_btn)

        self.clear_filter_btn = QPushButton("清除筛选")
        self.clear_filter_btn.clicked.connect(self.clear_filter)
        filter_layout.addWidget(self.clear_filter_btn)

        filter_control_layout.addLayout(filter_layout)

        # 显示控制复选框
        checkbox_layout = QHBoxLayout()
        self.show_stats_check = QCheckBox("显示统计信息")
        self.show_stats_check.setChecked(True)
        self.show_stats_check.stateChanged.connect(self.apply_filter)
        checkbox_layout.addWidget(self.show_stats_check)

        self.show_not_in_file1_check = QCheckBox("显示仅在数据源2中存在")
        self.show_not_in_file1_check.setChecked(True)
        self.show_not_in_file1_check.stateChanged.connect(self.apply_filter)
        checkbox_layout.addWidget(self.show_not_in_file1_check)

        self.show_not_in_file2_check = QCheckBox("显示仅在数据源1中存在")
        self.show_not_in_file2_check.setChecked(True)
        self.show_not_in_file2_check.stateChanged.connect(self.apply_filter)
        checkbox_layout.addWidget(self.show_not_in_file2_check)

        filter_control_layout.addLayout(checkbox_layout)
        results_layout.addWidget(filter_control_group)

        # 创建滚动区域来包含结果表格，以支持水平滚动
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # 结果表格
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(1)
        self.results_table.setHorizontalHeaderLabels(["差异详情信息"])
        # 设置列宽策略，允许水平滚动
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)
        self.results_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.results_table.setAlternatingRowColors(True)

        # 将表格设置为滚动区域的子控件
        scroll_area.setWidget(self.results_table)

        # 将滚动区域添加到布局中
        results_layout.addWidget(scroll_area)

        # 存储原始结果数据
        self.original_results = None

        self.tab_widget.addTab(results_tab, "比较结果")

    def create_status_bar(self):
        # 状态栏
        status_layout = QHBoxLayout()

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        status_layout.addWidget(self.progress_bar)

        self.status_label = QLabel("就绪")
        status_layout.addWidget(self.status_label)

        status_widget = QWidget()
        status_widget.setLayout(status_layout)
        self.statusBar().addWidget(status_widget, 1)

    def on_mode_changed(self):
        """比较模式改变时的处理"""
        is_file_mode = self.file_mode_radio.isChecked()

        if is_file_mode:
            self.file_selection_group.show()
            self.sheet_selection_group.hide()
            self.file2_label.setText("文件2:")
            self.file2_path_edit.setPlaceholderText("选择第二个文件...")
            self.file2_browse_btn.show()
        else:
            self.file_selection_group.show()
            self.sheet_selection_group.show()
            self.file2_label.setText("文件路径:")
            self.file2_path_edit.setPlaceholderText("选择包含多个Sheet的Excel文件...")
            self.file2_browse_btn.show()

    def on_file_type_changed(self):
        """文件类型改变时的处理"""
        file_type = self.file_type_combo.currentText()

        if file_type == "excel":
            self.delimiter_edit.setEnabled(False)
            self.delimiter_edit.hide()
            # 隐藏分隔符标签
            self.delimiter_label.hide()
        else:
            self.delimiter_edit.setEnabled(True)
            self.delimiter_edit.show()
            # 显示分隔符标签
            self.delimiter_label.show()

    def browse_file1(self):
        """浏览第一个文件"""
        file_type = self.file_type_combo.currentText()
        if file_type == "excel":
            filter_str = "Excel文件 (*.xlsx *.xls);;所有文件 (*.*)"
        elif file_type == "csv":
            filter_str = "CSV文件 (*.csv);;所有文件 (*.*)"
        else:
            filter_str = "文本文件 (*.txt);;所有文件 (*.*)"

        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择第一个文件", "", filter_str
        )
        if file_path:
            self.file1_path_edit.setText(file_path)

            # 如果是Excel文件，尝试加载Sheet列表
            if file_type == "excel":
                self.load_excel_sheets(file_path)

    def browse_file2(self):
        """浏览第二个文件"""
        is_file_mode = self.file_mode_radio.isChecked()
        file_type = self.file_type_combo.currentText()

        if file_type == "excel":
            filter_str = "Excel文件 (*.xlsx *.xls);;所有文件 (*.*)"
        elif file_type == "csv":
            filter_str = "CSV文件 (*.csv);;所有文件 (*.*)"
        else:
            filter_str = "文本文件 (*.txt);;所有文件 (*.*)"

        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择第二个文件", "", filter_str
        )
        if file_path:
            self.file2_path_edit.setText(file_path)

            # 如果是Excel文件且是文件比较模式，尝试加载Sheet列表
            if file_type == "excel" and is_file_mode:
                self.load_excel_sheets(file_path)

    def browse_report_path(self):
        """浏览报告保存路径"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "选择报告保存路径", "", "CSV文件 (*.csv);;所有文件 (*.*)"
        )
        if file_path:
            self.report_path_edit.setText(file_path)

    def load_excel_sheets(self, file_path):
        """加载Excel文件的Sheet列表"""
        try:
            excel_file = pd.ExcelFile(file_path)
            sheet_names = excel_file.sheet_names

            self.sheet1_combo.clear()
            self.sheet1_combo.addItems(sheet_names)

            self.sheet2_combo.clear()
            self.sheet2_combo.addItems(sheet_names)

            if len(sheet_names) >= 2:
                self.sheet2_combo.setCurrentIndex(1)

        except Exception as e:
            QMessageBox.warning(self, "错误", f"无法加载Excel文件: {str(e)}")

    def start_comparison(self):
        """开始比较"""
        # 验证输入
        if not self.file1_path_edit.text():
            QMessageBox.warning(self, "警告", "请选择第一个文件")
            return

        if not self.file2_path_edit.text():
            QMessageBox.warning(self, "警告", "请选择第二个文件")
            return

        if not self.key_column_edit.text():
            QMessageBox.warning(self, "警告", "请输入关键列名")
            return

        is_file_mode = self.file_mode_radio.isChecked()
        file_type = self.file_type_combo.currentText()

        # 准备参数
        params = {
            "file1_path": self.file1_path_edit.text(),
            "file2_path": self.file2_path_edit.text() if is_file_mode else None,
            "key_column": self.key_column_edit.text(),
            "output_report": self.output_report_check.isChecked(),
            "report_path": (
                self.report_path_edit.text() if self.report_path_edit.text() else None
            ),
            "compare_mode": "file" if is_file_mode else "sheet",
            "file_path_for_sheet": (
                self.file2_path_edit.text() if not is_file_mode else None
            ),
            "file_type": file_type,
            "delimiter": self.delimiter_edit.text(),
        }

        if not is_file_mode:
            params["sheet1"] = self.sheet1_combo.currentText()
            params["sheet2"] = self.sheet2_combo.currentText()

        # 禁用比较按钮
        self.compare_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 不确定进度
        self.status_label.setText("正在比较...")

        # 切换到结果选项卡
        self.tab_widget.setCurrentIndex(1)

        # 清空结果表格
        self.results_table.setRowCount(0)

        # 启动工作线程
        self.worker_thread = DiffWorkerThread(params)
        self.worker_thread.finished.connect(self.on_comparison_finished)
        self.worker_thread.error.connect(self.on_comparison_error)
        self.worker_thread.progress.connect(self.on_progress_update)
        self.worker_thread.start()

    def on_comparison_finished(self, results):
        """比较完成处理"""
        # 恢复UI状态
        self.compare_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText("比较完成")

        # 显示结果
        self.display_results(results)

    def on_comparison_error(self, error_msg):
        """比较错误处理"""
        # 恢复UI状态
        self.compare_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText("比较出错")

        # 显示错误消息
        QMessageBox.critical(self, "错误", f"比较过程中出错: {error_msg}")

    def on_progress_update(self, message):
        """进度更新处理"""
        self.status_label.setText(message)

    def display_results(self, results):
        """显示比较结果"""
        # 保存原始结果数据
        self.original_results = results

        # 应用筛选和显示控制
        self.apply_filter()

    def apply_filter(self):
        """应用筛选和显示控制"""
        if not self.original_results:
            return

        # 清空表格
        self.results_table.setRowCount(0)

        # 获取筛选文本和显示控制状态
        filter_text = self.filter_edit.text().lower()
        show_stats = self.show_stats_check.isChecked()
        show_not_in_file1 = self.show_not_in_file1_check.isChecked()
        show_not_in_file2 = self.show_not_in_file2_check.isChecked()

        # 添加结果数据
        row = 0

        # 添加统计信息 - 根据复选框状态决定是否显示
        if show_stats:
            self.results_table.insertRow(row)
            stats_item = QTableWidgetItem("统计信息:")
            stats_item.setBackground(QColor(200, 220, 255))  # 浅蓝色背景
            self.results_table.setItem(row, 0, stats_item)
            row += 1

            self.results_table.insertRow(row)
            self.results_table.setItem(
                row,
                0,
                QTableWidgetItem(
                    f"完全一致的行数: {len(self.original_results['identical'])}"
                ),
            )
            row += 1

            self.results_table.insertRow(row)
            self.results_table.setItem(
                row,
                0,
                QTableWidgetItem(
                    f"有差异的行数: {len(self.original_results['mismatch'])}"
                ),
            )
            row += 1

            self.results_table.insertRow(row)
            self.results_table.setItem(
                row,
                0,
                QTableWidgetItem(
                    f"仅在数据源1中存在的行数: {len(self.original_results['not_in_file1'])}"
                ),
            )
            row += 1

            self.results_table.insertRow(row)
            self.results_table.setItem(
                row,
                0,
                QTableWidgetItem(
                    f"仅在数据源2中存在的行数: {len(self.original_results['not_in_file2'])}"
                ),
            )
            row += 1

        # 添加"仅在数据源2中存在"的数据 - 根据复选框状态决定是否显示
        if show_not_in_file1 and self.original_results["not_in_file1"]:
            self.results_table.insertRow(row)
            not_in_file1_item = QTableWidgetItem("仅在数据源2中存在:")
            not_in_file1_item.setBackground(QColor(255, 220, 200))  # 浅橙色背景
            self.results_table.setItem(row, 0, not_in_file1_item)
            row += 1

            for item in self.original_results["not_in_file1"]:
                self.results_table.insertRow(row)
                self.results_table.setItem(row, 0, QTableWidgetItem(f"{item}"))
                row += 1

        # 添加"仅在数据源1中存在"的数据 - 根据复选框状态决定是否显示
        if show_not_in_file2 and self.original_results["not_in_file2"]:
            self.results_table.insertRow(row)
            not_in_file2_item = QTableWidgetItem("仅在数据源1中存在:")
            not_in_file2_item.setBackground(QColor(255, 220, 200))  # 浅橙色背景
            self.results_table.setItem(row, 0, not_in_file2_item)
            row += 1

            for item in self.original_results["not_in_file2"]:
                self.results_table.insertRow(row)
                self.results_table.setItem(row, 0, QTableWidgetItem(f"{item}"))
                row += 1

        # 添加差异数据 - 显示在顶部以提高可读性
        if self.original_results["mismatch"]:
            # 应用筛选
            filtered_mismatch = []
            if filter_text:
                for item in self.original_results["mismatch"]:
                    if filter_text in item.lower():
                        filtered_mismatch.append(item)
            else:
                filtered_mismatch = self.original_results["mismatch"]

            if filtered_mismatch:
                self.results_table.insertRow(row)
                mismatch_item = QTableWidgetItem("差异详情:")
                mismatch_item.setBackground(QColor(255, 200, 200))  # 浅红色背景
                self.results_table.setItem(row, 0, mismatch_item)
                row += 1

                for item in filtered_mismatch:
                    self.results_table.insertRow(row)
                    self.results_table.setItem(row, 0, QTableWidgetItem(item))
                    row += 1
    def clear_filter(self):
        """清除筛选"""
        self.filter_edit.clear()
        self.apply_filter()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExcelDiffGUI()
    window.show()
    sys.exit(app.exec())
