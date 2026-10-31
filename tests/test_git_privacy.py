import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[1]
PUBLIC_EMAIL = "123456+sample-user@users.noreply.github.com"
PRIVATE_EMAIL = "private@example.invalid"
PRIVATE_NAME = "Private Person"


class GitPrivacyTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name) / "repository"
        self.root.mkdir()
        self.environment = os.environ.copy()
        for name in list(self.environment):
            if name.startswith("GIT_") or name == "EMAIL":
                self.environment.pop(name)
        self.environment["GIT_CONFIG_GLOBAL"] = os.devnull
        self.environment["GIT_CONFIG_SYSTEM"] = os.devnull
        self.command("git", "init", "--quiet", "--initial-branch=master")
        shutil.copytree(PROJECT / "scripts", self.root / "scripts")
        shutil.copytree(PROJECT / ".githooks", self.root / ".githooks")
        for hook in (self.root / ".githooks").iterdir():
            hook.chmod(0o755)
        self.command(sys.executable, "scripts/setup_git_privacy.py", "--email", PUBLIC_EMAIL)
        (self.root / "example.txt").write_text("synthetic example\n")
        self.command("git", "add", "example.txt")

    def command(self, *arguments, overrides=None, check=True, data=None):
        environment = self.environment | (overrides or {})
        result = subprocess.run(
            arguments,
            cwd=self.root,
            env=environment,
            capture_output=True,
            text=True,
            input=data,
            check=False,
        )
        if check and result.returncode:
            self.fail(f"Fixture command failed: {result.stderr}")
        return result

    def assert_private_values_hidden(self, result):
        self.assertNotIn(PRIVATE_EMAIL, result.stdout + result.stderr)
        self.assertNotIn(PRIVATE_NAME, result.stdout + result.stderr)

    def test_setup_configures_all_roles_and_reuses_existing_identity(self):
        for role in ("user", "author", "committer"):
            self.assertEqual(self.command("git", "config", f"{role}.name").stdout.strip(), "sample-user")
            self.assertEqual(self.command("git", "config", f"{role}.email").stdout.strip(), PUBLIC_EMAIL)
        self.command(sys.executable, "scripts/setup_git_privacy.py")
        self.assertEqual(self.command("git", "config", "core.hooksPath").stdout.strip(), ".githooks")

    def test_valid_commit_and_history_pass(self):
        self.command("git", "commit", "--quiet", "-m", "Synthetic public commit")
        self.command(sys.executable, "scripts/git_privacy.py", "history")

    def test_author_and_committer_environment_overrides_are_blocked(self):
        for variable in ("GIT_AUTHOR_EMAIL", "GIT_COMMITTER_EMAIL"):
            with self.subTest(variable=variable):
                result = self.command(
                    "git", "commit", "--quiet", "-m", "Synthetic blocked commit",
                    overrides={variable: PRIVATE_EMAIL}, check=False,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assert_private_values_hidden(result)

    def test_private_names_are_blocked_even_with_noreply(self):
        for variable in ("GIT_AUTHOR_NAME", "GIT_COMMITTER_NAME"):
            with self.subTest(variable=variable):
                result = self.command(
                    "git", "commit", "--quiet", "-m", "Synthetic blocked name",
                    overrides={variable: PRIVATE_NAME}, check=False,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assert_private_values_hidden(result)

    def test_explicit_private_author_is_blocked(self):
        result = self.command(
            "git", "commit", "--quiet", "-m", "Synthetic explicit author",
            "--author", f"{PRIVATE_NAME} <{PRIVATE_EMAIL}>", check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assert_private_values_hidden(result)

    def test_push_checks_intermediate_commits(self):
        self.command("git", "commit", "--quiet", "-m", "Synthetic base")
        base = self.command("git", "rev-parse", "HEAD").stdout.strip()
        tree = self.command("git", "rev-parse", "HEAD^{tree}").stdout.strip()
        private_commit = self.command(
            "git", "commit-tree", tree, "-p", base, "-m", "Synthetic private fixture",
            overrides={"GIT_AUTHOR_EMAIL": PRIVATE_EMAIL, "GIT_AUTHOR_NAME": PRIVATE_NAME},
        ).stdout.strip()
        corrected_commit = self.command(
            "git", "commit-tree", tree, "-p", private_commit, "-m", "Synthetic public tip",
        ).stdout.strip()
        for remote in (base, "0" * 40, "f" * 40):
            with self.subTest(remote_kind="known" if remote == base else "new-or-unknown"):
                result = self.command(
                    sys.executable, "scripts/git_privacy.py", "pre-push",
                    data=f"refs/heads/master {corrected_commit} refs/heads/master {remote}\n",
                    check=False,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assert_private_values_hidden(result)

    def test_github_service_committer_is_allowed(self):
        self.command(
            "git", "commit", "--quiet", "-m", "Synthetic web commit",
            overrides={"GIT_COMMITTER_NAME": "GitHub", "GIT_COMMITTER_EMAIL": "noreply@github.com"},
        )
        self.command(sys.executable, "scripts/git_privacy.py", "history")

    def test_other_hooks_path_is_preserved(self):
        self.command("git", "config", "core.hooksPath", "other-hooks")
        result = self.command(sys.executable, "scripts/setup_git_privacy.py", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.command("git", "config", "core.hooksPath").stdout.strip(), "other-hooks")

    def test_active_default_hooks_are_preserved(self):
        self.command("git", "config", "--unset", "core.hooksPath")
        hook = self.root / ".git/hooks/pre-commit"
        hook.write_text("#!/bin/sh\nexit 0\n")
        hook.chmod(0o755)
        result = self.command(sys.executable, "scripts/setup_git_privacy.py", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(hook.read_text(), "#!/bin/sh\nexit 0\n")


if __name__ == "__main__":
    unittest.main()
