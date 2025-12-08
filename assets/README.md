# 资源文件说明

本目录包含项目使用的各种资源文件。

## 目录结构

```
assets/
├── icons/          # 图标文件
│   └── app.ico     # 应用程序图标
└── README.md       # 本文件
```

## 文件说明

### icons/app.ico
应用程序的主图标，用于：
- 应用程序窗口图标
- 任务栏图标
- 文件关联图标（可选）

## 使用方法

在代码中引用图标文件：

```python
import os
from PyQt6.QtGui import QIcon

# 获取图标路径
icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icons", "app.ico")

# 设置窗口图标
window.setWindowIcon(QIcon(icon_path))
```

## 添加新资源

如需添加新的资源文件，请按照以下步骤：

1. 在适当的子目录中放置文件
2. 更新本README文件，说明新资源的用途
3. 在代码中添加相应的引用

## 注意事项

- 请确保所有资源文件都有适当的许可证
- 图标文件应支持多种尺寸（16x16, 32x32, 48x48, 256x256）
- 避免使用过大的资源文件，以免影响应用程序启动速度