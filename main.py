# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

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


def group_message_handler(data: dict):
    """
    群消息处理函数（旧版本框架通用格式）
    data字典包含：user_id(发送者ID)、group_id(群ID)、message(消息文本)、self_id(机器人ID)
    """
    # 1. 过滤非群聊消息（如果框架已确保只传群消息，可省略）
    if data.get("message_type") != "group":
        return

    # 2. 过滤机器人自己的消息
    if data.get("user_id") == data.get("self_id"):
        return

    # 3. 提取信息
    user_id = data.get("user_id")
    group_id = data.get("group_id")
    message_text = data.get("message", "").strip().lower()

    # 4. 冷却检查
    now = datetime.now()
    last_time = cool_down_records.get(user_id, datetime.min)
    if (now - last_time).total_seconds() < COOL_DOWN_SECONDS:
        return

    # 5. 匹配关键词并回复
    for keyword, reply in call_mapping.items():
        if keyword.lower() in message_text:
            # 构建回复内容（用原始格式@用户，避免依赖At组件）
            # 旧版本框架通常用 "@[user_id]" 表示艾特
            reply_text = f"@[{user_id}] {reply}"
            
            # 最原始的发送方式：通过全局bot对象发送（旧框架普遍支持）
            from astrbot import bot  # 假设存在全局bot对象
            bot.send_group_message(group_id, reply_text)  # 旧框架常用发送方法名
            
            # 更新冷却时间
            cool_down_records[user_id] = now
            break


# 插件注册（旧版本框架最简单的识别方式）
plugin = {
    "name": "astrbot_plugin_nm",
    "events": {
        "group_message": group_message_handler  # 绑定群消息事件
    }
}
