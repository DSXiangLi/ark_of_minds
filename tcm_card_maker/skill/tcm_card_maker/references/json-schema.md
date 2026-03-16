# JSON Schema规范

## 使用说明

**重要**：此文件为**语义提取指导文档**，供大模型参考使用。大模型应通过语义理解从markdown内容中提取对应字段，**不需要编写或运行任何脚本**。

## 完整JSON结构

```json
{
  "formula_name": "方剂名称",
  "subtitle": "副标题",
  "formula_type": "方剂类型",
  "herbs": ["药材1", "药材2"],
  "core_rhyme": "核心口诀",
  "indications": {
    "main_symptoms": ["症状1", "症状2"],
    "additional_symptoms": ["兼证"]
  },
  "pathogenesis_theater": {
    "title": "病机剧场标题",
    "description": "病机剧场描述"
  },
  "herb_actions": [
    {
      "group": "组名",
      "herbs": ["药材"],
      "action": "作用",
      "analogy": "类比"
    }
  ],
  "symptom_herb_links": [
    {
      "symptom": "症状",
      "herb": "药材",
      "action": "作用"
    }
  ],
  "clinical_reminders": {
    "scenarios": ["适用场景"],
    "usage_tips": "使用要点"
  },
  "classical_text": "经典原文",
  "optional_sections": {
    "usage_rules": "使用铁律",
    "pathogenesis_evolution": "病机演变",
    "compatibility_insights": "配伍点睛",
    "modifications": "兼证加减",
    "usage_points": "用法要点"
  }
}
```

## 字段提取规则

### 从markdown提取对应关系

| Markdown模式 | JSON字段 | 提取方法 |
|-------------|----------|----------|
| `## 方剂名称` | `formula_name` | 提取`## `后的内容 |
| `**名称 · 描述的"类型"方**` | `subtitle` | 提取`**`之间的内容 |
| 同上 | `formula_type` | 提取`的"`和`"方`之间的内容 |
| `[药物手绘组合：药材]` | `herbs` | 提取`：`后的内容，用顿号分割 |
| `**核心口诀**`后的引号内容 | `core_rhyme` | 提取`"`之间的内容 |
| `主治：`后的数字列表项 | `indications.main_symptoms` | 提取`1. `、`2. `等开头的行 |
| `主治：`后的项目符号项 | `indications.additional_symptoms` | 提取`- `开头的行 |
| `病机剧场 · 标题` | `pathogenesis_theater.title` | 提取`· `后的内容 |
| 病机剧场描述内容 | `pathogenesis_theater.description` | 提取标题后的所有内容 |
| `**药物行动队**`后的列表项 | `herb_actions` | 解析格式：`- **组名**：药材，作用。如同**类比**。` |
| `**症状-药物连线**`后的列表项 | `symptom_herb_links` | 解析格式：`- 症状 ← 药材 (作用)` |
| `- **场景**：**疾病**` | `clinical_reminders.scenarios` | 提取`**`之间的内容，用顿号分割 |
| `- **用法**：`或`- **注意**：` | `clinical_reminders.usage_tips` | 提取`：`后的内容 |
| `**经典原文**`后的`>`内容 | `classical_text` | 提取所有`>`开头的行 |

### 可选章节提取

| Markdown章节 | JSON字段 | 提取内容 |
|-------------|----------|----------|
| `**使用铁律**` | `optional_sections.usage_rules` | 提取所有内容 |
| `### **病机演变**` | `optional_sections.pathogenesis_evolution` | 提取所有内容 |
| `**配伍点睛**：` | `optional_sections.compatibility_insights` | 提取`：`后的加粗内容 |
| `**兼证加减**：` | `optional_sections.modifications` | 提取所有内容 |
| `- **用法要点**：` | `optional_sections.usage_points` | 提取`：`后的内容 |

## 提取示例

### 简单字段提取
Markdown:
```
## 理中丸
**理中汤 · 中焦虚寒的"暖炉"方**
```

JSON:
```json
{
  "formula_name": "理中丸",
  "subtitle": "理中汤 · 中焦虚寒的\"暖炉\"方",
  "formula_type": "暖炉"
}
```

### 复杂字段提取
Markdown:
```
**药物行动队**

- **点火升温组**：干姜，辛热，温中散寒。如同**加大火力**。

**症状-药物连线**

- 脘腹冷痛 ← 干姜 (温中散寒)
```

JSON:
```json
{
  "herb_actions": [
    {
      "group": "点火升温组",
      "herbs": ["干姜"],
      "action": "辛热，温中散寒",
      "analogy": "加大火力"
    }
  ],
  "symptom_herb_links": [
    {
      "symptom": "脘腹冷痛",
      "herb": "干姜",
      "action": "温中散寒"
    }
  ]
}
```

## 完整JSON示例

```json
{
  "formula_name": "理中丸",
  "subtitle": "理中汤 · 中焦虚寒的\"暖炉\"方",
  "formula_type": "暖炉",
  "herbs": ["干姜", "人参", "白术", "炙甘草"],
  "core_rhyme": "理中汤主理中乡，甘草人参术干姜；呕利腹痛阴寒盛，温中祛寒补脾阳。",
  "indications": {
    "main_symptoms": [
      "脘腹冷痛：腹部绵绵作痛，喜温喜按，遇寒加重。",
      "呕吐下利：呕吐清水或食物，大便稀溏，完谷不化。"
    ],
    "additional_symptoms": []
  },
  "pathogenesis_theater": {
    "title": "寒冬里的老旧锅炉房",
    "description": "[场景图：寒冬腊月，一座老旧锅炉房（脾胃）内，炉火微弱（阳气不足）...]"
  },
  "herb_actions": [
    {
      "group": "点火升温组",
      "herbs": ["干姜"],
      "action": "辛热，直入脾胃，温中散寒，助阳化气",
      "analogy": "加大火力，重燃炉膛"
    }
  ],
  "symptom_herb_links": [
    {
      "symptom": "脘腹冷痛、喜温喜按",
      "herb": "干姜",
      "action": "温中散寒"
    }
  ],
  "clinical_reminders": {
    "scenarios": ["慢性胃炎", "消化性溃疡"],
    "usage_tips": "丸剂缓图，汤剂急用。"
  },
  "classical_text": "\"大病差后，喜唾，久不了了，胸上有寒，当以丸药温之，宜理中丸。\" —— 张仲景《伤寒论》"
}
```

## 注意事项

1. **字段验证**：检查必填字段是否齐全
2. **数据清洗**：去除多余空格和换行
3. **特殊字符**：正确转义引号等字符
4. **数组处理**：确保是有效的JSON数组
5. **可选字段**：不存在时可以不包含或为空

## 使用建议

1. **顺序提取**：按markdown章节顺序处理
2. **正则匹配**：使用模式匹配提取内容
3. **错误处理**：处理缺失或异常数据
4. **结果验证**：验证JSON结构的有效性

**返回SKILL.md继续工作流程**
