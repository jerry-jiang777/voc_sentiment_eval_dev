"""负面舆情召回率计算（优化版）"""
from sklearn.metrics import recall_score
from src.common.logger import get_logger

logger = get_logger(__name__)

def calculate_negative_recall(y_true, y_pre, negative_label='negative', verbose=True):
    """
    计算负面舆情的召回率
    :param y_true: 真实标签列表
    :param y_pre: 预测标签列表
    :param negative_label: 负面标签名称
    :param verbose: 是否控制台打印
    :return: 负面召回率
    """
    try:
        # 校验负面标签是否存在
        if negative_label not in y_true:
            logger.warning(f"真实标签中无{negative_label}标签，召回率为0")
            negative_recall = 0.0
        else:
            negative_recall = recall_score(
                y_true, y_pre, 
                labels=[negative_label], 
                average='macro',
                zero_division=0
            )
        
        logger.info(f"负面舆情召回率: {negative_recall:.3f}")
        if verbose:
            print(f"负面舆情召回率: {negative_recall:.3f}")
        
        return negative_recall
    except Exception as e:
        logger.error("计算负面召回率失败", exc_info=True)
        raise

if __name__ == "__main__":
    # 示例测试
    y_true_example = ['positive', 'negative', 'neutral', 'negative', 'positive']
    y_pre_example = ['positive', 'neutral', 'neutral', 'negative', 'positive']
    calculate_negative_recall(y_true_example, y_pre_example)