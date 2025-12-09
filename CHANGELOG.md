# 更新日志

本文档记录了文件差异比较工具的所有重要更新。

## [1.0.0] - 2025-12-09

### 新增

- 初始版本发布
- 支持Excel文件(.xlsx, .xls)的差异比较
- 提供图形用户界面(GUI)和命令行接口
- 支持差异结果导出为CSV文件
- 提供示例数据和测试用例

### 功能特点

- 直观的GUI界面，易于使用
- 支持大文件处理，内存优化
- 精确的单元格级别比较
- 高亮显示差异内容
- 支持筛选和排序功能

### 技术栈

- Python 3.7+
- PyQt6 (GUI框架)
- pandas (数据处理)

### 文件结构

```
file-diff-tools/
├── main.py                 # 主入口脚本
├── start.bat              # Windows启动脚本
├── file_diff.py           # 核心差异比较逻辑
├── file_diff_gui.py       # GUI界面实现
├── test.py                # 测试脚本
├── generate_examples.py   # 示例数据生成脚本
├── requirements.txt       # 依赖包列表
├── README.md              # 项目说明文档
├── LICENSE                # MIT开源许可证
├── .gitignore             # Git忽略文件配置
├── assets/                # 资源文件目录
│   ├── icons/             # 图标文件
│   │   └── app.ico        # 应用程序图标
│   └── README.md          # 资源文件说明
└── examples/              # 示例数据和测试用例
    ├── employees_original.xlsx
    ├── employees_modified.xlsx
    ├── products_original.xlsx
    ├── products_modified.xlsx
    └── README.md
```

## 未来计划

### [1.1.0] - 计划中

- [ ] 支持更多文件格式(JSON, XML等等)
- [ ] 添加文件合并功能
- [ ] 支持批量文件比较
- [ ] 添加比较历史记录
- [ ] 支持自定义比较规则

### [1.2.0] - 计划中

- [ ] 添加插件系统
- [ ] 支持云存储集成
- [ ] 添加协作功能
- [ ] 支持命令行高级参数
- [ ] 添加自动化测试

---

## 贡献

欢迎提交问题报告和功能请求！请查看 [贡献指南](CONTRIBUTING.md) 了解如何参与项目开发。

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。
