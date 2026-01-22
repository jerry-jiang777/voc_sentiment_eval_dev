# VOC 情感分类算法评估项目
用于评估AIVOC情感分类算法的效果，基于scikit-learn实现指标计算、混淆矩阵可视化等功能。

## 项目结构
voc_sentiment_eval/
├── config.yaml # 统一配置文件（数据库、Kafka、路径等）
├── requirements.txt # 依赖清单
├── src/ # 核心源码
│ ├── main.py # 项目入口
│ ├── common/ # 公共模块（日志、数据库、Kafka 推送）
│ ├── algorithm/ # 算法相关
│ ├── data_processing/ # 数据处理（读取、标签构建）
│ └── evaluation/ # 评估模块（指标计算、负面召回率）
├── data/ # 原始数据目录
├── results/ # 评估结果（混淆矩阵图片）
├── logs/ # 运行日志
└── tests/ # 单元测试



## 环境搭建
1. 安装Python 3.8+
2. 安装依赖：
   ```bash
   pip install -r requirements.txt

# 直接运行入口文件
python src/main.py

# 或通过run.py运行
python run.py
