"""统一日志配置模块"""
import logging
import os
import yaml
from pathlib import Path

# 读取配置文件 - 修正路径
CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config.yaml"

# 检查配置文件是否存在
if not CONFIG_PATH.exists():
    # 如果标准路径不存在，则尝试相对路径查找
    CONFIG_PATH = Path("config.yaml").resolve()
    if not CONFIG_PATH.exists():
        # 如果还是找不到，使用默认配置
        LOG_LEVEL = "INFO"
        LOG_FILE = "logs/app.log"
    else:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        LOG_LEVEL = config["logger"]["level"]
        LOG_FILE = config["logger"]["log_file"]
else:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    LOG_LEVEL = config["logger"]["level"]
    LOG_FILE = config["logger"]["log_file"]

def get_logger(name: str) -> logging.Logger:
    """
    获取配置好的logger实例
    :param name: 日志命名空间（通常为__name__）
    :return: 配置后的logger
    """
    # 避免重复添加处理器
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    
    logger.setLevel(LOG_LEVEL)
    logger.propagate = False

    # 确保日志目录存在
    log_dir = os.path.dirname(LOG_FILE)
    os.makedirs(log_dir, exist_ok=True)

    # 格式配置
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    )

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 文件处理器
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger