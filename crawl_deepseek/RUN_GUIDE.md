# auto_crawl_v2 运行指南

## 快速开始

### 1. 环境准备
```bash
# 确保在项目目录
cd /home/lixiang/Desktop/auto_crawl_v2

# 激活虚拟环境（如果使用）
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows

# 安装依赖（如果需要）
uv sync
```

### 2. 首次运行（需要手动登录）
```bash
# 运行一个测试查询
python -m src.main -q "测试查询"

# 或者使用测试文件中的第一个查询
python -m src.main -q "什么是人工智能？请简要解释并给出3个实际应用场景。"
```

**首次运行时:**
1. 浏览器会自动打开
2. 导航到 DeepSeek 网站
3. **需要手动登录**（输入手机号、验证码等）
4. 登录成功后，程序会自动保存cookies
5. 然后继续执行查询任务

### 3. 后续运行（自动登录）
```bash
# 使用保存的cookies自动登录
python -m src.main -q "今天天气怎么样？"

# 或者使用批处理模式
python -m src.main -f tests/test_queries.json
```

## 命令行参数

### 基本用法:
```bash
python -m src.main [选项]
```

### 选项:
- `-q, --query TEXT`: 运行单个查询
  ```bash
  python -m src.main -q "你的查询内容"
  ```

- `-f, --file PATH`: 运行批处理（JSON文件）
  ```bash
  python -m src.main -f tests/test_queries.json
  ```

- `-p, --profile PATH`: 使用自定义profile目录
  ```bash
  python -m src.main -q "查询" -p "./my_profile"
  ```

### 示例:
```bash
# 单个查询
python -m src.main -q "Python和Java有什么区别？"

# 批处理
python -m src.main -f tests/test_queries.json

# 自定义profile
python -m src.main -q "测试" -p "~/.config/deepseek-custom"
```

## 输出文件

### 生成的文件:
1. **JSON结果文件**: `{查询内容}.json`
   ```json
   {
     "answer": "模型回答内容...",
     "references": [
       {
         "id": "ref_1",
         "title": "网页标题",
         "url": "https://example.com",
         "meta": "附加信息"
       }
     ]
   }
   ```

2. **日志文件**: `logs/crawl_YYYYMMDD_HHMMSS.log`
   - 包含所有操作的详细日志
   - 用于故障排除

### 文件位置:
1. JSON文件: 当前目录或指定输出目录
2. Cookies文件: `~/.config/deepseek-chrome/storage_state.json`
3. 日志文件: `logs/` 目录

## 故障排除

### 常见问题:

#### 1. 登录失败
```bash
# 清除保存的cookies，重新登录
rm ~/.config/deepseek-chrome/storage_state.json
python -m src.main -q "测试"
```

#### 2. 浏览器无法打开
```bash
# 检查Chromium是否安装
uvx browser-use install

# 尝试headless模式（修改src/agent.py中的headless=True）
```

#### 3. 查询超时
```bash
# 增加等待时间（修改src/agent.py中的等待逻辑）
# 或检查网络连接
```

#### 4. JSON文件未生成
```bash
# 检查文件权限
ls -la *.json

# 检查日志
tail -f logs/crawl_*.log
```

### 调试模式:
```bash
# 设置详细日志
export BROWSER_USE_LOGGING_LEVEL=debug

# 运行程序
python -m src.main -q "测试"
```

## 高级用法

### 1. 自定义配置
修改 `src/agent.py` 中的配置:
```python
config: dict = {
    "headless": False,  # 改为True以隐藏浏览器
    "keep_alive": True,
    "window_size": {"width": 1200, "height": 800},
    "use_vision": "auto",  # 视觉辅助
}
```

### 2. 添加自定义工具
在 `src/tools.py` 中添加新的 `@tools.action` 装饰函数。

### 3. 修改任务描述
更新 `src/agent.py` 中的 `create_agent_task` 函数。

### 4. 使用Cloud Browser（绕过验证码）
```python
# 在src/agent.py中修改Browser配置
config["use_cloud"] = True
config["cloud_profile_id"] = "your-profile-id"
```

## 监控和日志

### 查看日志:
```bash
# 查看最新日志
tail -f logs/crawl_*.log

# 搜索错误
grep -i error logs/crawl_*.log

# 查看成功记录
grep -i success logs/crawl_*.log
```

### 监控输出:
```bash
# 实时监控JSON文件生成
watch -n 1 'ls -la *.json 2>/dev/null || echo "No JSON files"'
```

## 性能提示

### 优化速度:
1. 使用 `headless=True` 模式
2. 减少等待时间（适当调整）
3. 使用更快的LLM模型

### 优化稳定性:
1. 增加重试次数
2. 添加更长的等待时间
3. 使用更详细的错误处理

## 支持

### 获取帮助:
1. 查看日志文件获取详细错误信息
2. 检查 `AGENTS.md` 中的browser-use文档
3. 查看 `FIX_SUMMARY.md` 中的修复总结

### 报告问题:
1. 提供相关日志文件
2. 描述具体问题和复现步骤
3. 包括环境信息（操作系统、Python版本等）
