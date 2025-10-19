# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

# 旧框架最基础的插件基类（最后尝试的导入路径）
try:
    from astrbot.core import BasePlugin  # 优先尝试核心模块
except ImportError:
    from astrbot import BasePlugin  # 备选路径


# 框架强制要求的主类名：必须是Main，且继承自BasePlugin
class Main(BasePlugin):
    def __init__(self):
        super().__init__()  # 必须调用父类初始化
        self.call_mapping = {
            "叫爸爸": "爸爸～",
            "叫妈妈": "妈妈～",
            "叫哥哥": "哥哥～",
            "叫姐姐": "姐姐～"
        }
        self.cool_down = {}
        self.cool_seconds = 5

    # 框架固定的群消息处理方法：必须命名为handle_group
    def handle_group(self, data):
        """处理群消息的核心方法（框架会自动调用）"""
        # 从原始数据中提取必要信息（旧框架数据格式）
        user_id = data.get("user_id")
        group_id = data.get("group_id")
        msg_text = data.get("content", "").strip().lower()
        bot_id = data.get("robot_id")  # 机器人自身ID

        # 过滤自身消息
        if user_id == bot_id:
            return

        # 冷却检查
        now = datetime.now()
        last_time = self.cool_down.get(user_id, datetime.min)
        if (now - last_time).total_seconds() < self.cool_seconds:
            return

        # 匹配关键词并回复
        for keyword, reply in self.call_mapping.items():
            if keyword.lower() in msg_text:
                # 构建回复（包含@）
                reply_content = f"@{user_id} {reply}"
                # 调用框架的发送接口（旧框架通用方法）
                self.send_group(group_id, reply_content)
                self.cool_down[user_id] = now
                break

    # 框架要求的发送群消息方法（封装底层调用）
    def send_group(self, group_id, content):
        """调用框架底层发送功能"""
        # 旧框架通常通过父类的方法发送消息
        self.parent.send("group", group_id, content)
