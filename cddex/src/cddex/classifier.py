from __future__ import annotations

KEYWORDS: dict[str, tuple[str, ...]] = {
    "file": ("파일", "폴더", "readme", "문서", "file", "directory", "folder"),
    "search": ("검색", "찾아", "찾기", "search", "find", "look up"),
    "code": ("코드", "함수", "패치", "리팩터", "code", "function", "patch", "refactor"),
    "error": ("오류", "에러", "버그", "실패", "error", "bug", "failure", "exception"),
}


def classify(text: str) -> tuple[str, ...]:
    """Classify a request without inspecting anything outside the supplied text."""
    lowered = text.casefold()
    intents = tuple(
        intent for intent, words in KEYWORDS.items() if any(word in lowered for word in words)
    )
    return intents or ("general",)

