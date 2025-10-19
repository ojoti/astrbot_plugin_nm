# -*- coding: utf-8 -*-
from typing import List
from datetime import datetime, timedelta
# 从框架核心模块导入（而非插件内部）
from astrbot import AstrBotMessage  # 直接从astrbot根模块导入
from astrbot import MessageType     # 消息类型枚举
from astrbot.core.message.components import At
from astrbot.core.message import send_group

# 关键词与回应映射
call_mapping = {
    "叫爸爸": "爸爸～",
    "叫妈妈": "妈妈～",
    "叫哥哥": "哥哥～",
    "叫姐姐": "姐姐～"
}

cool_down_records = {}
COOL_DOWN_SECONDS = 5


def on_group_message(msg: AstrBotMessage):
    if msg.type != MessageType.GROUP:
        return

    if msg.sender.user_id == msg.self_id:
        return

    user_id = msg.sender.user_id
    group_id = msg.group_id
    message_text = msg.message_str.strip().lower()

    now = datetime.now()
    last_time = cool_down_records.get(user_id, datetime.min)
    if (now - last_time).total_seconds() < COOL_DOWN_SECONDS:
        return

    for keyword, reply in call_mapping.items():
        if keyword.lower() in message_text:
            reply_content: List[At] = [At(user_id), f" {reply}"]
            send_group(group_id, reply_content)
            cool_down_records[user_id] = now
            break


plugin = {
    "name": "astrbot_plugin_nm",
    "version": "1.0.0",
    "handlers": {"group_message": on_group_message}
}
