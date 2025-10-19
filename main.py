# -*- coding: utf-8 -*-
# 兼容 AstrBot < 0.6.0 版本，修复 GroupMessageEvent 导入错误
from astrbot.api.event import filter, MessageEvent  # 旧版本用 MessageEvent
from astrbot.adapter.onebot.v11.event import GroupMessage  # 从 onebot 适配器导入群聊事件
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import At
from datetime import datetime, timedelta

@register(
    plugin_name="call_respond",
    author="YourName",
    description="检测群聊中称呼关键词并@发送者回应（兼容旧版本）",
    version="1.2.1"
)
class CallRespondPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.call_mapping = {
            "叫爸爸": "哎，乖儿子/女儿～",
            "叫妈妈": "哎，宝贝～",
            "叫哥哥": "来啦，小老弟/小老妹～",
            "叫姐姐": "嗯呢，小可爱～"
        }
        self.cool_down_records = {}  # {用户ID: 最后响应时间}
        self.cool_down_seconds = 5  # 冷却时间（秒）

    async def initialize(self):
        logger.info(f"[{self.__class__.__name__}] 插件加载成功（兼容模式）")

    @filter.all()
    async def on_message(self, event: MessageEvent):  # 用 MessageEvent 接收消息
        # 仅处理群聊消息（旧版本判断方式）
        if not isinstance(event, GroupMessage):
            return

        # 过滤机器人自己的消息
        if event.is_self:  # 旧版本可能用 event.is_self 而非 event.is_self()
            return

        # 获取发送者ID和消息文本
        sender_id = event.user_id  # 旧版本用 event.user_id 获取用户ID
        message_text = str(event.message).strip().lower()  # 旧版本用 str(event.message) 获取文本

        # 冷却时间检查
        now = datetime.now()
        last_time = self.cool_down_records.get(sender_id, datetime.min)
        if (now - last_time).total_seconds() < self.cool_down_seconds:
            logger.debug(f"用户 {sender_id} 处于冷却中，跳过响应")
            return

        # 关键词匹配与回应
        for keyword, reply in self.call_mapping.items():
            if keyword.lower() in message_text:
                # 构建艾特+回应消息
                reply_chain = [At(sender_id), f" {reply}"]
                yield event.result(reply_chain)
                # 更新冷却时间
                self.cool_down_records[sender_id] = now
                logger.info(f"群 {event.group_id} | 用户 {sender_id} 触发关键词「{keyword}」")
                break

    async def terminate(self):
        logger.info(f"[{self.__class__.__name__}] 插件已卸载")
