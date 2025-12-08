# 构建脚本
# 用于本地构建可执行文件

import os
import sys
import shutil
import subprocess
from datetime import datetime

def build_executable():
    """构建可执行文件"""
    print("开始构建可执行文件...")
    
    # 检查PyInstaller是否已安装
    try:
        import PyInstaller
        print("PyInstaller已安装")
    except ImportError:
        print("正在安装PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 清理之前的构建
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已清理目录: {dir_name}")
    
    # 运行PyInstaller构建
    print("正在运行PyInstaller...")
    subprocess.check_call([
        sys.executable, 
        "-m", 
        "PyInstaller", 
        "--clean",
        "--noconfirm",
        "FileDiffTools.spec"
    ])
    
    # 检查构建结果
    exe_path = os.path.join("dist", "FileDiffTools.exe")
    if os.path.exists(exe_path):
        print(f"构建成功! 可执行文件位于: {exe_path}")
        
        # 创建发布包
        create_release_package()
    else:
        print("构建失败!")
        return False
    
    return True

def create_release_package():
    """创建发布包"""
    print("正在创建发布包...")
    
    # 创建发布目录
    release_dir = "release"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    # 复制可执行文件
    shutil.copy("dist/FileDiffTools.exe", f"{release_dir}/FileDiffTools.exe")
    
    # 复制必要文件
    files_to_copy = [
        "README.md",
        "LICENSE",
        "CHANGELOG.md",
    ]
    
    for file_name in files_to_copy:
        if os.path.exists(file_name):
            shutil.copy(file_name, f"{release_dir}/{file_name}")
    
    # 复制资源文件夹
    dirs_to_copy = [
        "examples",
        "assets"
    ]
    
    for dir_name in dirs_to_copy:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, f"{release_dir}/{dir_name}")
    
    # 创建ZIP压缩包
    import zipfile
    version = datetime.now().strftime("%Y%m%d-%H%M")
    zip_name = f"FileDiffTools-{version}-windows.zip"
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, release_dir)
                zipf.write(file_path, arcname)
    
    print(f"发布包已创建: {zip_name}")
    print(f"发布目录: {release_dir}")

if __name__ == "__main__":
    success = build_executable()
    if success:
        print("\n构建完成!")
        print("您可以运行 dist/FileDiffTools.exe 来启动应用程序")
    else:
        print("\n构建失败!")
        sys.exit(1)