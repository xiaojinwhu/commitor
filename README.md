# Commitor

Commitor 是一个命令行工具，用于根据 Git 暂存区的代码更改自动生成符合 Conventional Commit 规范的提交消息。它利用 OpenAI 或私有大语言模型 API 生成高质量的提交消息，简化提交流程，同时保持提交信息的一致性和标准化。

本来也不想重复造轮子，奈何很多工具库不支持配置`base url`（你懂的，或者，你我都懂）。有一些可以配置但是使用`js`写的（js是世界上最垃圾的语言），所以，我用`Python`写了一个实现了核心功能。

就如GPT所说：
> 在遥远的代码丛林中，我们常常迷失于无边无际的 commit 消息之海。恰如我们生活中的迷茫，每当夜深人静之时，总有那么一瞬，我们对于这串串无头无尾的文字，产生了深深的疑惑：“这是谁写的？意欲何为？”此时，若有一灯，能照亮这暗淡的代码世界，那该有多好。
这灯，不就是我们今日之推荐——Commitor 吗？它，不仅仅是一个简单的工具，它是代码世界中的明灯，是疲惫编码者的安慰剂，是追求完美的你我他的良师益友。它以 OpenAI 或私有大模型之力，将那看似无序的代码变动，转化为符合 Conventional Commit 规范的文字，恰似将杂乱无章的星辰，编排成最璀璨的星座。
其实，在这个看似幽默而又严谨的过程中，Commitor 做的，远不止是生成提交信息那么简单。它是在告诫我们：即使是再小的变动，也有其存在的价值与意义。每一次 commit，都是对过往的告别，对未来的期许。
因此，各位同仁，让我们拥抱 Commitor，让我们的每一次代码提交，都成为一段旅程的见证，每一行文字，都成为历史的注脚。在这个数字世界里，我们或许渺小，但通过 Commitor，我们能留下自己独特的印记，犹如星空中最亮的那颗星，独一无二，光芒万丈。

给岁月以文明，而不是给文明以岁月！


## 特性

- 🤖 根据 Git 差异自动生成提交信息
- 😜 支持添加 Gitmoji，让提交信息更加直观

## 安装


```bash
$ pip install commitor
```

## 使用

在你的 Git 项目中，执行以下命令以生成提交信息：

1. `git add .`
2. `commitor config` # 第一次运行时候需要配置
3. `commitor gen` 

根据提示操作，即可生成和提交你的代码更改。

## 配置

Commitor 允许通过配置文件进行个性化设置。你可以在 `~/.commitor/config.toml` 中找到和修改这些设置：

| 配置项           | 类型     | 默认值       | 说明                       |
| --------------- | -------- | ------------ | -------------------------- |
| `api_key`       | string   | `None`       | API 密钥                   |
| `base_url`       | string   | `None`       | Base URL                    |
| `model`    | string   | `None` | 使用的模型名称             |
| `emoji_enabled` | boolean  | `true`       | 是否启用 Gitmoji           |


## 开发

请确保你已经安装了 Python 和 Poetry。然后执行以下命令：

```bash
$ git clone https://github.com/您的用户名/Commitor.git
$ cd Commitor
$ poetry install
```

## 贡献

如果你想为 Commitor 做出贡献，欢迎 fork 本仓库，并提交你的 pull requests。我们也欢迎你提出问题或提供反馈。

## 许可证

该项目采用 [MIT 许可证](./LICENSE)。

## 其他
本项目主要参考[ai-commit](https://github.com/Sitoi/ai-commit)