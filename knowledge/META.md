# 知识库元数据（注入 system prompt）

admin 每次更新 B 或 C 后**必须**修改本文件。

| 字段 | 当前值 | 说明 |
|------|--------|------|
| `training_version` | `最新产品100问-2026-05-20` | B 培训文档版本（来源 PDF 拆分） |
| `qa_version` | `0.0.0-placeholder` | C 销冠 Q&A 版本号或日期 |
| `effective_date` | `2026-05-20` | 政策类信息生效参考日；**含历史价格，答复须标注以门店/官网为准** |
| `skill_spec_version` | `1.1.0` | 对齐 Product-Spec.md |

## 培训文档索引（B）

| 文件 | 内容 |
|------|------|
| `training/00-preface-fabg.md` | FABG 沟通方法前言 |
| `training/01-products.md` | 产品类 Q1–58 |
| `training/02-charging.md` | 充电类 Q59–62 |
| `training/03-purchase.md` | 购买类 Q63–74 等 |
| `training/04-safety.md` | 安全类 |
| `training/05-after-sales.md` | 售后类 |
| `training/06-hot-topics.md` | 舆论热点类 |
| `training/07-corporate-culture.md` | 企业文化 Q100 |
| `training/最新产品100问.pdf` | 原始 PDF（归档，运行时注入请用 `.md`） |

## 官方确认渠道（拒答时引导客户）

- 门店：请咨询您下单或看车的特斯拉门店
- 官方：特斯拉中国官网 / 小程序内官方入口（按运营填写）
