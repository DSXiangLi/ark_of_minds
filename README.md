# 🧠 Ark of Minds

<div align="center">

**AI Coding能做什么？要试过才知道**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![AI](https://img.shields.io/badge/AI-Applications-green.svg)](https://github.com/)

</div>

---

## ✨ 应用列表

### 🕷️ [Task1：crawl_deepseek](./crawl_deepseek)

<div align="center">

![DeepSeek 爬虫应用](./crawl_deepseek/asset/introduction.png)

**DeepSeek数据爬虫与处理工具** - 批量去网页版DeepSeek提问并获取答案和搜索链接

**可解锁技能点：open code，browser-use，单智能体，Agents.md**

[查看文档 →](./crawl_deepseek/README.md)

[📖 博客：和AI一起搞事情#1 - opencode ×browser-use实战复盘](https://cloud.tencent.com/developer/article/2634586)

</div>

### 🌿 [Task2：tcm_card_maker](./tcm_card_maker)

<div align="center">

![中医方剂卡片](./tcm_card_maker/asset/introduction.png)

**AI 中医方剂卡片生成器** - 输入方剂名称，AI 自动完成知识整理并生成精美中式卡片图像

**可解锁技能点：OpenClaw，技能开发，AI绘图，图像生成**

[查看文档 →](./tcm_card_maker/README.md)

[📖 博客：和AI一起搞事情#2 - 边剥龙虾&边做个中医方剂技能](https://cloud.tencent.com/developer/article/2642702)

</div>

### 🏮 [Task3：formula_odyssey](./formula_odyssey) ⚠️ 已废弃

<div align="center">

![公式奥德赛](./formula_odyssey/assets/introduction.png)

**AI 中医方剂文字冒险游戏** - 探索中医方剂世界的沉浸式文字冒险游戏（探索性失败案例）

**可解锁技能点：AI游戏设计，文字冒险，交互式AI**

[查看文档 →](./formula_odyssey/README.md)

[📖 博客：和AI一起搞事情#3 - Claude Teammate 开发中医游戏翻车了](https://cloud.tencent.com/developer/article/2650411)

</div>

### 🌿 [Task4：tcm_odyssey](https://github.com/DSXiangLi/tcm_odyssey)

<div align="center">

![药灵山谷 - 药园区域](https://raw.githubusercontent.com/DSXiangLi/tcm_odyssey/master/assets/herb_area.gif)

**药灵山谷 - AI 中医像素游戏** - 2D像素风格中医学习游戏，在探索药王谷的过程中学习中医知识

**可解锁技能点：Phaser 3 游戏开发，TypeScript，AI NPC（Hermes-Agent），TDD，像素美术**

[查看仓库 →](https://github.com/DSXiangLi/tcm_odyssey)

[📖 博客：和AI一起搞事情#4 - 小白用Claude Code做游戏究竟能踩多少坑](https://cloud.tencent.com/developer/article/2657050)

</div>

### 🎮 [Task5：tcm_odyssey - 进阶篇](https://github.com/DSXiangLi/tcm_odyssey)

<div align="center">

![药灵山谷 - 煎药系统](https://raw.githubusercontent.com/DSXiangLi/tcm_odyssey/master/assets/煎药.gif)

**AI 游戏开发技能进阶** - 从原型设计到代码实现的完整闭环，技能创建方法论与实践经验总结

**可解锁技能点：Claude Design，Git Worktree，自定义技能系统，进度管理方法论**

[查看仓库 →](https://github.com/DSXiangLi/tcm_odyssey)

[📖 博客：和AI一起搞事情#5 - 技能进阶与Claude Design初体验](https://cloud.tencent.com/developer/article/2664349)

</div>

---

## 🚀 快速开始

每个应用都是独立的，拥有自己的依赖和配置：

```bash
# 进入应用目录
cd crawl_deepseek

# 查看应用文档
cat README.md

# 安装依赖
pip install -r requirements.txt
```

或者体验中医方剂卡片 maker：

```bash
cd tcm_card_maker/skill/tcm_card_maker

# 查看技能文档
cat SKILL.md

# 安装依赖
pip install requests python-dotenv jinja2
```

---

## 📁 项目结构

```
ark_of_minds/
├── crawl_deepseek/          # DeepSeek爬虫应用
│   ├── src/                 # 源代码
│   ├── tests/               # 测试文件
│   ├── asset/               # 资源文件（图片、视频）
│   ├── README.md            # 应用文档
│   └── ...
├── tcm_card_maker/          # 中医方剂卡片生成器
│   ├── skill/               # 技能定义
│   ├── memory/              # 技能记忆
│   ├── asset/               # 资源文件
│   ├── test/                # 测试文件
│   ├── README.md            # 应用文档
│   └── ...
├── formula_odyssey/         # 公式奥德赛游戏
│   ├── assets/              # 资源文件（视频、演示）
│   ├── README.md            # 应用文档
│   └── ...
└── README.md                # 主文档（本文件）
```
