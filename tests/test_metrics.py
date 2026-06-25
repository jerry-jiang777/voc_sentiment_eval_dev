"""评估模块单元测试"""
import pytest
from src.evaluation.metrics import evaluate_model
from src.evaluation.negtive_recall import calculate_negative_recall

def test_evaluate_model():
    """测试指标计算"""
    y_true = ['positive', 'negative', 'neutral']
    y_pre = ['positive', 'negative', 'neutral']
    metrics = evaluate_model(y_true, y_pre)
    assert metrics['accuracy'] == 1.0
    assert metrics['precision'] == 1.0

def test_negative_recall():
    """测试负面召回率"""
    y_true = ['negative', 'negative', 'positive']
    y_pre = ['negative', 'neutral', 'positive']
    recall = calculate_negative_recall(y_true, y_pre, verbose=False)
    assert recall == 0.5