#!/usr/bin/env python3
"""
UserPromptSubmit Hook: 프롬프트 로깅 및 컨텍스트 추가
사용자 프롬프트를 로깅하고 추가 컨텍스트를 주입합니다.
"""

import json
import os
import sys
from datetime import datetime


def get_git_info() -> dict:
    """현재 Git 정보를 가져옵니다."""
    import subprocess

    git_info = {}

    try:
        # 현재 브랜치
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            git_info["branch"] = result.stdout.strip()

        # 마지막 커밋 해시
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            git_info["commit"] = result.stdout.strip()

        # 변경된 파일 수
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            changes = [line for line in result.stdout.strip().split("\n") if line]
            git_info["changes"] = len(changes)

    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return git_info


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}", file=sys.stderr)
        sys.exit(1)

    prompt = input_data.get("prompt", "")
    session_id = input_data.get("session_id", "unknown")
    cwd = input_data.get("cwd", os.getcwd())

    # 현재 시간
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Git 정보 가져오기
    git_info = get_git_info()

    # 컨텍스트 정보 구성
    context_parts = [f"현재 시간: {current_time}"]

    if git_info:
        if "branch" in git_info:
            context_parts.append(f"Git 브랜치: {git_info['branch']}")
        if "commit" in git_info:
            context_parts.append(f"최근 커밋: {git_info['commit']}")
        if "changes" in git_info and git_info["changes"] > 0:
            context_parts.append(f"변경된 파일: {git_info['changes']}개")

    context = "\n".join(context_parts)

    # stdout으로 컨텍스트 출력 (Claude의 컨텍스트에 추가됨)
    print(context)

    # 또는 JSON 형식으로 출력할 수도 있음:
    # output = {
    #     "hookSpecificOutput": {
    #         "hookEventName": "UserPromptSubmit",
    #         "additionalContext": context
    #     }
    # }
    # print(json.dumps(output, ensure_ascii=False))

    sys.exit(0)


if __name__ == "__main__":
    main()
