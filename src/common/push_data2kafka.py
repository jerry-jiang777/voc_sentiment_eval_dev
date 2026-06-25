"""Kafka数据推送模块（优化版）"""
import requests
import time
import yaml
from pathlib import Path
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from .logger import get_logger

# 读取配置
CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.yaml"
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
KAFKA_CONFIG = config["kafka"]

# 初始化日志
logger = get_logger(__name__)

@retry(
    stop=stop_after_attempt(KAFKA_CONFIG["push_retry"]),
    wait=wait_fixed(2),
    retry=retry_if_exception_type((requests.exceptions.ConnectionError, requests.exceptions.Timeout)),
    reraise=True
)
def push_data2kafka(data):
    """
    向Kafka推送数据（增加重试+日志+超时）
    :param data: 单条数据字典
    """
    url = KAFKA_CONFIG["push_url"]
    headers = {"Content-Type": "application/json"}
    body = [{
        "news_uuid": data['unique_id'],
        "article_id": data['unique_id'],
        "media_name": data['media_type'],
        "news_author": data['media_type'],
        "news_title": data['title'],
        "news_posttime": data['publish_time'],
        "news_url": data['url'],
        "news_content": data['content']
    }]

    try:
        response = requests.post(
            url,
            headers=headers,
            json=body,
            timeout=KAFKA_CONFIG["push_timeout"]
        )
        response.raise_for_status()  # 触发HTTP错误
        time.sleep(3)
        logger.info(f"数据 {data['unique_id']} 推送Kafka成功")
    except requests.exceptions.HTTPError as e:
        logger.error(f"数据 {data['unique_id']} 推送失败（HTTP错误）: {response.status_code} | {str(e)}")
        raise
    except requests.exceptions.ConnectionError as e:
        logger.error(f"数据 {data['unique_id']} 推送失败（连接错误）: {str(e)}")
        raise
    except requests.exceptions.Timeout as e:
        logger.error(f"数据 {data['unique_id']} 推送失败（超时）: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"数据 {data['unique_id']} 推送失败（未知错误）: {str(e)}", exc_info=True)
        raise