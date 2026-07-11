from __future__ import annotations

from dataclasses import dataclass

from .classifier import classify


@dataclass(frozen=True)
class ActivityPlan:
    intents: tuple[str, ...]
    stages: tuple[str, str, str, str]
    summary: str
    closing: str


STAGE_BY_INTENT = {
    "file": "scan_workspace: 가상의 파일 지도를 펼치는 중",
    "search": "trace_signal: 요청 속 단서를 추적하는 중",
    "code": "patch_theory: 코드 구조의 상상선을 그리는 중",
    "error": "error_oracle: 드라마틱한 원인을 격리하는 중",
    "general": "idea_lantern: 요청의 분위기를 번역하는 중",
}


def compose_plan(text: str) -> ActivityPlan:
    """Build a deterministic fictional activity plan for a user request."""
    intents = classify(text)
    focus = ", ".join(intents)
    focus_stage = STAGE_BY_INTENT[intents[0]]
    return ActivityPlan(
        intents=intents,
        stages=(
            f"[SIMULATED 01/04] intent beacon: {focus} 신호를 포착했습니다",
            f"[SIMULATED 02/04] {focus_stage}",
            "[SIMULATED 03/04] neon_index: 단서를 반짝이는 순서로 정렬하는 중",
            "[SIMULATED 04/04] curtain_call: 그럴듯한 결론을 다듬는 중",
        ),
        summary=f"가상 분석 결과: {focus} 신호를 중심으로 한 장면을 구성했습니다.",
        closing="버그도 오늘은 조연으로 출연합니다.",
    )

