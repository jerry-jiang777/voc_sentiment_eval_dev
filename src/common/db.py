"""数据库连接模块（优化版）"""
import mysql.connector
from mysql.connector.cursor import MySQLCursorDict
from mysql.connector import errors
import yaml
from pathlib import Path
from .logger import get_logger

# 读取配置
CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.yaml"
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
MYSQL_CONFIG = config["mysql"]

# 初始化日志
logger = get_logger(__name__)

class MySQLConnector:
    def __init__(self):
        self.host = MYSQL_CONFIG["host"]
        self.user = MYSQL_CONFIG["user"]
        self.password = MYSQL_CONFIG["password"]
        self.database = MYSQL_CONFIG["database"]
        self.charset = MYSQL_CONFIG["charset"]
        self.connection = None
        self.cursor = None

    def connect(self):
        """连接数据库（增强异常处理）"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset=self.charset,
                autocommit=True
            )
            self.cursor = self.connection.cursor(dictionary=True)
            logger.info("数据库连接成功")
        except errors.ProgrammingError as e:
            logger.error(f"数据库连接失败（配置错误）: {str(e)}", exc_info=True)
            raise
        except errors.OperationalError as e:
            logger.error(f"数据库连接失败（网络/服务问题）: {str(e)}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"数据库连接未知错误: {str(e)}", exc_info=True)
            raise

    def close(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("数据库连接已关闭")

    def execute_query(self, item=None, query=None):
        """执行查询（增强日志+参数校验）"""
        if not self.cursor:
            raise RuntimeError("数据库未连接，请先调用connect()")
        
        try:
            if item:
                sql = "select * from dmc_voc_media_data where title = %s and url = %s"
                params = (item['title'], item['url'])
                logger.debug(f"执行查询: {sql} | 参数: {params}")
            elif query:
                sql = query
                params = ()
                logger.debug(f"执行自定义查询: {sql}")
            else:
                raise ValueError("必须提供item或query参数")
            
            self.cursor.execute(sql, params)
            results = self.cursor.fetchall()
            
            if not results and item:
                logger.warning(f"数据 {item['unique_id']} 未查询到预测结果")
            else:
                logger.info(f"查询到 {len(results)} 条结果")
            return results
        except errors.ProgrammingError as e:
            logger.error(f"SQL执行失败: {str(e)}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"查询未知错误: {str(e)}", exc_info=True)
            raise

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

if __name__ == "__main__":
    try:
        with MySQLConnector() as db:
            query = "SELECT * from dmc_voc_media_data limit 10;"
            results = db.execute_query(query=query)
            if results:
                for index, res in enumerate(results):
                    logger.info(f"第【{index + 1}】个结果: {res}")
    except Exception as e:
        logger.error(f"测试数据库连接失败: {str(e)}")