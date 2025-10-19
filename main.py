# -*- coding: utf-8 -*-
from typing import List
from datetime import datetime, timedelta
# 只导入确认存在的发送组件和方法（如果 send_group 也不存在，需替换为框架实际发送方法）
from astrbot.core.message.components import At
from astrbot.core.message import send_group

# 关键词与回应映射
call_mapping = {
    "叫爸爸": "爸爸～",
    "叫妈妈": "妈妈～",
    "叫哥哥": "哥哥～",
    "叫姐姐": "姐姐～"
}

# 冷却时间存储：{用户ID: 最后响应时间}
cool_down_records = {}
COOL_DOWN_SECONDS = 5


def on_group_message(raw_data: dict):
    """
    群消息处理函数（接收框架原始字典数据）
    旧版本框架通常将消息数据以字典形式传递，包含以下键：
    - "type": 消息类型（群聊为"group"）
    - "self_id": 机器人自身ID
    - "user_id": 发送者ID
    - "group_id": 群ID
    - "message_str": 消息文本
    """
    # 1. 仅处理群聊消息（通过原始数据的"type"判断）
    if raw_data.get("type") != "group":
        return

    # 2. 过滤机器人自己的消息
    if raw_data.get("user_id") == raw_data.get("self_id"):
        return

    # 3. 提取关键信息（从原始字典中获取）
    user_id = raw_data.get("user_id")
    group_id = raw_data.get("group_id")
    message_text = raw_data.get("message_str", "").strip().lower()

    # 4. 冷却时间检查
    now = datetime.now()
    last_time = cool_down_records.get(user_id, datetime.min)
    if (now - last_time).total_seconds() < COOL_DOWN_SECONDS:
        return

    # 5. 匹配关键词并回复
    for keyword, reply in call_mapping.items():
        if keyword.lower() in message_text:
            # 构建回复内容（@发送者 + 文本）
            reply_content: List[At] = [At(user_id), f" {reply}"]
            # 发送消息（调用框架发送方法）
            send_group(group_id, reply_content)
            # 更新冷却时间
            cool_down_records[user_id] = now
            break


# 插件注册（最简化形式，框架可能只需要识别处理函数）
plugin = {
    "name": "astrbot_plugin_nm",
    "handlers": {"group_message": on_group_message}
}
