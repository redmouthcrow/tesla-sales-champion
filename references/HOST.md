# 宿主集成说明（微信小程序后端）

本文档供**组装模型请求**的开发者使用。Skill 不实现 HTTP、会话存储或微信 API。

## 推荐请求结构

```json
{
  "model": "deepseek-chat",
  "messages": [
    {
      "role": "system",
      "content": "<SYSTEM_PROMPT 见下文>"
    },
    {
      "role": "user",
      "content": "客户当前问题"
    }
  ],
  "temperature": 0.3
}
```

多轮时，在 `user` 消息之前按时间顺序插入历史 `user` / `assistant` 对（由宿主从会话存储加载）。

## 组装 SYSTEM_PROMPT

建议按顺序拼接（均为 UTF-8 文本）：

1. **全文**：`SKILL.md` 正文（可去掉 YAML frontmatter）
2. **元数据**：`knowledge/META.md` 全文
3. **检索片段**（二选一）：
   - **小库**：将相关 `knowledge/training/*.md` 与 `knowledge/champion-qa/*.md` 片段拼入（注意 token 上限）
   - **大库**：宿主先做 RAG，将 Top-K 片段以 `## 检索到的知识` 标题追加

### 模板

```markdown
<SKILL.md 正文>

---

## 知识库版本

<META.md 内容>

---

## 检索到的知识

### [B] training/xxx.md
<片段>

### [C] champion-qa/yyy.md
<片段>
```

## 检索建议

| 库体量 | 策略 |
|--------|------|
| B+C 合计 < 80k 字符 | 可按问题关键词选文件全文注入 |
| 较大 | 对 B、C 分库 embedding；检索时 **C 权重 ≥ B**（例如 C Top-5 + B Top-3） |

检索 query：当前用户消息 +（可选）最近 1 轮用户发言。

## 模型参数建议

| 参数 | 建议 | 说明 |
|------|------|------|
| `temperature` | 0.2–0.4 | 降低政策类幻觉 |
| `max_tokens` | ≥ 1024 | 多意图分点作答 |
| 历史轮数 | 宿主自定 | 建议最近 10 轮或按 token 截断 |

## 响应处理

- 直接将模型 `assistant` 正文展示给客户（小程序 UI）
- **无需**解析 JSON；本 Skill 不要求结构化输出
- 若需日志，可记录本次注入的 `training_version` / `qa_version`（来自 META.md）

## 错误与降级

| 情况 | 建议 |
|------|------|
| 模型超时 | 返回「服务繁忙，请稍后重试」 |
| 知识库目录缺失 | 勿调用模型；告警并返回维护提示 |
| Skill 版本变更 | 宿主缓存需失效或带版本号热更新 |

## 文件清单

加载本 Skill 时至少需要：

```
SKILL.md
knowledge/META.md
knowledge/training/   # 至少一个 .md
knowledge/champion-qa/  # 至少一个 .md
```

可选：`references/HOST.md`（给人读，不必注入模型）。
