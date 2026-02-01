#!/usr/bin/env python3
"""
PreToolUse Hook: Bash 명령어 검증
위험한 명령어를 차단하고 권장 사항을 제안합니다.
"""

import json
import re
import sys


# 차단할 위험한 명령어 패턴
DANGEROUS_PATTERNS = [
    (r"\brm\s+-rf\s+/", "루트 디렉토리 삭제는 금지됩니다"),
    (r"\brm\s+-rf\s+\*", "와일드카드 삭제는 위험합니다. 구체적인 경로를 지정하세요"),
    (r"\bsudo\s+rm", "sudo로 파일 삭제는 신중히 검토가 필요합니다"),
    (r":(){.*};:", "Fork bomb이 감지되었습니다"),
    (r">\s*/dev/sd[a-z]", "디스크 직접 쓰기는 금지됩니다"),
    (r"\bdd\s+if=.*of=/dev/", "dd로 디바이스 쓰기는 위험합니다"),
]

# 권장사항 패턴
RECOMMENDATION_PATTERNS = [
    (
        r"\bgrep\b(?!.*\|.*rg)",
        "권장: 'grep' 대신 'rg' (ripgrep)를 사용하면 더 빠릅니다"
    ),
    (
        r"\bfind\s+\S+\s+-name\b",
        "권장: 'find -name' 대신 'rg --files -g pattern'이 더 효율적입니다"
    ),
    (
        r"\bcat\s+\S+\s*\|\s*grep",
        "권장: 'cat | grep' 대신 'grep file' 또는 'rg pattern file'을 사용하세요"
    ),
]


def validate_command(command: str) -> tuple[bool, str]:
    """
    명령어를 검증합니다.
    반환: (차단여부, 메시지)
    """
    # 위험한 패턴 확인
    for pattern, message in DANGEROUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return True, f"[보안] {message}"

    return False, ""


def get_recommendations(command: str) -> list[str]:
    """권장사항을 반환합니다."""
    recommendations = []
    for pattern, message in RECOMMENDATION_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            recommendations.append(message)
    return recommendations


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}", file=sys.stderr)
        sys.exit(1)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    command = tool_input.get("command", "")

    if tool_name != "Bash" or not command:
        sys.exit(0)

    # 위험한 명령어 확인
    should_block, block_message = validate_command(command)
    if should_block:
        print(block_message, file=sys.stderr)
        sys.exit(2)  # 종료 코드 2: 차단하고 stderr를 Claude에게 표시

    # 권장사항 확인 (차단하지 않음)
    recommendations = get_recommendations(command)
    if recommendations:
        # JSON 출력으로 권장사항 표시 (차단하지 않음)
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": "\n".join(recommendations)
            }
        }
        print(json.dumps(output, ensure_ascii=False))

    sys.exit(0)


if __name__ == "__main__":
    main()
