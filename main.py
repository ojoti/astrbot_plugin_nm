# -*- coding: utf-8 -*-
from typing import List
from datetime import datetime, timedelta
from astrbot.core import add_handler  # 框架核心的事件注册方法
from astrbot.core.message.components import At  # 艾特组件（用于@用户）
from .message_type import MessageType  # 消息类型枚举（群聊/私聊）
from . import AstrBotMessage  # 框架的消息对象类

# 关键词与回应映射
call_mapping = {
    "叫爸爸": "爸爸～",
    "叫妈妈": "妈妈～"，
    "叫哥哥": "哥哥～",
    "叫姐姐": "姐姐～"
}

# 冷却时间存储：{用户ID: 最后响应时间}
cool_down_records = {}
# 冷却时长（秒）
COOL_DOWN_SECONDS = 5


def handle_group_message(msg: AstrBotMessage):
    """处理群聊消息的回调函数"""
    # 1. 仅处理群聊消息
    if msg.type != MessageType.GROUP:
        return

    # 2. 过滤机器人自己发送的消息（避免自我触发）
    if msg.sender.user_id == msg.self_id:
        return

    # 3. 提取关键信息
    user_id = msg.sender.user_id  # 发送者ID
    group_id = msg.group_id       # 群ID（从AstrBotMessage的group_id属性获取）
    message_text = msg.message_str.strip().lower()  # 消息文本（转小写，忽略大小写）

    # 4. 冷却时间检查
    now = datetime.now()
    last_time = cool_down_records.get(user_id, datetime.min)
    if (now - last_time).total_seconds() < COOL_DOWN_SECONDS:
        return  # 冷却中，不响应

    # 5. 匹配关键词并回复
    for keyword, reply in call_mapping.items():
        if keyword.lower() in message_text:
            # 构建回复消息链：艾特用户 + 回应文本
            reply_components: List[At] = [
                At(user_id),  # 艾特发送者
                f" {reply}"   # 回应内容（加空格分隔艾特和文本）
            ]
            # 调用框架的消息发送方法（通过msg对象的上下文发送到对应群）
            # 注意：此处需根据框架实际发送接口调整，以下为示例
            from astrbot.core.message import send_group  # 框架的群消息发送方法
            send_group(group_id, reply_components)

            # 更新冷却时间
            cool_down_records[user_id] = now
            break  # 只响应第一个匹配的关键词


# 注册事件处理器：监听群聊消息事件
add_handler("group_message", handle_group_message)
