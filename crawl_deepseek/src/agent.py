import logging
import os
import json
import shutil
from pathlib import Path
from typing import Optional
from datetime import datetime

from browser_use import Agent, Browser, ChatOpenAI

from .tools import tools

logger = logging.getLogger(__name__)


def create_llm():
    """创建 LLM 客户端 - 使用 Qwen_VL"""
    base_url = os.getenv("QWEN_VL_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    api_key = os.getenv("QWEN_VL_KEY")

    if not api_key:
        raise ValueError("QWEN_VL_KEY not found in environment")

    return ChatOpenAI(
        model="qwen-vl-max",
        base_url=base_url,
        api_key=api_key,
    )


def create_agent_task(query: str) -> str:
    """生成 Agent 任务描述"""
    return f"""
向DeepSeek提问"{query}"。

步骤：
1. 打开 chat.deepseek.com (如果需要登录就登录)
2. 点击输入框，输入问题，按 Enter 发送
3. 等待AI回复完成（看到"本回答由 AI 生成"就算完成）
4. 调用 save_deepseek_result 工具保存结果
5. 调用 done 工具结束

重要：发送消息后不要重复发送，直接等待并保存！
"""


class DeepSeekAgent:
    """DeepSeek 问答 Agent - 调试版"""

    def __init__(self, profile_dir: Optional[str] = None):
        self.llm = create_llm()
        self.browser: Optional[Browser] = None
        self.agent: Optional[Agent] = None
        self.profile_dir = profile_dir
        self.debug_dir = Path("logs") / f"debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.debug_dir.mkdir(parents=True, exist_ok=True)

    def _get_storage_state_path(self) -> str:
        """获取保存的 storage state 文件路径"""
        if self.profile_dir:
            return str(Path(self.profile_dir) / "storage_state.json")
        return str(Path.home() / ".config" / "deepseek-chrome" / "storage_state.json")

    def _has_saved_cookies(self) -> bool:
        """检查是否有已保存的 cookies"""
        path = self._get_storage_state_path()
        if not os.path.exists(path):
            return False

        try:
            with open(path, "r") as f:
                content = f.read().strip()
                if not content:
                    return False
                json.loads(content)
                return True
        except (json.JSONDecodeError, Exception):
            return False

    def _save_debug_info(self, history, query: str):
        """保存调试信息：模型调用、响应、截图"""
        try:
            debug_file = self.debug_dir / f"{query[:20]}_debug.json"

            debug_info = {
                "query": query,
                "steps": [],
            }

            # 提取每一步的信息
            try:
                if history and hasattr(history, "action_history"):
                    action_history = history.action_history()
                    if isinstance(action_history, list):
                        for i, action in enumerate(action_history):
                            step_info = {
                                "step": i + 1,
                                "action": str(action)[:500] if action else "None",
                            }
                            debug_info["steps"].append(step_info)
            except Exception as e:
                logger.warning(f"Failed to extract action history: {e}")

            # 提取模型思考
            try:
                if history and hasattr(history, "model_thoughts"):
                    thoughts = history.model_thoughts()
                    if thoughts and isinstance(thoughts, list):
                        for i, thought in enumerate(thoughts[:10]):  # 只保存前10步
                            if i < len(debug_info["steps"]) and thought:
                                debug_info["steps"][i]["thought"] = str(thought)[:1500]
            except Exception as e:
                logger.warning(f"Failed to extract model thoughts: {e}")

            # 提取截图
            try:
                if history and hasattr(history, "screenshot_paths"):
                    screenshots = history.screenshot_paths()
                    if screenshots and isinstance(screenshots, list):
                        debug_info["screenshot_count"] = len(screenshots)
                        for j, screenshot_path in enumerate(screenshots[-5:]):
                            if screenshot_path and os.path.exists(str(screenshot_path)):
                                ext = Path(str(screenshot_path)).suffix or ".png"
                                new_name = f"{query[:20]}_step{j + 1}{ext}"
                                try:
                                    shutil.copy(str(screenshot_path), self.debug_dir / new_name)
                                    if j < len(debug_info["steps"]):
                                        debug_info["steps"][j]["screenshot"] = str(
                                            self.debug_dir / new_name
                                        )
                                except:
                                    pass
            except Exception as e:
                logger.warning(f"Failed to extract screenshots: {e}")

            # 提取模型输出
            try:
                if history and hasattr(history, "model_outputs"):
                    outputs = history.model_outputs()
                    if outputs and isinstance(outputs, list):
                        debug_info["model_outputs"] = [str(o)[:1000] for o in outputs[:5]]
            except:
                pass

            # 保存调试JSON
            with open(debug_file, "w", encoding="utf-8") as f:
                json.dump(debug_info, f, ensure_ascii=False, indent=2)

            logger.info(f"Debug info saved to {debug_file}")

        except Exception as e:
            logger.error(f"Failed to save debug info: {e}")

    async def run(self, query: str) -> dict:
        """运行单个 query"""
        config: dict = {
            "headless": False,
            "keep_alive": True,
            "window_size": {"width": 1200, "height": 800},
        }

        storage_state_path = self._get_storage_state_path()

        # 优先使用CDP连接已运行的Chrome
        cdp_url = "http://localhost:52245"
        try:
            import urllib.request

            urllib.request.urlopen(cdp_url, timeout=2)
            config["cdp_url"] = cdp_url
            logger.info(f"Using CDP to connect to existing Chrome at {cdp_url}")
        except Exception:
            # 回退到使用storage_state方式
            if self._has_saved_cookies():
                config["storage_state"] = storage_state_path
                logger.info(f"Using saved cookies from {storage_state_path}")
            else:
                logger.info("No valid saved cookies found. First run will require manual login.")
                os.makedirs(os.path.dirname(storage_state_path), exist_ok=True)

        self.browser = Browser(**config)

        self.agent = Agent(
            task=create_agent_task(query),
            llm=self.llm,
            browser=self.browser,
            tools=tools,
            use_vision="auto",
            save_conversation_path=str(self.debug_dir / f"{query[:20]}_conversation.json"),
        )

        history = await self.agent.run(max_steps=100)

        # 保存调试信息
        self._save_debug_info(history, query)

        # 检查是否成功进入chat界面，如果是则保存cookies
        try:
            if (
                history
                and history.final_result()
                and "LOGIN_REQUIRED" not in str(history.final_result())
            ):
                await self.browser.export_storage_state(storage_state_path)
                logger.info(f"Cookies saved after successful login to {storage_state_path}")
                if os.path.exists(storage_state_path):
                    file_size = os.path.getsize(storage_state_path)
                    logger.info(f"Storage state file size: {file_size} bytes")
            else:
                logger.info("Login not successful, not saving cookies")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")

        return {
            "query": query,
            "success": history.is_done() if history else False,
            "result": history.final_result() if history else None,
            "history": history,
        }

    async def close(self):
        """关闭浏览器"""
        if self.browser:
            try:
                await self.browser.stop()
            except Exception as e:
                logger.error(f"Error closing browser: {e}")
