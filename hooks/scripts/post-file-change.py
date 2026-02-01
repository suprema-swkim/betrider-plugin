#!/usr/bin/env python3
"""
PostToolUse Hook: 파일 변경 후 처리
파일 변경 후 린터 실행, 포맷팅 등을 수행합니다.
"""

import json
import os
import subprocess
import sys


# 파일 확장자별 린터/포맷터 설정
LINTERS = {
    ".py": {
        "name": "Python",
        "commands": [
            # black 포맷터가 설치되어 있으면 실행
            {"cmd": ["python", "-m", "black", "--check", "--quiet"], "optional": True},
            # flake8이 설치되어 있으면 실행
            {"cmd": ["python", "-m", "flake8", "--max-line-length=100"], "optional": True},
        ]
    },
    ".js": {
        "name": "JavaScript",
        "commands": [
            {"cmd": ["npx", "eslint", "--quiet"], "optional": True},
        ]
    },
    ".ts": {
        "name": "TypeScript",
        "commands": [
            {"cmd": ["npx", "eslint", "--quiet"], "optional": True},
        ]
    },
    ".json": {
        "name": "JSON",
        "commands": [
            # JSON 문법 검사
            {"cmd": ["python", "-m", "json.tool"], "stdin": True, "optional": True},
        ]
    },
}


def get_file_extension(file_path: str) -> str:
    """파일 확장자를 반환합니다."""
    _, ext = os.path.splitext(file_path)
    return ext.lower()


def run_linter(file_path: str, linter_config: dict) -> list[str]:
    """린터를 실행하고 결과를 반환합니다."""
    results = []

    for cmd_config in linter_config.get("commands", []):
        cmd = cmd_config["cmd"] + [file_path] if not cmd_config.get("stdin") else cmd_config["cmd"]
        optional = cmd_config.get("optional", False)

        try:
            if cmd_config.get("stdin"):
                with open(file_path, "r", encoding="utf-8") as f:
                    result = subprocess.run(
                        cmd,
                        stdin=f,
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
            else:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=10
                )

            if result.returncode != 0 and result.stderr:
                results.append(f"린트 경고: {result.stderr.strip()}")

        except FileNotFoundError:
            if not optional:
                results.append(f"린터를 찾을 수 없습니다: {cmd[0]}")
        except subprocess.TimeoutExpired:
            results.append(f"린터 시간 초과: {cmd[0]}")
        except Exception as e:
            if not optional:
                results.append(f"린터 오류: {str(e)}")

    return results


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}", file=sys.stderr)
        sys.exit(1)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    tool_response = input_data.get("tool_response", {})
    file_path = tool_input.get("file_path", "")

    if tool_name not in ["Write", "Edit"] or not file_path:
        sys.exit(0)

    # 파일이 성공적으로 생성/수정되었는지 확인
    if not tool_response.get("success", True):
        sys.exit(0)

    # 파일 확장자 확인
    ext = get_file_extension(file_path)
    linter_config = LINTERS.get(ext)

    if not linter_config:
        # 지원하지 않는 파일 타입
        sys.exit(0)

    # 린터 실행
    results = run_linter(file_path, linter_config)

    if results:
        # Claude에게 린트 결과 피드백
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": f"[{linter_config['name']} 린트 결과]\n" + "\n".join(results)
            }
        }
        print(json.dumps(output, ensure_ascii=False))

    sys.exit(0)


if __name__ == "__main__":
    main()
