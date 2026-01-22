"""算法调用或者模拟算法（修复递归bug）"""
from src.common.logger import get_logger

logger = get_logger(__name__)

class SentimentClassifier:
    def __init__(self):
        # 模拟模型初始化（可替换为真实模型加载）
        logger.info("情感分类器初始化完成")

    def predict(self, texts):
        """
        对文本进行情感分类
        :param texts: list[str] 输入舆情文本
        :return: list[str] 输出预测标签 ["positive", "negative", "neutral"]
        """
        if not isinstance(texts, list):
            logger.error("输入texts必须是列表类型")
            raise TypeError("texts must be list of str")
        
        y_pred = []
        for text in texts:
            # 模拟预测逻辑（实际场景替换为真实模型推理）
            text_lower = text.lower()
            if "差评" in text_lower or "不好" in text_lower:
                pred = "negative"
            elif "好评" in text_lower or "不错" in text_lower:
                pred = "positive"
            else:
                pred = "neutral"
            y_pred.append(pred)
        
        logger.info(f"完成 {len(texts)} 条文本的情感预测")
        return y_pred

if __name__ == "__main__":
    # 测试
    classifier = SentimentClassifier()
    test_texts = ["这款产品很好用", "体验太差了", "一般般，没感觉"]
    res = classifier.predict(test_texts)
    logger.info(f"测试预测结果: {res}")