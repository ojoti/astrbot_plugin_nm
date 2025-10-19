# -*- coding: utf-8 -*-
# 适配 AstrBot v4.3.5 版本（旧版 API 结构）
from astrbot import Star, register  # 旧版本核心类导入
from astrbot.filter import on_message  # 旧版本消息过滤装饰器
from astrbot.message import At  # 旧版本艾特组件
from astrbot.event import AstrMessageEvent  # 旧版本消息事件类
from datetime import datetime, timedelta

# 注册插件（v4.3.5 版本的 register 装饰器参数格式）
@register(
    name="astrbot_plugin_nm",  # 必须与插件文件夹名一致
    author="YourName",
    description="检测群聊称呼关键词并@回应",
    version="1.0.0"
)
class CallRespondPlugin(Star):
    def __init__(self):
        super().__init__()
        # 关键词与回应映射
        self.call_mapping = {
            "叫爸爸": "爸爸～",
            "叫妈妈": "妈妈～",
            "叫哥哥": "哥哥～",
            "叫姐姐": "姐姐～"
        }
        self.cool_down = {}  # {用户ID: 最后响应时间}
        self.cool_seconds = 5  # 冷却时间

    # 监听所有消息（旧版本用 on_message 装饰器）
    @on_message
    def handle_message(self, event: AstrMessageEvent):
        # 仅处理群聊消息（v4.3.5 通过 event.type 判断）
        if event.type != "group":
            return

        # 过滤机器人自己的消息
        if event.is_self:
            return

        # 获取发送者ID和消息文本（旧版本属性）
        user_id = event.user_id
        msg_text = event.content.strip().lower()  # event.content 是消息内容

        # 冷却检查
        now = datetime.now()
        last_time = self.cool_down.get(user_id, datetime.min)
        if (now - last_time).total_seconds() < self.cool_seconds:
            return

        # 匹配关键词并回复
        for keyword, reply in self.call_mapping.items():
            if keyword.lower() in msg_text:
                # 构建艾特+回应（旧版本消息链格式）
                reply_msg = [At(user_id), f" {reply}"]
                # 发送回复（旧版本用 self.send 方法）
                self.send(event, reply_msg)
                # 更新冷却时间
                self.cool_down[user_id] = now
                break
