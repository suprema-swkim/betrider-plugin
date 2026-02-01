#!/usr/bin/env python3
"""
PreToolUse Hook: 파일 쓰기/편집 검증
민감한 파일이나 중요한 설정 파일 수정을 감지합니다.
"""

import json
import os
import re
import sys


# 보호할 파일 패턴
PROTECTED_PATTERNS = [
    (r"\.env$", "환경 변수 파일"),
    (r"\.env\.local$", "로컬 환경 변수 파일"),
    (r"credentials\.json$", "인증 정보 파일"),
    (r"secrets\.json$", "비밀 정보 파일"),
    (r"\.pem$", "인증서 파일"),
    (r"\.key$", "키 파일"),
    (r"id_rsa", "SSH 키 파일"),
]

# 경고만 표시할 파일 패턴
WARNING_PATTERNS = [
    (r"package\.json$", "패키지 설정 파일 - 의존성 변경을 확인하세요"),
    (r"package-lock\.json$", "잠금 파일 - 자동 생성되어야 합니다"),
    (r"\.gitignore$", "Git 무시 파일 - 중요한 파일이 노출될 수 있습니다"),
    (r"tsconfig\.json$", "TypeScript 설정 - 빌드에 영향을 줍니다"),
    (r"webpack\.config\.", "Webpack 설정 - 빌드에 영향을 줍니다"),
]


def check_file_path(file_path: str) -> tuple[bool, str, bool]:
    """
    파일 경로를 확인합니다.
    반환: (차단여부, 메시지, 경고여부)
    """
    # 경로 정규화
    normalized_path = os.path.basename(file_path.lower())

    # 보호된 파일 확인
    for pattern, description in PROTECTED_PATTERNS:
        if re.search(pattern, file_path, re.IGNORECASE):
            return True, f"[보안] {description} 수정이 감지되었습니다: {file_path}", False

    # 경고 파일 확인
    for pattern, description in WARNING_PATTERNS:
        if re.search(pattern, file_path, re.IGNORECASE):
            return False, f"[주의] {description}: {file_path}", True

    return False, "", False


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}", file=sys.stderr)
        sys.exit(1)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    if tool_name not in ["Write", "Edit"] or not file_path:
        sys.exit(0)

    # 파일 경로 확인
    should_block, message, is_warning = check_file_path(file_path)

    if should_block:
        print(message, file=sys.stderr)
        sys.exit(2)

    if is_warning:
        # 경고만 표시 (차단하지 않음)
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": message
            }
        }
        print(json.dumps(output, ensure_ascii=False))

    sys.exit(0)


if __name__ == "__main__":
    main()
