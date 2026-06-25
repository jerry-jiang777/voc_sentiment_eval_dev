"""快捷运行入口"""
import os
from pathlib import Path
from src.main import main

# 设置工作目录为项目根目录
project_root = Path(__file__).resolve().parent
os.chdir(project_root)

if __name__ == "__main__":
    main()