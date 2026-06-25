# VOC 情感分类算法评估项目

本项目用于评估 AIVOC 情感分类算法效果，支持从 Excel 数据中构建真实标签和预测标签，并基于 scikit-learn 输出分类评估指标、混淆矩阵和负面舆情召回率。

## 核心功能

- 读取 VOC 情感分类评估数据
- 支持直接评估模式和 SQL 查询评估模式
- 标准化中文、英文情感标签
- 计算准确率、精确率、召回率、F1 值
- 输出分类报告和混淆矩阵图片
- 单独计算负面舆情召回率
- 统一记录运行日志

## 项目结构

```text
voc_sentiment_eval_dev/
├── config.yaml                 # 项目配置文件：数据路径、日志、评估参数等
├── requirements.txt            # Python 依赖清单
├── run.py                      # 推荐运行入口
├── README.md                   # 项目说明文档
├── data/                       # 数据文件目录
│   ├── prod_data.xlsx          # 原始生产数据示例
│   ├── voc线上数据.xlsx         # 直接评估数据示例
│   └── get_data.py             # 数据获取相关脚本
├── src/                        # 核心源码目录
│   ├── main.py                 # 主流程入口
│   ├── algorithm/              # 算法相关模块
│   │   └── sentiment_model.py
│   ├── common/                 # 公共能力模块
│   │   ├── db.py               # MySQL 连接与查询
│   │   ├── logger.py           # 日志配置
│   │   └── push_data2kafka.py  # Kafka 数据推送
│   ├── data_processing/        # 数据处理模块
│   │   └── get_origin_data.py  # Excel 读取与标签构建
│   └── evaluation/             # 评估模块
│       ├── metrics.py          # 分类指标与混淆矩阵
│       └── nagtive_recall.py   # 负面舆情召回率
├── results/                    # 评估结果输出目录
│   └── confusion_matrix/       # 混淆矩阵图片
├── logs/                       # 运行日志目录
└── tests/                      # 单元测试目录
```

## 环境要求

- Python 3.8+
- pip 或 conda
- 可读取 `.xlsx` 文件的运行环境

## 安装依赖

建议先创建独立虚拟环境，再安装依赖：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell 可使用：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 配置说明

项目通过根目录下的 `config.yaml` 统一管理配置，主要包含以下配置项：

```yaml
data:
  prod_data_path: "data/prod_data.xlsx"
  direct_evaluation_path: "data/voc线上数据.xlsx"

logger:
  level: "INFO"
  log_file: "logs/app.log"

evaluation:
  labels: ["negative", "positive", "neutral"]
  confusion_matrix_dir: "results/confusion_matrix"
  interactive: false
  data_processing_mode: "direct"
```

关键配置说明：

- `data.prod_data_path`：SQL 查询模式使用的原始数据文件路径
- `data.direct_evaluation_path`：直接评估模式使用的数据文件路径
- `logger.log_file`：运行日志输出路径
- `evaluation.labels`：分类标签集合
- `evaluation.confusion_matrix_dir`：混淆矩阵图片保存目录
- `evaluation.interactive`：是否显示图形窗口，服务器或 CI 环境建议设置为 `false`
- `evaluation.data_processing_mode`：数据处理模式，可选 `direct` 或 `sql_query`

## 数据格式

### direct 模式

`direct` 是当前默认模式，适用于 Excel 中已经包含真实标签和预测标签的场景。

Excel 至少需要包含以下两列：

| 字段名 | 含义 |
| --- | --- |
| `voc_tendencies_manually` | 人工标注的真实情感标签 |
| `voc_tendencies` | 算法预测的情感标签 |

支持的标签值会被统一转换为：

| 标准标签 | 支持示例 |
| --- | --- |
| `negative` | `negative`、`neg`、`负面`、`消极`、`负向` |
| `positive` | `positive`、`pos`、`正面`、`积极`、`正向` |
| `neutral` | `neutral`、`neu`、`中性`、`中立` |

无法识别的标签会被记录到日志，并默认转换为 `neutral`。

### sql_query 模式

`sql_query` 模式适用于需要先将原始数据推送到 Kafka，再从数据库查询算法预测结果的场景。

该模式依赖：

- `config.yaml` 中的 MySQL 配置
- `config.yaml` 中的 Kafka 推送配置
- 原始数据中存在 `unique_id` 字段
- 原始数据中存在 `voc_tendencies_manually` 字段

## 运行项目

推荐从项目根目录运行：

```bash
python run.py
```

也可以直接运行主入口：

```bash
python src/main.py
```

运行流程：

1. 读取 `config.yaml`
2. 根据 `evaluation.data_processing_mode` 选择数据处理模式
3. 构建 `y_true` 和 `y_pred`
4. 计算分类指标
5. 生成混淆矩阵图片
6. 计算负面舆情召回率
7. 写入运行日志

## 输出结果

运行完成后会产生以下输出：

- 控制台输出真实标签条数、预测标签条数、分类报告和负面召回率
- 日志文件：`logs/app.log`
- 混淆矩阵图片：`results/confusion_matrix/confusion_matrix_YYYYMMDD_HHMMSS.png`

## 运行测试

如需执行单元测试，可运行：

```bash
pytest tests
```

## 注意事项

- 提交到 GitHub 前，请确认 `config.yaml` 中不包含真实数据库账号、密码、内网地址或其他敏感信息。
- `data/` 目录可能包含业务数据，提交前请确认数据是否允许公开。
- `logs/` 和 `results/` 通常属于运行产物，可根据团队规范决定是否提交。
- 当前评估标签顺序为 `negative`、`positive`、`neutral`，如需调整，请同步修改 `config.yaml` 中的 `evaluation.labels`。
