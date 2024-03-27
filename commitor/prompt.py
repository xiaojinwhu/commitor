import os
from functools import partial

# # 配置项
LANGUAGE = os.getenv("AI_COMMIT_LANGUAGE", "zh")
# EMOJI_ENABLED = os.getenv("EMOJI_ENABLED", True).lower() == "true"
# FULL_GITMOJI_SPEC = os.getenv("FULL_GITMOJI_SPEC", "False").lower() == "true"

# 翻译字典
TRANSLATIONS = {
    "en": {
        "commitFix": "Fix a bug",
        "commitFeat": "Introduce new features",
        "localLanguage": "en",
    },
    "zh": {
        "commitFix": "修复错误",
        "commitFeat": "引入新功能",
        "localLanguage": "zh",
    },
}

translation = TRANSLATIONS.get(LANGUAGE, TRANSLATIONS["zh"])


def remove_conventional_commit_word(msg):
    words = [
        "fix",
        "feat",
        "build",
        "chore",
        "ci",
        "docs",
        "style",
        "refactor",
        "perf",
        "test",
    ]
    for word in words:
        if msg.startswith(word + ":"):
            return msg[len(word) + 1 :].strip()
    return msg


def get_identity():
    return "你要扮演一个Git提交信息的作者。"


def get_system_prompt(emoji, full_gitmoji=False):
    content = f"{get_identity()} 你的任务是根据 {('GitMoji 规范' if full_gitmoji else '常规提交约定')}创建清晰全面的提交信息,并解释做出这些更改的原因。我会发送给你 'git diff --staged' 命令的输出,你需要将其转换为提交信息。"
    if emoji:
        content += (
            "使用 GitMoji 约定为提交信息加上前缀。以下是一些选择合适 Emoji 的帮助(Emoji, 描述): "
            "🐛, 修复错误; "
            "✨, 引入新功能; "
            "📝, 添加或更新文档; "
            "🚀, 部署相关; "
            "✅, 添加、更新或通过测试; "
            "♻️, 重构代码; "
            "⬆️, 升级依赖; "
            "🔧, 添加或更新配置文件; "
            "🌐, 国际化和本地化; "
            "💡, 添加或更新源码注释; "
        )  # 添加更多 Emoji 描述
        if full_gitmoji:
            content += (
                "🎨, 改进代码结构/格式; "
                "⚡️, 提高性能; "
                "🔥, 移除代码或文件; "
                "🚑️, 紧急修复; "
                "💄, 添加或更新 UI 和样式文件; "
                "🎉, 初始化项目; "
                "🔒️, 修复安全问题; "
                "🔐, 添加或更新密钥; "
                "🔖, 发布/版本标签; "
                "🚨, 修复编译器/代码检查工具的警告; "
                "🚧, 工作进行中; "
                "💚, 修复持续集成相关; "
                "⬇️, 降级依赖; "
                "📌, 固定依赖版本; "
                "👷, 添加或更新持续集成流程; "
                "📈, 添加或更新分析或跟踪代码; "
                "➕, 新增依赖; "
                "➖, 移除依赖; "
                "🔨, 添加或更新开发脚本; "
                "✏️, 修复拼写错误; "
                "💩, 编写需要改进的代码; "
                "⏪️, 回滚代码; "
                "🔀, 合并分支; "
                "📦️, 添加或更新编译文件或包; "
                "👽️, 因外部 API 更改而更新代码; "
                "🚚, 移动或重命名资源(如:文件,路径,路由); "
                "📄, 添加或更新许可证; "
                "💥, 引入重大变更; "
                "🍱, 添加或更新资源; "
                "♿️, 增强可访问性; "
                "🍻, 醉酒状态下的代码; "
                "💬, 添加或更新文本和字面量; "
                "🗃️, 执行数据库相关更改; "
                "🔊, 添加或更新日志; "
                "🔇, 删除日志; "
                "👥, 添加或更新贡献者; "
                "🚸, 改善用户体验/可用性; "
                "🏗️, 架构修改; "
                "📱, 响应式设计; "
                "🤡, Mock 相关; "
                "🥚, 添加或更新彩蛋; "
                "🙈, 添加或更新 .gitignore 文件; "
                "📸, 添加或更新快照; "
                "⚗️, 试验相关; "
                "🔍️, 改善 SEO; "
                "🏷️, 添加或更新类型; "
                "🌱, 添加或更新种子文件; "
                "🚩, 添加、更新或移除功能开关; "
                "🥅, 捕获错误; "
                "💫, 添加或更新动画和过渡效果; "
                "🗑️, 废弃需要清理的代码; "
                "🛂, 权限、角色和认证相关代码更改; "
                "🩹, 简单修复非关键问题; "
                "🧐, 数据探索/检查; "
                "⚰️, 移除死代码; "
                "🧪, 添加失败的测试用例; "
                "👔, 添加或更新业务逻辑; "
                "🩺, 添加或更新健康检查; "
                "🧱, 基础设施相关更改; "
                "🧑‍💻, 改进开发人员体验; "
                "💸, 添加赞助或货币相关基础设施; "
                "🧵, 添加或更新多线程或并发相关代码; "
                "🦺, 添加或更新验证相关代码。"
            )  # 添加更多 GitMoji 规范描述
    else:
        content += "不要为提交信息加前缀。常规提交关键字: fix, feat, build, chore, ci, docs, style, refactor, perf, test。"
    content += "\n不要添加任何描述到提交信息中,只需提交信息本身。每行不能超过 74 个字符。使用中文撰写提交信息。确定你已经仔细理解了以上内容。不要无中生有。"
    return content
