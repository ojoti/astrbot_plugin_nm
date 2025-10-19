# -*- coding: utf-8 -*-
from astrbot.api.event import filter, AstrMessageEvent, GroupMessageEvent  # 明确导入群聊事件
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import At  # 正确导入艾特组件
from datetime import datetime, timedelta

# 注册插件信息（确保参数正确，无多余空格）
@register(
    plugin_name="call_respond",
    author="YourName",
    description="检测群聊中称呼关键词并@发送者回应",
    version="1.2.0"
)
class CallRespondPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # 关键词与回应映射（支持带标点的模糊匹配）
        self.call_mapping = {
            "叫爸爸": "爸爸～",
            "叫妈妈": "妈妈～",
            "叫哥哥": "哥哥～",
            "叫姐姐": "姐姐～"
        }
        # 冷却时间记录：{用户ID: 最后响应时间}，防止刷屏
        self.cool_down_records = {}
        # 冷却时长（秒）
        self.cool_down_seconds = 5

    async def initialize(self):
        """插件初始化成功提示"""
        logger.info(f"[{self.__class__.__name__}] 插件加载成功，版本：1.2.0")

    @filter.all()  # 监听所有消息
    async def on_message(self, event: AstrMessageEvent):
        """处理消息：仅群聊生效，过滤自身消息，带冷却机制"""
        # 仅处理群聊消息（过滤私聊）
        if not isinstance(event, GroupMessageEvent):
            return

        # 过滤机器人自己的消息（防止自我触发）
        if event.is_self():
            return

        # 获取发送者ID和消息文本（处理大小写和空格）
        sender_id = event.get_sender_id()
        message_text = event.message_str.strip().lower()  # 转为小写，忽略大小写

        # 检查冷却时间
        now = datetime.now()
        last_time = self.cool_down_records.get(sender_id, datetime.min)
        if (now - last_time).total_seconds() < self.cool_down_seconds:
            logger.debug(f"用户 {sender_id} 处于冷却中，跳过响应")
            return

        # 匹配关键词并回应
        for keyword, reply in self.call_mapping.items():
            # 关键词转为小写，支持模糊匹配（如"叫爸爸！"也能触发）
            if keyword.lower() in message_text:
                # 构建艾特+回应的消息链
                reply_chain = [At(sender_id), f" {reply}"]
                # 发送回应
                yield event.result(reply_chain)
                # 更新冷却时间
                self.cool_down_records[sender_id] = now
                # 日志记录
                logger.info(f"群 {event.group_id} | 用户 {sender_id} 触发关键词「{keyword}」")
                break  # 只响应第一个匹配的关键词

    async def terminate(self):
        """插件卸载提示"""
        logger.info(f"[{self.__class__.__name__}] 插件已卸载")
        
