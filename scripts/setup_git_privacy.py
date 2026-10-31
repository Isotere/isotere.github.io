#!/usr/bin/env python3
"""Configure privacy locally and preserve unrelated hooks and global settings."""

import argparse
import os
from pathlib import Path
import subprocess
import sys

from git_privacy import PrivacyError, public_handle


def configure(email=""):
    root = Path(__file__).resolve().parents[1]

    def run(*arguments):
        return subprocess.run(
            ["git", "-C", str(root), *arguments],
            capture_output=True,
            text=True,
            check=False,
        )

    def read(*arguments):
        result = run(*arguments)
        if result.returncode:
            raise PrivacyError("Не удалось прочитать настройки Git.")
        return result.stdout.strip()

    if read("rev-parse", "--is-bare-repository") != "false":
        raise PrivacyError("Ожидается обычный рабочий Git-репозиторий.")
    if Path(read("rev-parse", "--show-toplevel")).resolve() != root:
        raise PrivacyError("Настройки можно применить только к этому репозиторию.")
    configured_hooks = run("config", "--get", "core.hooksPath")
    if configured_hooks.returncode not in (0, 1):
        raise PrivacyError("Не удалось проверить текущие hooks.")
    if configured_hooks.returncode == 0:
        if configured_hooks.stdout.strip() != ".githooks":
            raise PrivacyError("Другой core.hooksPath сохранён. Сначала согласуй совместную работу hooks.")
    else:
        default_hooks = Path(read("rev-parse", "--git-path", "hooks"))
        if not default_hooks.is_absolute():
            default_hooks = root / default_hooks
        if any(
            path.is_file() and os.access(path, os.X_OK) and not path.name.endswith(".sample")
            for path in default_hooks.glob("*")
        ):
            raise PrivacyError("Существующие активные Git hooks сохранены.")
    for name in ("pre-commit", "pre-push"):
        path = root / ".githooks" / name
        if not path.is_file() or not os.access(path, os.X_OK):
            raise PrivacyError("Проектные hooks отсутствуют или не имеют права исполнения.")

    email = email or run("config", "user.email").stdout.strip()
    handle = public_handle(email)
    if handle is None:
        raise PrivacyError("Укажи свой GitHub noreply-email через GIT_NOREPLY_EMAIL; значение не печатается.")
    settings = {
        "user.name": handle,
        "user.email": email,
        "author.name": handle,
        "author.email": email,
        "committer.name": handle,
        "committer.email": email,
        "user.useConfigOnly": "true",
        "core.hooksPath": ".githooks",
    }
    for key, value in settings.items():
        if run("config", "--local", key, value).returncode:
            raise PrivacyError("Не удалось сохранить локальные настройки Git.")
    print("Локальная публичная Git identity и проектные hooks настроены.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", default="")
    arguments = parser.parse_args()
    try:
        configure(arguments.email)
    except (PrivacyError, OSError) as error:
        print(str(error) if isinstance(error, PrivacyError) else "Не удалось настроить Git.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
