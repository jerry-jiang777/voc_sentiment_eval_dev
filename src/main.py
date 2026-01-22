"""项目统一入口"""
from pathlib import Path
import yaml
from src.data_processing.get_origin_data import build_labels, read_excel, DATA_PROCESSING_MODE, DIRECT_EVALUATION_PATH
from src.evaluation.metrics import evaluate_model
from src.evaluation.nagtive_recall import calculate_negative_recall
from src.common.logger import get_logger

# 初始化日志
logger = get_logger(__name__)

# 读取配置 - 修正路径
CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"

# 检查配置文件是否存在
if not CONFIG_PATH.exists():
    # 如果标准路径不存在，则尝试相对路径查找
    CONFIG_PATH = Path("config.yaml").resolve()
    if not CONFIG_PATH.exists():
        # 如果还是找不到，使用默认配置
        DATA_PATH = Path("../data/prod_data.xlsx").resolve()  # 相对于src目录的路径
        DIRECT_EVALUATION_PATH = Path("../data/voc线上数据.xlsx").resolve()
        DATA_PROCESSING_MODE = "direct"
    else:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        # 使用项目根目录作为基准来构建数据路径
        PROJECT_ROOT = Path(__file__).resolve().parent.parent
        DATA_PATH = PROJECT_ROOT / config["data"]["prod_data_path"]
        DIRECT_EVALUATION_PATH = PROJECT_ROOT / config["data"]["direct_evaluation_path"]
        DATA_PROCESSING_MODE = config["evaluation"].get("data_processing_mode", "direct")
else:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    # 使用项目根目录作为基准来构建数据路径
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    DATA_PATH = PROJECT_ROOT / config["data"]["prod_data_path"]
    DIRECT_EVALUATION_PATH = PROJECT_ROOT / config["data"]["direct_evaluation_path"]
    DATA_PROCESSING_MODE = config["evaluation"].get("data_processing_mode", "direct")

def main():
    """主流程"""
    try:
        logger.info("===== 开始VOC情感算法评估 =====")
        
        # 根据配置选择数据处理模式
        logger.info(f"使用数据处理模式: {DATA_PROCESSING_MODE}")
        
        if DATA_PROCESSING_MODE == "direct":
            logger.info(f"读取直接评估数据文件: {DIRECT_EVALUATION_PATH}")
            y_true, y_pred = build_labels(DIRECT_EVALUATION_PATH, processing_mode="direct")
        else:  # sql_query 模式
            logger.info(f"读取原始数据文件: {DATA_PATH}")
            data = read_excel(DATA_PATH)
            y_true, y_pred = build_labels(DATA_PATH, processing_mode="sql_query")
        
        # 3. 打印基础信息
        logger.info(f"真实标签条数: {len(y_true)}")
        logger.info(f"预测标签条数: {len(y_pred)}")
        print(f"\n真实标签数据条数: {len(y_true)}")
        print(f"预测标签数据条数: {len(y_pred)}")
        
        # 4. 评估模型
        logger.info("开始计算评估指标...")
        evaluate_model(y_true, y_pred)
        
        # 5. 计算负面召回率
        logger.info("计算负面舆情召回率...")
        calculate_negative_recall(y_true, y_pred)
        
        logger.info("===== 评估完成 =====")
    except Exception as e:
        logger.error("评估流程执行失败", exc_info=True)
        raise

if __name__ == "__main__":
    main()