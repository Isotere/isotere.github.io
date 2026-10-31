#!/usr/bin/env python3
"""Check public Git identities without printing names or email addresses."""

import re
import subprocess
import sys


class PrivacyError(Exception):
    pass


NOREPLY = re.compile(
    r"(?:[0-9]+\+)?([a-z0-9](?:[a-z0-9-]*[a-z0-9])?(?:\[bot\])?)"
    r"@users\.noreply\.github\.com",
    re.IGNORECASE,
)
OBJECT_ID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")


def git(*arguments):
    result = subprocess.run(
        ["git", *arguments], capture_output=True, text=True, check=False
    )
    if result.returncode:
        raise PrivacyError("Не удалось прочитать необходимые данные Git.")
    return result.stdout


def public_handle(email):
    match = NOREPLY.fullmatch(email)
    return match[1] if match else None


def identity_problem(name, email, role):
    if role == "committer" and name == "GitHub" and email == "noreply@github.com":
        return None
    handle = public_handle(email)
    if handle is None:
        return "email должен быть GitHub noreply"
    if name.casefold() != handle.casefold():
        return "имя должно совпадать с публичным логином из noreply-email"
    return None


def check_identity():
    for role, variable in (
        ("author", "GIT_AUTHOR_IDENT"),
        ("committer", "GIT_COMMITTER_IDENT"),
    ):
        identity = git("var", variable).strip()
        match = re.fullmatch(r"(.*) <([^<>]+)> [0-9]+ [+-][0-9]{4}", identity)
        if not match:
            raise PrivacyError("Не удалось определить Git identity.")
        problem = identity_problem(match[1], match[2], role)
        if problem:
            raise PrivacyError(f"{role}: {problem}. Выполни make git-privacy.")


def check_commits(revisions):
    metadata = git(
        "log", "--format=%H%x00%an%x00%ae%x00%cn%x00%ce", *revisions, "--"
    )
    count = 0
    for line in metadata.splitlines():
        fields = line.split("\0")
        if len(fields) != 5:
            raise PrivacyError("Не удалось разобрать метаданные коммита.")
        commit, author_name, author_email, committer_name, committer_email = fields
        for role, name, email in (
            ("author", author_name, author_email),
            ("committer", committer_name, committer_email),
        ):
            problem = identity_problem(name, email, role)
            if problem:
                raise PrivacyError(f"Коммит {commit[:12]}, {role}: {problem}.")
        count += 1
    return count


def check_history():
    has_head = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"],
        capture_output=True,
        check=False,
    ).returncode == 0
    return check_commits(["HEAD"]) if has_head else 0


def check_push(stream):
    for line in stream:
        fields = line.split()
        if len(fields) != 4:
            raise PrivacyError("Не удалось разобрать список отправляемых refs.")
        _, local_oid, _, remote_oid = fields
        if not OBJECT_ID.fullmatch(local_oid) or not OBJECT_ID.fullmatch(remote_oid):
            raise PrivacyError("Получен некорректный идентификатор Git object.")
        if set(local_oid) == {"0"}:
            continue
        revisions = [local_oid]
        if set(remote_oid) != {"0"}:
            remote_known = subprocess.run(
                ["git", "cat-file", "-e", f"{remote_oid}^{{commit}}"],
                capture_output=True,
                check=False,
            ).returncode == 0
            if remote_known:
                revisions.append(f"^{remote_oid}")
        check_commits(revisions)


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("identity", "history", "pre-push"):
        print("Usage: git_privacy.py identity|history|pre-push", file=sys.stderr)
        return 2
    try:
        if sys.argv[1] == "identity":
            check_identity()
        elif sys.argv[1] == "history":
            count = check_history()
            print(f"Проверено коммитов: {count}.")
        else:
            check_push(sys.stdin)
    except (PrivacyError, OSError) as error:
        if isinstance(error, PrivacyError):
            print(f"Проверка приватности Git: {error}", file=sys.stderr)
        else:
            print("Не удалось запустить проверку приватности Git.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
