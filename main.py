# -*- coding: utf-8 -*-
from typing import List
from datetime import datetime, timedelta
# 仅导入框架确认存在的核心类
from . import AstrBotMessage
from .message_type import MessageType
from astrbot.core.message.components import At
from astrbot.core.message import send_group  # 框架自带的群消息发送方法

# 关键词与回应映射（确保英文标点和逗号）
call_mapping = {
    "叫爸爸": "爸爸～",
    "叫妈妈": "妈妈～",
    "叫哥哥": "哥哥～",
    "叫姐姐": "姐姐～"
}

# 冷却时间存储：{用户ID: 最后响应时间}
cool_down_records = {}
# 冷却时长（秒），防止刷屏
COOL_DOWN_SECONDS = 5


def on_group_message(msg: AstrBotMessage):
    """
    群消息处理函数
    框架会自动扫描并调用此函数处理群聊消息
    """
    # 1. 仅处理群聊消息（过滤私聊等其他类型）
    if msg.type != MessageType.GROUP:
        return

    # 2. 过滤机器人自己发送的消息（避免自我触发）
    if msg.sender.user_id == msg.self_id:
        return

    # 3. 提取消息关键信息
    user_id = msg.sender.user_id  # 发送者QQ号
    group_id = msg.group_id       # 群号
    message_text = msg.message_str.strip().lower()  # 消息文本（转小写，支持模糊匹配）

    # 4. 冷却时间检查（同一用户5秒内只能触发一次）
    now = datetime.now()
    last_trigger_time = cool_down_records.get(user_id, datetime.min)
    if (now - last_trigger_time).total_seconds() < COOL_DOWN_SECONDS:
        return  # 冷却中，不响应

    # 5. 匹配关键词并发送回应
    for keyword, reply in call_mapping.items():
        if keyword.lower() in message_text:
            # 构建回复内容：@发送者 + 回应文本
            reply_content: List[At] = [
                At(user_id),  # @发送者
                f" {reply}"   # 回应内容（加空格分隔@和文本）
            ]
            # 调用框架发送方法，发送到对应的群
            send_group(group_id, reply_content)
            # 更新冷却时间
            cool_down_records[user_id] = now
            break  # 只响应第一个匹配的关键词


# 插件元信息与入口（框架通过此变量识别插件）
plugin = {
    "name": "astrbot_plugin_nm",  # 必须与插件文件夹名一致
    "version": "1.0.0",
    "description": "群聊中检测'叫爸爸''叫妈妈'等关键词并自动回应",
    "handlers": {
        "group_message": on_group_message  # 绑定群消息事件到处理函数
    }
}
