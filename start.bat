@echo off
REM 文件差异比较工具启动脚本

echo 正在启动文件差异比较工具...

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未检测到Python，请先安装Python 3.7或更高版本
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 检查依赖包...
pip show PyQt6 >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装依赖包，请稍候...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo 错误: 依赖包安装失败，请检查网络连接或手动运行: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

REM 启动应用
echo 启动应用...
python main.py

REM 如果应用异常退出，暂停以查看错误信息
if %errorlevel% neq 0 (
    echo 应用异常退出，错误代码: %errorlevel%
    pause
)