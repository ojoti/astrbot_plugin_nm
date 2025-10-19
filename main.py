# -*- coding: utf-8 -*-
# 适配 AstrBot v4.3.5（极旧版本，无 Star 类）
from astrbot.plugin import Plugin, plugin  # 旧版本插件基类是 Plugin
from astrbot.event import Event  # 旧版本事件基类
from astrbot.message import Message, At  # 消息和艾特组件
from datetime import datetime, timedelta

# 注册插件（旧版本用 @plugin 装饰器，参数为元信息）
@plugin(
    name="astrbot_plugin_nm",  # 必须与文件夹名一致
    author="YourName",
    version="1.0.0",
    description="检测群聊称呼关键词并@回应"
)
class CallRespondPlugin(Plugin):  # 继承 Plugin 而非 Star
    def __init__(self, bot):
        super().__init__(bot)
        self.call_mapping = {
            "叫爸爸": "爸爸～",
            "叫妈妈": "妈妈～",
            "叫哥哥": "哥哥～",
            "叫姐姐": "姐姐～"
        }
        self.cool_down = {}  # {用户ID: 最后响应时间}
        self.cool_seconds = 5

    # 监听群聊消息（旧版本用 on 方法绑定事件）
    def on_group_message(self, event: Event):
        # 过滤机器人自己的消息
        if event.uid == self.bot.uid:
            return

        # 获取消息内容和用户ID（旧版本事件属性）
        msg_text = event.text.strip().lower()  # 消息文本
        user_id = event.uid  # 发送者ID
        group_id = event.group_id  # 群聊ID

        # 冷却检查
        now = datetime.now()
        last_time = self.cool_down.get(user_id, datetime.min)
        if (now - last_time).total_seconds() < self.cool_seconds:
            return

        # 匹配关键词并回复
        for keyword, reply in self.call_mapping.items():
            if keyword.lower() in msg_text:
                # 构建回复消息：艾特 + 文本
                reply_msg = Message()
                reply_msg.append(At(user_id))  # 添加艾特组件
                reply_msg.append(reply)  # 添加文本内容
                # 发送到对应群聊
                self.bot.send_group_message(group_id, reply_msg)
                # 更新冷却时间
                self.cool_down[user_id] = now
                break
