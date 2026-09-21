from pathlib import Path

from rx50t_crypto_gui import choose_default_port


REPO_ROOT = Path(__file__).resolve().parents[2]
TEXT_SUFFIXES = {".md", ".py", ".ps1", ".tcl", ".xdc", ".txt"}
FORBIDDEN_LEGACY_STRINGS = (
    "D:\\FPGAhanjia\\jichuangsai",
    "D:/FPGAhanjia/jichuangsai",
    "COM12",
)


def test_public_tree_has_no_legacy_machine_specific_paths() -> None:
    roots = [
        REPO_ROOT / "README.md",
        REPO_ROOT / "docs",
        REPO_ROOT / "contest_project" / "constraints",
        REPO_ROOT / "contest_project" / "scripts",
        REPO_ROOT / "contest_project" / "tools",
    ]

    offenders: list[str] = []

    for root in roots:
        paths = [root] if root.is_file() else sorted(p for p in root.rglob("*") if p.is_file())
        for path in paths:
            if path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            if path == Path(__file__):
                continue

            text = path.read_text(encoding="utf-8")
            if any(marker in text for marker in FORBIDDEN_LEGACY_STRINGS):
                offenders.append(str(path.relative_to(REPO_ROOT)))

    assert offenders == []


def test_default_port_selection_is_unambiguous() -> None:
    assert choose_default_port("", []) == ""
    assert choose_default_port("", ["COM7"]) == "COM7"
    assert choose_default_port("", ["COM7", "COM8"]) == ""
    assert choose_default_port("COM8", ["COM7", "COM8"]) == "COM8"
