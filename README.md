# 称呼回应插件（call_respond）

## 简介
适用于 AstrBot 框架的 QQ 机器人插件，自动检测群聊关键词并@回应。

## 适用环境
- 框架：AstrBot ≥ 0.5.0（兼容新旧版本，v1.2.1 修复旧版本导入错误）
- Python：3.8+
- 后端：OneBot V11 协议（go-cqhttp、NapCat 等）

## 安装步骤
1. 将 `call_respond` 文件夹放入 AstrBot 的 `data/plugins/` 目录。
2. 重启机器人：`astrbot run`。

## 使用方法
| 关键词   | 回应内容                |
|----------|-------------------------|
| 叫爸爸   | @用户 哎，乖儿子/女儿～ |
| 叫妈妈   | @用户 哎，宝贝～        |
| 叫哥哥   | @用户 来啦，小老弟/小老妹～ |
| 叫姐姐   | @用户 嗯呢，小可爱～    |

## 版本兼容说明
- v1.2.1：修复旧版本 AstrBot 中 `GroupMessageEvent` 导入错误，改用 `GroupMessage` 兼容。
- 若使用 AstrBot ≥ 0.6.0，可直接使用此版本，无需额外修改。

## 常见问题
1. **Q：导入错误 `cannot import name 'GroupMessageEvent'`？**  
   A：已在 v1.2.1 中修复，确保使用本版本代码即可。
