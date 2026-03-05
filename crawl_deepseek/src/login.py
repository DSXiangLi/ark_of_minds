import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class LoginManager:
    """管理 DeepSeek 登录状态 - 使用 storage_state 方法"""

    def __init__(self, profile_dir: Optional[str] = None):
        self.profile_dir = profile_dir or self._get_default_profile_dir()
        self.storage_state_path = Path(self.profile_dir) / "storage_state.json"

    def _get_default_profile_dir(self) -> str:
        """获取默认的profile目录"""
        base_dir = Path.home() / ".config" / "deepseek-chrome"
        base_dir.mkdir(parents=True, exist_ok=True)
        return str(base_dir)

    def has_valid_storage_state(self) -> bool:
        """检查是否有有效的storage state文件"""
        if not self.storage_state_path.exists():
            return False
        
        try:
            with open(self.storage_state_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    logger.warning("Storage state file is empty")
                    return False
                
                data = json.loads(content)
                # 检查是否有cookies
                cookies = data.get('cookies', [])
                if not cookies:
                    logger.warning("No cookies found in storage state")
                    return False
                
                # 检查是否有DeepSeek相关的cookies
                deepseek_cookies = [c for c in cookies if 'deepseek' in c.get('domain', '').lower()]
                if not deepseek_cookies:
                    logger.warning("No DeepSeek cookies found")
                    return False
                
                logger.info(f"Found {len(cookies)} cookies, {len(deepseek_cookies)} DeepSeek cookies")
                return True
                
        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"Invalid storage state file: {e}")
            return False

    def get_browser_config(self, headless: bool = False) -> Dict[str, Any]:
        """获取浏览器配置"""
        config = {
            "headless": headless,
            "window_size": {"width": 1200, "height": 800},
            "keep_alive": True,
        }
        
        if self.has_valid_storage_state():
            config["storage_state"] = str(self.storage_state_path)
            logger.info(f"Using storage state from {self.storage_state_path}")
        else:
            logger.info("No valid storage state found - will require manual login")
            # 确保目录存在
            self.storage_state_path.parent.mkdir(parents=True, exist_ok=True)
        
        return config

    def save_storage_state(self, storage_state: Dict[str, Any]) -> bool:
        """保存storage state到文件"""
        try:
            # 确保目录存在
            self.storage_state_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.storage_state_path, 'w', encoding='utf-8') as f:
                json.dump(storage_state, f, ensure_ascii=False, indent=2)
            
            file_size = os.path.getsize(self.storage_state_path)
            logger.info(f"Storage state saved to {self.storage_state_path} ({file_size} bytes)")
            
            # 验证保存的文件
            if self.has_valid_storage_state():
                logger.info("Storage state validated successfully")
                return True
            else:
                logger.warning("Saved storage state validation failed")
                return False
                
        except Exception as e:
            logger.error(f"Failed to save storage state: {e}")
            return False

    def clear_storage_state(self) -> bool:
        """清除storage state"""
        try:
            if self.storage_state_path.exists():
                self.storage_state_path.unlink()
                logger.info("Storage state cleared")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to clear storage state: {e}")
            return False

    def get_storage_state_info(self) -> Dict[str, Any]:
        """获取storage state信息"""
        info = {
            "path": str(self.storage_state_path),
            "exists": self.storage_state_path.exists(),
            "valid": False,
            "size": 0,
            "cookie_count": 0,
        }
        
        if self.storage_state_path.exists():
            info["size"] = os.path.getsize(self.storage_state_path)
            info["valid"] = self.has_valid_storage_state()
            
            if info["valid"]:
                try:
                    with open(self.storage_state_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        cookies = data.get('cookies', [])
                        info["cookie_count"] = len(cookies)
                except Exception:
                    pass
        
        return info
