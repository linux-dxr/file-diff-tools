# 文件差异比较工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![PyQt Version](https://img.shields.io/badge/PyQt-6.0%2B-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)

一个基于PyQt6开发的图形界面工具，用于比较Excel、CSV和TXT文件之间的差异。

## 功能特点

- 📊 支持多种文件格式：Excel (.xlsx, .xls)、CSV (.csv)、TXT (.txt)
- 🔄 两种比较模式：文件比较模式和Sheet比较模式
- 🔑 可自定义关键列和分隔符
- 📝 生成详细的差异报告
- 🎨 现代化的用户界面设计
- ⚡ 多线程处理，避免界面卡顿
- 🌍 跨平台支持（Windows、macOS、Linux）

## 截图

![应用截图](docs/screenshot.png)

## 安装

### 环境要求

- Python 3.7+
- PyQt6
- pandas
<<<<<<< HEAD
=======
- openpyxl (用于Excel文件处理)
>>>>>>> 1aa9785be6cadf7180d6c1289a64c5870dc63e5f

### 安装方法

#### 方法1：克隆仓库（推荐）

```bash
git clone https://github.com/yourusername/file-diff-tools.git
cd file-diff-tools
pip install -r requirements.txt
```

#### 方法2：直接下载

1. 下载最新版本的压缩包
2. 解压到任意目录
3. 安装依赖：`pip install -r requirements.txt`

## 使用方法

### 方法1：使用启动脚本（推荐）

**Windows用户：**
双击 `start.bat` 文件即可启动应用程序。

<<<<<<< HEAD
=======
**Linux/macOS用户：**
```bash
chmod +x start.sh
./start.sh
```
>>>>>>> 1aa9785be6cadf7180d6c1289a64c5870dc63e5f

### 方法2：使用Python脚本

```bash
python main.py
```

### 方法3：直接运行GUI模块

```bash
python file_diff_gui.py
```

## 使用说明

### 文件比较模式

1. 选择"文件比较模式"
2. 选择要比较的两个文件
3. 输入用于匹配行的关键列名
4. 根据文件类型设置分隔符（CSV和TXT文件需要）
5. 选择是否生成差异报告
6. 点击"开始比较"按钮

### Sheet比较模式

1. 选择"Sheet比较模式"
2. 选择第一个文件（可以是Excel文件中的任意Sheet）
3. 选择包含多个Sheet的Excel文件
4. 从下拉菜单中选择要比较的两个Sheet
5. 输入用于匹配行的关键列名
6. 点击"开始比较"按钮

## 比较结果

比较完成后，可以在"比较结果"选项卡中查看：

- ✅ 完全一致的行数
- ❌ 有差异的行数
- ➕ 仅在数据源1中存在的行数
- ➖ 仅在数据源2中存在的行数
- 📋 详细的差异数据

如果选择了生成差异报告，报告将保存在指定路径或自动生成的路径中。

## 示例

### 示例1：比较两个Excel文件

```python
from file_diff import two_file_diff

# 比较两个Excel文件
result = two_file_diff(
    file1_path="data1.xlsx",
    file2_path="data2.xlsx",
    key_column="ID",
    output_report=True,
    report_path="diff_report.csv"
)

print(f"完全一致的行数: {len(result['identical'])}")
print(f"有差异的行数: {len(result['mismatch'])}")
```

### 示例2：比较同一Excel文件中的两个Sheet

```python
from file_diff import two_file_diff

# 比较同一Excel文件中的两个Sheet
result = two_file_diff(
    compare_mode="sheet",
    file_path_for_sheet="data.xlsx",
    sheet1="Sheet1",
    sheet2="Sheet2",
    key_column="ID",
    output_report=True
)
```

### 示例3：比较两个CSV文件

```python
from file_diff import two_file_diff

# 比较两个CSV文件
result = two_file_diff(
    file1_path="data1.csv",
    file2_path="data2.csv",
    key_column="ID",
    file_type="csv",
    delimiter=",",
    output_report=True
)
```

## 注意事项

- 比较时需要确保两个数据源都包含指定的关键列
- Sheet比较模式仅支持Excel文件
- 报告文件使用CSV格式，但包含注释信息
- 比较大文件时可能需要一些时间，请耐心等待

## 技术实现

本工具基于以下技术：

