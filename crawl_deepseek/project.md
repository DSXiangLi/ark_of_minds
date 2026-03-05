# 目标
使用browser-use自动登录deepseek网站，并在开启深度思考和联网模式下提问。
然后把模型回答，和所有引用的网站链接，复制并保存到'{query}.json'文件中

## 操作流程
1. 输入query
2. 打开深度思考和智能搜索（联网模式）
3. 点击运行（发送按钮）
4. 等待模型回答完成
5. 点击复制按钮，从剪贴板获取模型回答
6. 如果没有网页信息，references部分为空
7. 如果有网页信息，点击网页引用链接，获取页面上展示的网站信息（标题、URL等）
8. 以上内容按输出格式写入文件

### 输入
{
    "query":"用户query"
}

### 输出
以下内容写入到`{query}.json`的文件中
```json
{
  "answer": "模型回答",
  "references": [{
    "id": "引用ID",
    "title": "网页标题",
    "url": "网站url",
    "meta": "任何你能获得的关于引用网站的其他信息都可以存储在这里"
  }]
}

```
### 批处理要求
需要可以输入一个query列表，然后逐一完成以上任务


## 代码要求
### 原则
1. 第一性原理：永远从源头排查、解决问题，严格禁止打补丁式后处理方案
2. 自主：除需要用户登录之类的问题，其余问题均自主判断解决
3. 先学习再行动：遇到问题，可以先从`AGENTS.md`中寻找官方browser-use的解决方案，再尝试自己解决
4. clean-and-neat: 代码仓库中所有代码都为必须代码，任何无用代码即刻删除，时刻保持代码仓库的干净整洁，没有一行多余代码

### 基础要求
1. 使用Qwen_VL多模态模型，APIKey在.env文件中
2. base Language：Python
3. Agent Language: browser-use, langchain or openai

### 网站登录要求
1. 第一次人工登录，登录后记录所有登录信息后续使用该登录信息自动登录


## 实施计划

### Phase 1: 环境搭建 (1天)
| 任务 | 说明 | 优先级 |
|------|------|--------|
| 1.1 | 创建 pyproject.toml 配置项目依赖 | P0 |
| 1.2 | 创建虚拟环境 `uv venv --python 3.11` | P0 |
| 1.3 | 安装依赖 `uv sync` | P0 |
| 1.4 | 安装 Chromium `uvx browser-use install` | P0 |
| 1.5 | 配置登录 profile（首次人工登录） | P0 |

### Phase 2: 核心功能开发 (2-3天)
| 任务 | 说明 | 优先级 |
|------|------|--------|
| 2.1 | 登录管理 - 复用 Chrome profile 自动登录 | P0 |
| 2.2 | 深度思考模式 - 自动开启深度思考开关 | P0 |
| 2.3 | 联网模式 - 自动开启联网搜索开关 | P0 |
| 2.4 | 提问与等待 - 输入 query，等待生成完成 | P0 |
| 2.5 | 复制回答 - 点击复制按钮读取剪贴板 | P0 |
| 2.6 | JSON 输出 - 按格式写入文件 | P0 |

### Phase 3: 批处理与完善 (1-2天)
| 任务 | 说明 | 优先级 |
|------|------|--------|
| 3.1 | 批处理支持 - 逐一处理 query 列表 | P0 |
| 3.2 | 日志系统 - 记录所有操作到 ./logs/ | P0 |
| 3.3 | 截图保存 - 保存中间截图 | P1 |


## 技术方案

### LLM 配置
使用 Qwen_VL 多模态模型（project.md 要求）：
```python
from browser_use import Agent, Browser
from browser_use import ChatOpenAI

llm = ChatOpenAI(
    model="qwen-vl-max",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("QWEN_VL_KEY")
)
```

### Agent Task 设计
根据 AGENTS.md 提示，使用详细的步骤描述：
```python
task = """
1. Navigate to https://chat.deepseek.com and wait for page load
2. If not logged in:
   - Ask human for help with login
3. Enable deep thinking mode by finding and clicking the toggle
4. Enable联网 search mode by finding and clicking the toggle
5. Input the query: "{user_query}"
6. Click the send button
7. Wait for response generation to complete (no more streaming)
8. Click copy button and read clipboard as answer
9. If references exist, click each to extract title, url, meta
10. Save to {query}.json with format:
    {{"answer": "...", "references": [{{"id": "...", "title": "...", "url": "...", "meta": "..."}}]}}
"""
```

### 登录方案
- 使用 Chrome user_data_dir 持久化登录状态
- 首次运行不传 user_data_dir，人工登录一次
- 后续运行传入已保存的 profile 目录实现自动登录


## 测试计划

