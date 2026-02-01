#!/usr/bin/env python3
"""
SessionStart Hook: 세션 시작 시 환경 설정
세션 시작 시 프로젝트 정보를 로드하고 환경을 설정합니다.
"""

import json
import os
import subprocess
import sys


def get_project_info() -> dict:
    """프로젝트 정보를 수집합니다."""
    info = {}

    # package.json 확인
    if os.path.exists("package.json"):
        try:
            with open("package.json", "r", encoding="utf-8") as f:
                pkg = json.load(f)
                info["project_name"] = pkg.get("name", "unknown")
                info["project_version"] = pkg.get("version", "unknown")
                info["project_type"] = "Node.js"

                # 주요 의존성
                deps = list(pkg.get("dependencies", {}).keys())[:5]
                if deps:
                    info["main_dependencies"] = deps
        except (json.JSONDecodeError, IOError):
            pass

    # pyproject.toml 확인
    elif os.path.exists("pyproject.toml"):
        info["project_type"] = "Python"

    # Cargo.toml 확인
    elif os.path.exists("Cargo.toml"):
        info["project_type"] = "Rust"

    # go.mod 확인
    elif os.path.exists("go.mod"):
        info["project_type"] = "Go"

    return info


def get_recent_issues() -> list:
    """최근 TODO/FIXME 주석을 찾습니다."""
    issues = []

    try:
        # ripgrep으로 TODO/FIXME 찾기
        result = subprocess.run(
            ["rg", "-i", "(TODO|FIXME|HACK|XXX):", "--no-heading", "-m", "5"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            lines = result.stdout.strip().split("\n")[:5]
            issues = [line.strip() for line in lines if line.strip()]
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return issues


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}", file=sys.stderr)
        sys.exit(1)

    source = input_data.get("source", "unknown")
    session_id = input_data.get("session_id", "unknown")

    # 프로젝트 정보 수집
    project_info = get_project_info()

    # 컨텍스트 구성
    context_parts = []

    if source == "startup":
        context_parts.append("=== 새 세션 시작 ===")
    elif source == "resume":
        context_parts.append("=== 세션 재개 ===")

    if project_info:
        if "project_name" in project_info:
            context_parts.append(f"프로젝트: {project_info['project_name']} v{project_info.get('project_version', 'unknown')}")
        if "project_type" in project_info:
            context_parts.append(f"프로젝트 타입: {project_info['project_type']}")
        if "main_dependencies" in project_info:
            context_parts.append(f"주요 의존성: {', '.join(project_info['main_dependencies'])}")

    # 최근 이슈 확인
    issues = get_recent_issues()
    if issues:
        context_parts.append("\n[주의가 필요한 항목]")
        for issue in issues[:3]:
            context_parts.append(f"  - {issue}")

    if context_parts:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": "\n".join(context_parts)
            }
        }
        print(json.dumps(output, ensure_ascii=False))

    # 환경 변수 설정 (선택적)
    env_file = os.environ.get("CLAUDE_ENV_FILE")
    if env_file and os.path.exists(env_file):
        try:
            with open(env_file, "a") as f:
                # 예: 프로젝트별 환경 변수 설정
                if project_info.get("project_type") == "Node.js":
                    f.write("export NODE_ENV=development\n")
        except IOError:
            pass

    sys.exit(0)


if __name__ == "__main__":
    main()
