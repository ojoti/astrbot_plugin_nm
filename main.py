# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

# 旧框架最原始的插件基类（必须正确导入，否则框架找不到）
# 若此导入失败，尝试 from astrbot.core.Plugin import Plugin
from astrbot.Plugin import Plugin  # 框架强制要求的基类


# 类名必须符合框架预期（通常与插件名相关，且是模块中唯一的公共类）
class AstrbotPluginNm(Plugin):  # 类名与插件名"astrbot_plugin_nm"对应（驼峰式）
    def __init__(self, bot):
        super().__init__(bot)  # 必须调用父类构造函数，传入bot实例
        self.call_mapping = {
            "叫爸爸": "爸爸～",
            "叫妈妈": "妈妈～",
            "叫哥哥": "哥哥～",
            "叫姐姐": "姐姐～"
        }
        self.cool_down = {}
        self.cool_seconds = 5

    # 框架硬编码的群消息处理方法名（必须是这个名字，否则不触发）
    def group_message(self, event):  # 注意方法名是 group_message，而非 on_group_message
        # event 是框架传递的原始事件对象，包含消息数据
        user_id = event.user_id
        group_id = event.group_id
        msg_text = event.message.strip().lower()

        # 过滤机器人自己的消息（event.self_id 是机器人ID）
        if user_id == event.self_id:
            return

        # 冷却检查
        now = datetime.now()
        last_time = self.cool_down.get(user_id, datetime.min)
        if (now - last_time).total_seconds() < self.cool_seconds:
            return

        # 匹配关键词并回复
        for keyword, reply in self.call_mapping.items():
            if keyword.lower() in msg_text:
                # 构建带@的回复（旧框架的艾特格式）
                reply_text = f"@{user_id} {reply}"
                # 通过父类传入的 bot 实例发送消息（框架固定发送方法）
                self.bot.send_group(group_id, reply_text)
                self.cool_down[user_id] = now
                break


# 模块中必须只有这一个公共类，且类名符合框架扫描规则
# 框架会自动实例化此类，无需额外注册代码
