"""指标计算、混淆矩阵可视化（优化版）"""
import time
import os
import yaml
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay, classification_report
from src.common.logger import get_logger

# 读取配置
CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.yaml"
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
EVAL_CONFIG = config["evaluation"]

# 初始化日志
logger = get_logger(__name__)

# 非交互环境适配
plt.switch_backend('Agg')  # 服务器无GUI时使用

def evaluate_model(y_true, y_pre, save_path=None):
    """
    评估模型性能（自动保存+日志+非交互）
    :param y_true: 真实标签列表
    :param y_pre: 预测标签列表
    :param save_path: 混淆矩阵保存路径（None则自动生成）
    :return: 指标字典
    """
    # 校验输入长度
    if len(y_true) != len(y_pre):
        logger.error(f"真实标签条数({len(y_true)})与预测标签条数({len(y_pre)})不一致")
        raise ValueError("y_true and y_pre length mismatch")
    
    # 基本指标计算
    try:
        acc = accuracy_score(y_true, y_pre)
        precision = precision_score(y_true, y_pre, average='macro', zero_division=0)
        recall = recall_score(y_true, y_pre, average='macro', zero_division=0)
        f1 = f1_score(y_true, y_pre, average='macro', zero_division=0)
        
        logger.info(f"评估指标 | 准确率: {acc:.3f} | 精确率: {precision:.3f} | 召回率: {recall:.3f} | F1值: {f1:.3f}")
        
        # 分类报告
        report = classification_report(y_true, y_pre, target_names=EVAL_CONFIG["labels"], zero_division=0)
        logger.info(f"\n分类报告:\n{report}")
        print(report)  # 保留控制台输出
        
        # 混淆矩阵
        cm = confusion_matrix(y_true, y_pre, labels=EVAL_CONFIG["labels"])
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=EVAL_CONFIG["labels"])
        disp.plot(cmap='Blues', values_format='d')
        plt.title(f"Confusion Matrix ({time.strftime('%Y-%m-%d %H:%M:%S')})")
        
        # 自动生成保存路径
        if save_path is None:
            save_dir = Path(EVAL_CONFIG["confusion_matrix_dir"]).resolve()
            save_dir.mkdir(parents=True, exist_ok=True)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            save_path = save_dir / f"confusion_matrix_{timestamp}.png"
        
        # 保存图片
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        logger.info(f"混淆矩阵已保存至: {save_path}")
        
        # 本地调试时显示（交互模式）
        if EVAL_CONFIG["interactive"]:
            plt.show()
        
        # 关闭plt避免内存泄漏
        plt.close()
        
        metrics = {
            'accuracy': acc,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }
        return metrics
    except Exception as e:
        logger.error("评估模型失败", exc_info=True)
        raise

if __name__ == "__main__":
    # 示例测试
    y_true_example = ['positive', 'negative', 'neutral', 'positive', 'negative']
    y_pre_example = ['positive', 'neutral', 'neutral', 'positive', 'positive']
    evaluate_model(y_true_example, y_pre_example)