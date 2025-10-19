# -*- coding: utf-8 -*-
from typing import List
from datetime import datetime, timedelta
# 从框架核心模块导入（而非插件内部）
from astrbot.core.message import AstrBotMessage  # 假设在 core.message 模块中
from astrbot.core.message import MessageType      # 消息类型枚举也从核心模块导入
from astrbot.core.message.components import At
from astrbot.core.message import send_group

# 关键词与回应映射
call_mapping = {
    "叫爸爸": "爸爸～",
    "叫妈妈": "妈妈～",
    "叫哥哥": "哥哥～",
    "叫姐姐": "姐姐～"
}

# 冷却时间存储
cool_down_records = {}
COOL_DOWN_SECONDS = 5


def on_group_message(msg: AstrBotMessage):
    # 仅处理群聊消息
    if msg.type != MessageType.GROUP:
        return

    # 过滤自身消息
    if msg.sender.user_id == msg.self_id:
        return

    # 提取信息
    user_id = msg.sender.user_id
    group_id = msg.group_id
    message_text = msg.message_str.strip().lower()

    # 冷却检查
    now = datetime.now()
    last_time = cool_down_records.get(user_id, datetime.min)
    if (now - last_time).total_seconds() < COOL_DOWN_SECONDS:
        return

    # 匹配关键词并回复
    for keyword, reply in call_mapping.items():
        if keyword.lower() in message_text:
            reply_content: List[At] = [At(user_id), f" {reply}"]
            send_group(group_id, reply_content)
            cool_down_records[user_id] = now
            break


# 插件入口
plugin = {
    "name": "astrbot_plugin_nm",
    "version": "1.0.0",
    "handlers": {"group_message": on_group_message}
}