- **PyQt6**: 用于构建图形用户界面
- **pandas**: 用于数据处理和比较
<<<<<<< HEAD
=======
- **openpyxl**: 用于Excel文件读写
>>>>>>> 1aa9785be6cadf7180d6c1289a64c5870dc63e5f
- **多线程**: 使用QThread避免界面卡顿

## 构建和发布

### 从源代码构建

如果您想从源代码构建可执行文件：

1. **安装构建依赖**:
<<<<<<< HEAD

   ```bash
   pip install pyinstaller
   ```
2. **运行构建脚本**:

   ```bash
   python build.py
   ```
3. **获取可执行文件**:

=======
   ```bash
   pip install pyinstaller
   ```

2. **运行构建脚本**:
   ```bash
   python build.py
   ```

3. **获取可执行文件**:
>>>>>>> 1aa9785be6cadf7180d6c1289a64c5870dc63e5f
   - Windows可执行文件位于 `dist/FileDiffTools.exe`
   - 发布包位于 `FileDiffTools-YYYYMMDD-HHMM-windows.zip`

### 手动使用PyInstaller

您也可以直接使用PyInstaller构建：

```bash
# 使用spec文件构建（推荐）
pyinstaller FileDiffTools.spec

# 或者使用命令行参数
pyinstaller --onefile --windowed --icon=assets/icons/app.ico --name="FileDiffTools" main.py
```

### 自动构建和发布

项目使用GitHub Actions进行自动构建和发布：

- **持续集成**: 每次推送到main或develop分支时运行测试
- **自动发布**: 创建新的标签（如v1.0.0）时自动构建并发布可执行文件

发布流程：
<<<<<<< HEAD

1. 创建并推送标签:

=======
1. 创建并推送标签:
>>>>>>> 1aa9785be6cadf7180d6c1289a64c5870dc63e5f
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
<<<<<<< HEAD
2. GitHub Actions将自动：

=======

2. GitHub Actions将自动：
>>>>>>> 1aa9785be6cadf7180d6c1289a64c5870dc63e5f
   - 构建Windows可执行文件
   - 创建发布包
   - 上传到GitHub Releases

### 下载预构建版本

您可以从GitHub Releases页面下载预构建的可执行文件，无需安装Python环境。

## 开发

### 环境设置

1. **克隆仓库**:
<<<<<<< HEAD

=======
>>>>>>> 1aa9785be6cadf7180d6c1289a64c5870dc63e5f
   ```bash
   git clone https://github.com/your-username/file-diff-tools.git
   cd file-diff-tools
   ```
<<<<<<< HEAD
2. **创建虚拟环境**:

=======

2. **创建虚拟环境**:
>>>>>>> 1aa9785be6cadf7180d6c1289a64c5870dc63e5f
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```
<<<<<<< HEAD
3. **安装依赖**:

=======

3. **安装依赖**:
>>>>>>> 1aa9785be6cadf7180d6c1289a64c5870dc63e5f
   ```bash
   pip install -r requirements.txt
   ```

### 运行测试

```bash
# 运行所有测试
python test.py

# 或者使用pytest（如果已安装）
pytest
```

### 贡献

欢迎贡献代码！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细信息。

## 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 更新日志

<<<<<<< HEAD
### v1.0.0 (2025-12-08)
=======
### v1.0.0 (2024-01-01)
>>>>>>> 1aa9785be6cadf7180d6c1289a64c5870dc63e5f

- 初始版本发布
- 支持Excel、CSV、TXT文件比较
- 实现文件比较模式和Sheet比较模式
- 添加差异报告生成功能
- 实现图形用户界面

## 许可证

本项目采用 [MIT许可证](LICENSE)。

## 联系方式

<<<<<<< HEAD
- 项目主页: https://github.com/linux-dxr/file-diff-tools
- 问题反馈: https://github.com/linux-dxr/file-diff-tools/issues
- 邮箱: d19091730135@gmail.com

## 致谢

感谢所有为本项目做出贡献的开发者和用户！
=======
- 项目主页: https://github.com/yourusername/file-diff-tools
- 问题反馈: https://github.com/yourusername/file-diff-tools/issues
- 邮箱: your.email@example.com

## 致谢

感谢所有为本项目做出贡献的开发者和用户！
>>>>>>> 1aa9785be6cadf7180d6c1289a64c5870dc63e5f
