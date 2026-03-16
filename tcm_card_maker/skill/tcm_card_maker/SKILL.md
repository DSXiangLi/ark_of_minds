---
name: tcm-card-maker
description: 中医方剂卡片制作技能。用于创建中医方剂的markdown格式解读和基于内容的卡片绘图。当用户需要制作中医方剂卡片、解析方剂信息、生成结构化markdown内容、提取JSON数据或生成图像卡片时使用此技能。支持完整工作流：1)发散收集方剂信息，2)整理为结构化markdown，3)提取为JSON字段，4)使用Jinja模板生成绘图指令并调用nanobananapro模型。
---

# 中医方剂卡片制作技能

创建中医方剂的结构化markdown解读和基于内容的中式风格卡片图像。

## 工作流程

### 步骤1：发散思考（无需外部参考）
请基于你对于方剂的理解，全方位思考方剂相关的所有知识。

### 步骤2：整理为结构化markdown
当你梳理完和方剂相关的所有知识后，你需要读取把内容整理成结构化的md文件。

请先全面阅读[markdown-structure.md](references/markdown-structure.md)，了解：
- 完整的markdown结构规范
- 必选和可选章节要求
- **优化要点**：卡片空间有限，只放最经典、最有代表性的内容
  - ✅ 必须包含：经典配伍、核心病机、代表性用法（如麻黄汤喝后要和热粥）
  - ✅ 推荐包含：生动比喻、拟人化描述、特色配伍
  - ❌ 避免包含：泛泛的使用要点、普通临床应用、缺乏特色的注意事项
- **药物行动队优化**：要拟人化展示，与病机剧场形成联动

### 步骤3：提取JSON数据
**参考文件**：

当你把内容整理成结构化md文件后，你需要进一步把内容提炼成结构化的JSON文件。

请先全面阅读[json-schema.md](references/json-schema.md)，然后**直接通过语义理解从markdown内容中提取对应字段**。

你应该：
1. 理解markdown内容的结构和语义
2. 参考json-schema.md中的字段定义
3. 将markdown内容映射到对应的JSON字段
4. 输出完整的JSON数据

**注意**：这是语义提取任务，不需要外部脚本或工具。大模型具备直接解析和转换的能力。

### 步骤4：生成图像
**模板文件**：[image-prompt.j2](assets/image-prompt.j2) - 完整的绘图指令模板
**脚本文件**：
- [generate-image.py](scripts/generate-image.py) - 完整API调用脚本（需要Python依赖）

#### 方法一：使用完整Python脚本（推荐）
需要安装Python依赖：`requests`, `python-dotenv`, `jinja2`

```bash
# 安装依赖
pip install requests python-dotenv jinja2

# 生成图像
python scripts/generate-image.py <方剂JSON文件> [纵横比] [分辨率]

# 示例
python scripts/generate-image.py 理中丸.json 16:9 2K
```

#### 参数说明：
- **纵横比**：可选，默认16:9。支持1:1、16:9、9:16、4:3、3:4、21:9、3:2、2:3、5:4、4:5
- **分辨率**：可选，默认2K。支持1K、2K、4K

#### 脚本功能：
- 加载环境配置
- 使用模板渲染完整绘图指令
- 调用Nano Banana Pro (Gemini 3 Pro Image Preview) API生成图像
- 保存图像文件