### 测试数据集
位置: `tests/test_queries.json`
```json
[
  {"query": "什么是人工智能？请简要解释并给出3个实际应用场景。"},
  {"query": "2024年最新的机器学习框架有哪些？请比较它们的优缺点。"},
  {"query": "气候变化对全球经济的影响有哪些？请提供数据支持。"},
  {"query": "ji"},
  {"query": "今天北京天气怎么样？请用联网搜索功能查找。"}
]
```

### 验收标准
- 每个 query 生成对应的 `{query}.json` 文件
- JSON 包含 `answer` 和 `references` 字段
- 无程序异常退出
- 日志完整记录所有操作

### 验收标准（增强版）

#### 回答完整性
- [ ] AI 回答必须以 "本回答由 AI 生成" 或 "内容由 AI 生成" 作为完成标志
- [ ] 回答长度应该合理（通常 > 500 字符，取决于问题复杂度）
- [ ] 回答内容完整，没有被截断

#### 引用完整性
- [ ] 引用的数量应该与 AI 报告中 "已阅读 X 个网页" 的数量一致（或接近）
- [ ] 每个引用包含有效的 title 和 url
- [ ] 排除网站自身的链接（如 deepseek.com）

#### 验证方法
```python
# 1. 检查完成标志
assert "本回答由 AI 生成" in answer or "内容由 AI 生成" in answer

# 2. 验证引用数量
import re
match = re.search(r'已阅读\s*(\d+)\s*个网页', answer)
reported_refs = int(match.group(1)) if match else 0
assert len(references) >= reported_refs * 0.6  # 允许部分丢失

# 3. 验证回答长度
assert len(answer) > 500  # 根据问题复杂度调整
```

### 测试通过标准
所有 5 个 query 全部成功完成


## 日志要求
1. 所有日志均写入./logs目录
2. 请完整记录browser-use每一步操作，模型对话的全部上文用于问题排查
3. 如果使用多模态模型，则把中间截图输入一并保存


## 项目结构
```
auto_crawl_v2/
├── src/
│   ├── __init__.py
│   ├── main.py           # 入口
│   ├── agent.py          # Agent 核心逻辑
│   ├── login.py          # 登录管理
│   └── tools.py          # 自定义工具
├── tests/
│   ├── test_queries.json
│   └── test_*.py
├── logs/
├── pyproject.toml
├── .env
└── AGENTS.md
```


## 待确认事项
- [ ] DeepSeek 登录是否需要手机验证码
- [ ] 深度思考/联网开关的 UI 位置和定位方式
- [ ] 响应完成的判定方式（流式输出停止）


## 经验总结

### 高纬度原则

#### 1. 等待策略：宁可过度等待，不要提前提取
- **核心**: 异步任务（如 AI 生成、网络请求）的完成时间不可预测
- **实践**: 使用明确的完成标志（completion marker）而非时间推断
- **案例**: DeepSeek 使用 "本回答由 AI 生成" 而非 "已思考"（出现在回答开头）

```python
# ❌ 错误：固定时间等待
await asyncio.sleep(5)  # 可能 AI 还在生成

# ✅ 正确：轮询检查完成标志
for i in range(max_wait // interval):
    await asyncio.sleep(interval)
    if "完成标志" in await page.evaluate("document.body.innerText"):
        break
```

#### 2. 数据提取：从 DOM 而非视觉判断
- **核心**: 截图/视觉判断容易误判，应直接从页面 DOM 提取数据
- **实践**: 使用 JavaScript 获取元素内容，而非依赖截图识别
- **案例**: 通过 `document.body.innerText` 获取完整文本，通过 `querySelectorAll('a[href]')` 获取链接

#### 3. 引用提取：匹配期望值
- **核心**: 页面可能显示引用数量（如 "已阅读 10 个网页"），提取时应参考此数值
- **实践**: 先解析页面显示的引用数量，再按此数量提取链接
- **原因**: 页面渲染可能延迟，直接提取可能丢失部分链接

```javascript
// 从页面文本解析期望引用数
var refCountMatch = bodyText.match(/已阅读\s*(\d+)\s*个网页/);
var expectedRefCount = refCountMatch ? parseInt(refCountMatch[1]) : 10;

// 按期望数量提取
result.references = uniqueRefs.slice(0, expectedRefCount);
```

#### 4. 调试原则：保留证据链
- **核心**: 自动化失败时，需要完整的上下文排查问题
- **实践**: 保存对话历史、每步截图、模型输出
- **工具**: `save_conversation_path`, `screenshot_paths`, `model_outputs`

#### 5. 避免硬编码
- **核心**: 代码应通用化，适应不同场景
- **实践**: 
  - 不硬编码特定 query
  - 使用参数传递而非字符串匹配
  - 从页面结构动态提取而非假设固定结构

### DeepSeek 特定经验

1. **完成标志**: 使用 "本回答由 AI 生成" 而非 "已阅读"（出现在回答开头）
2. **登录持久化**: 使用 `storage_state` 而非 `user_data_dir`（更轻量）
3. **引用提取**: 需要排除 `deepseek.com` 域名下的链接
