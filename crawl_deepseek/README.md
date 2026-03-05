# 🤖 Task 1 - DeepSeek 自动问答爬虫

> 让 AI 自动帮你打开网页，打开搜索模式并提问 DeepSeek，并保存回答和引用链接

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Browser-Use](https://img.shields.io/badge/Browser--Use-0.12.0-green.svg)](https://github.com/browser-use/browser-use)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 一句话说明

**这是一个自动化工具：你问问题，AI 去 DeepSeek 搜索答案，自动保存为 JSON 文件。**

就像有一个助手帮你去 DeepSeek 网站提问，然后把答案整理好放进文件里——你只需要告诉它问什么。

## 项目一页纸

![和AI不算peace的首次合作](./asset/introduction.png)

## 🎬 演示视频

https://github.com/user-attachments/assets/046b79fa-3998-4389-bcb4-d5ec1307e224

## 🚀 能做什么

| 场景 | 示例 |
|------|------|
| 📊 批量调研 | 一次提问 10 个关于"天弘基金"的问题 |
| 📰 新闻汇总 | 自动获取最新科技新闻并整理 |

## 📦 安装

```bash
# 1. 克隆项目
cd auto_crawl_v2

# 2. 创建虚拟环境
uv venv --python 3.11
source .venv/bin/activate

# 3. 安装依赖
uv sync

# 4. 配置 API Key
cp .env.example .env
# 编辑 .env，填入你的 API Key
```

## ⚡ 快速开始

### 方式一：问一个问题

```bash
python -m src.main -q "今天北京天气怎么样？"
```

### 方式二：批量提问

创建 `queries.json` 文件：

```json
[
  {"query": "今天天气怎么样？"},
  {"query": "2026年最新科技新闻有哪些？"},
  {"query": "Python和JavaScript哪个更适合初学者？"}
]
```

运行：

```bash
python -m src.main -f queries.json
```

## 📋 输出示例

运行后会在当前目录生成 JSON 文件：

```json
{
  "answer": "已阅读 8 个网页\n\n今天（3月2日）北京天气阴冷，大部分地区会有小雪或雨夹雪...",
  "references": [
    {"title": "weather.com.cn", "url": "https://www.weather.com.cn/..."},
    {"title": "nmc.cn", "url": "https://nmc.cn/publish/forecast/..."},
    {"title": "sohu.com", "url": "https://www.sohu.com/a/..."}
  ]
}
```

- `answer`: AI 的完整回答
- `references`: 回答中引用的网页链接

## 🔧 配置说明

### 环境变量 (.env)

```env
# 阿里云 Qwen VL 模型（推荐）
QWEN_VL_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
QWEN_VL_KEY=你的API密钥
```

### 登录状态

首次运行需要登录 DeepSeek，之后会自动保存登录状态（cookies），下次无需再登录。

## 📁 项目结构

```
auto_crawl_v2/
├── src/
│   ├── main.py      # 入口程序
│   ├── agent.py     # Agent 核心逻辑
│   └── tools.py     # 工具函数（保存 JSON）
├── tests/           # 测试用例
├── logs/            # 运行日志
└── *.json          # 输出的结果文件
```

## 🐛 常见问题

**Q: 运行时浏览器卡住了怎么办？**
> 按 `Ctrl+C` 终止，程序会自动清理。

**Q: 提取的内容不完整怎么办？**
> 检查网络是否稳定，DeepSeek 响应时间可能较长。

**Q: 如何查看详细日志？**
> 查看 `logs/` 目录下的日志文件。

