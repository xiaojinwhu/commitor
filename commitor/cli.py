import os
import subprocess
from functools import partial
from pathlib import Path
from typing import Optional

import openai
import toml
import typer
from rich.console import Console
from rich.syntax import Syntax

from commitor.prompt import get_system_prompt

app = typer.Typer()
console = Console()

config_path = Path.home() / ".commitor_config.toml"


def load_config():
    if config_path.exists():
        return toml.load(config_path)
    else:
        return {}


def save_config(config):
    with open(config_path, "w") as f:
        toml.dump(config, f)


def get_diff():
    """获取本地文件的 git diff 输出"""
    diff_output = subprocess.run(
        ["git", "diff", "--staged"], capture_output=True, text=True
    ).stdout
    return diff_output


def get_commit_message(
    diff, api_key, model, base_url=None, emoji=True, full_gitmoji=False
):
    """使用大模型生成 commit 信息"""

    openai.api_key = api_key
    openai.base_url = base_url

    response = openai.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": get_system_prompt(emoji, full_gitmoji),
            },
            {
                "role": "user",
                "content": f"这里是 `git diff` 的输出：\n{diff}",
            },
        ],
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.3,
    )
    commit_msg = response.choices[0].message.content.strip()
    return commit_msg


@app.command()
def gen(
    syntax_highlight: bool = typer.Option(
        False, "--highlight/--no-highlight", help="是否高亮显示 diff 输出"
    ),
):
    """根据本地 git diff 输出自动生成 commit 信息"""
    diff = get_diff()
    if syntax_highlight:
        diff = Syntax(diff, "diff", background_color="default")
    console.print(diff)

    config = load_config()
    if not config:
        console.print(
            "API is not configured. Please run 'commitor config' first.", style="red"
        )
        raise typer.Exit()

    commit_msg = get_commit_message(
        diff,
        model=config["model"],
        api_key=config["api_key"],
        base_url=config["base_url"],
    )
    console.print(f"\n[bold green]Generated commit message:[/bold green] {commit_msg}")


@app.command()
def config(
    model: str = typer.Option(
        ..., "--model", "-m", help="指定使用的大模型", prompt="Model"
    ),
    api_key: Optional[str] = typer.Option(
        None, "--api_key", help="API Key", prompt="API Key"
    ),
    base_url: Optional[str] = typer.Option(
        None, "--base_url", help="模型 URL", prompt="Private Model URL"
    ),
):
    """配置使用的大模型及相关 API"""
    config = load_config()
    config["model"] = model
    config["api_key"] = api_key
    config["base_url"] = base_url
    save_config(config)
    console.print(f"[bold green]Configuration updated:[/bold green] {config}")


@app.command()
def help():
    """显示帮助信息"""
    console.print("用法:")
    console.print("  commitor gen       根据本地 git diff 输出自动生成 commit 信息")
    console.print("  commitor config [OPTIONS]    配置使用的大模型及相关 API")
    console.print("  commitor help                显示帮助信息")
    console.print("\n选项:")
    console.print("  --highlight, --no-highlight  是否高亮显示 diff 输出")
    console.print("  --model MODEL                指定使用的大模型 [required]")
    console.print("  --api_key API_KEY            API Key [required]")
    console.print("  --base_url BASE_URL          模型 URL [required]")


if __name__ == "__main__":
    app()
