# B：培训文档目录

## 用途

存放**最新版**特斯拉培训材料（Markdown）。仅保留当前有效版本，不并行多版本。

## 更新流程

1. 运营提供 Word/PDF → 转为 `.md` 章节文件放入本目录  
2. 删除或覆盖旧文件  
3. 更新 `knowledge/META.md` 的 `training_version` 与 `effective_date`  
4. 通知宿主重新加载 Skill  

## 文件命名建议

- `products-model-y.md` — 车型与配置  
- `purchase-process.md` — 购车流程  
- `finance.md` — 金融方案（须含生效日期）  
- `charging.md` — 充电与家充  
- `after-sales.md` — 售后政策  

## 格式规范

- **文件类型**：仅 `.md`（UTF-8 纯文本 Markdown）
- **源材料**：Word / PDF / PPT 需先转成 Markdown（可用 Pandoc、飞书导出、或手工整理）
- **不要**直接把 PDF 丢进目录（当前 Skill 按文本注入，模型无法读 PDF）

完整字段说明与示例结构：复制 [`_template.md`](_template.md) 改名后填写。

## 当前内容

已由 `最新产品100问.pdf` 拆分为：

- `00-preface-fabg.md` … `07-corporate-culture.md`（共 112 条 Q&A 块）

重新拆分 PDF 时运行：

```bash
python scripts/pdf_to_training_md.py
```

（需先存在 `knowledge/training/_pdf_extract.txt`，可由 `pypdf` 从 PDF 生成。）

## 维护

更新 PDF 后：覆盖 `最新产品100问.pdf` → 重新运行脚本 → 更新 `knowledge/META.md`。
