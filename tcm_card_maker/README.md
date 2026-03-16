# 🌿 Task 2 - 中医方剂卡片 maker

> 让 AI 为你创作一张美轮美奂的中医方剂卡片——从知识整理到图像生成，一气呵成

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Nano Banana Pro](https://img.shields.io/badge/Nano%20Banana%20Pro-Gemini%203%20Pro-green.svg)](https://nanobanana.ai/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 一句话说明

**这是一个 AI 卡片创作工具：输入一个中医方剂名称，AI 自动完成知识整理、Markdown 编写、JSON 提取，最终生成一张精美绝伦的中式风格卡片图像。**

就像有一位国画大师 + 中医教授为你打工，你只需告诉它「来一幅桂枝汤」，它就为你画出一张可以直接发朋友圈的专业卡片。

## 项目一页纸

![中医方剂卡片示例](./asset/introduction.png)

## 🎬 演示效果

![中医方剂卡片四宫格](./asset/cards_grid.png)

## 🚀 能做什么

| 场景 | 示例 |
|------|------|
| 📚 中医学习 | 生成「麻黄汤」「桂枝汤」等经典方剂的学习卡片 |
| 📖 教学备课 | 一键生成可供课堂展示的方剂图解 |
| 📱 社交分享 | 制作精美中医知识卡片发小红书/朋友圈 |

## 工作流程

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  ① 发散思考  │ → │  ② 整理Markdown │ → │  ③ 提取JSON │ → │  ④ AI绘图   │
│  方剂知识    │    │  结构化内容   │    │  数据字段   │    │  中式卡片   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## 📦 安装

```bash
# 1. 进入项目目录
cd tcm_card_maker/skill/tcm_card_maker

# 2. 创建虚拟环境
uv venv --python 3.11
source .venv/bin/activate

# 3. 安装依赖
pip install requests python-dotenv jinja2
```

## ⚡ 快速开始

### 方式一：使用 OpenClaw、claude code等召唤技能（推荐）

在 OpenClaw 中激活 `tcm-card-maker` 技能，直接对话式完成全流程：

```
用户：帮我制作一张「小青龙汤」的卡片
AI：  （自动完成知识整理→Markdown→JSON→图像生成）
```

### 方式二：手动运行脚本

```bash
# 1. 准备方剂 JSON 文件（需包含 formula_name 字段）
# 参考 skill/tcm_card_maker/references/json-schema.md

# 2. 运行图像生成脚本
python scripts/generate-image.py 你的方剂.json

# 3. 指定纵横比和分辨率（可选）
python scripts/generate-image.py 你的方剂.json 16:9 2K
```

### 参数说明

| 参数 | 默认值 | 可选值 |
|------|--------|--------|
| 纵横比 | 16:9 | 1:1, 16:9, 9:16, 4:3, 3:4, 21:9... |
| 分辨率 | 2K | 1K, 2K, 4K |

## 📋 输出示例

运行后会生成以下文件：

```
├── 桂枝汤_中医方剂卡片.png    # 生成的卡片图像
├── 桂枝汤_图像提示.txt        # 绘图提示文本
└── 桂枝汤_生成报告.txt        # 生成报告
```

## 📁 项目结构

```
tcm_card_maker/
├── skill/tcm_card_maker/
│   ├── SKILL.md              # 技能定义文件
│   ├── .env                  # API 配置
│   ├── assets/
│   │   └── image-prompt.j2   # 绘图提示模板
│   ├── references/
│   │   ├── markdown-structure.md  # Markdown 结构规范
│   │   └── json-schema.md          # JSON 字段规范
│   └── scripts/
│       └── generate-image.py       # 图像生成脚本
├── memory/                    # 技能记忆
├── asset/                    # 资源文件
└── test/                     # 测试用例
```

