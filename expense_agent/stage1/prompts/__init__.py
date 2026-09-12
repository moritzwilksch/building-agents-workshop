"""Load Stage 1 prompts from their editable text files."""

from pathlib import Path

PROMPTS_DIR = Path(__file__).parent
SYSTEM_PROMPT = (PROMPTS_DIR / "system.md").read_text(encoding="utf-8").strip()
HANDBOOK_PROMPT = (PROMPTS_DIR / "handbook.md").read_text(encoding="utf-8")
