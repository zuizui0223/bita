from __future__ import annotations

import ast
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "trait_architecture"


def _python_files() -> list[Path]:
    roots = (ROOT / "trait_architecture", ROOT / "scripts", ROOT / "examples")
    return sorted(path for root in roots if root.exists() for path in root.rglob("*.py"))


def _local_imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("trait_architecture."):
            modules.add(node.module.split(".", 1)[1].split(".", 1)[0])
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("trait_architecture."):
                    modules.add(alias.name.split(".", 1)[1].split(".", 1)[0])
    return modules


def test_active_python_surfaces_do_not_import_retired_modules() -> None:
    missing: list[str] = []
    for path in _python_files():
        for module in sorted(_local_imports(path)):
            if not (PACKAGE / f"{module}.py").exists() and not (PACKAGE / module / "__init__.py").exists():
                missing.append(f"{path.relative_to(ROOT)} -> trait_architecture.{module}")
    assert missing == []


def test_workflows_only_call_present_repository_scripts() -> None:
    missing: list[str] = []
    for workflow in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
        text = workflow.read_text(encoding="utf-8")
        for script in sorted(set(re.findall(r"scripts/[A-Za-z0-9_.-]+(?:\.py|\.sh)", text))):
            if not (ROOT / script).is_file():
                missing.append(f"{workflow.relative_to(ROOT)} -> {script}")
    assert missing == []


def test_active_workflows_do_not_write_to_retired_research_branches() -> None:
    violations: list[str] = []
    for workflow in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
        text = workflow.read_text(encoding="utf-8")
        if "analysis/pattern-expansion-v1" in text or "contents: write" in text:
            violations.append(str(workflow.relative_to(ROOT)))
    assert violations == []
