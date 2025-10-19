# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
# 旧版本框架通常要求插件继承自 Plugin 基类（假设存在）
from astrbot import Plugin  # 最基础的插件基类

class CallRespondPlugin(Plugin):  # 必须继承框架的 Plugin 类
    def __init__(self):
        super().__init__()
        # 关键词映射
        self.call_mapping = {
            "叫爸爸": "爸爸～",
            "叫妈妈": "妈妈～",
            "叫哥哥": "哥哥～",
            "叫姐姐": "姐姐～"
        }
        self.cool_down = {}  # 冷却存储
        self.cool_seconds = 5

    # 框架会自动调用此方法处理群消息（方法名固定）
    def on_group_message(self, data: dict):
        """处理群消息的方法（旧框架固定方法名）"""
        # 过滤自身消息
        if data.get("user_id") == self.bot.uid:  # 旧框架通常通过 self.bot.uid 获取机器人ID
            return

        # 提取信息
        user_id = data.get("user_id")
        group_id = data.get("group_id")
        msg_text = data.get("message", "").strip().lower()

        # 冷却检查
        now = datetime.now()
        last_time = self.cool_down.get(user_id, datetime.min)
        if (now - last_time).total_seconds() < self.cool_seconds:
            return

        # 匹配关键词并回复
        for keyword, reply in self.call_mapping.items():
            if keyword.lower() in msg_text:
                # 构建回复（原始@格式）
                reply_text = f"@[{user_id}] {reply}"
                # 旧框架发送群消息的方法（通过 self.bot 调用）
                self.bot.send_group(group_id, reply_text)
                self.cool_down[user_id] = now
                break

# 插件注册（旧框架通过类名识别，无需额外字典）
# 框架会自动扫描并加载继承自 Plugin 的类
