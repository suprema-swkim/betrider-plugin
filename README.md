# Betrider Plugin for Claude Code

Claude Code를 위한 커스텀 슬래시 명령어 플러그인 모음입니다.

## 설치 방법

이 플러그인을 사용하려면 `.claude` 폴더를 홈 디렉토리 또는 프로젝트 루트에 복사하세요:

### 전역 설치 (모든 프로젝트에서 사용)
```bash
cp -r .claude ~/.claude
```

### 프로젝트별 설치
프로젝트 루트에 `.claude` 폴더를 그대로 두면 해당 프로젝트에서만 명령어를 사용할 수 있습니다.

## 포함된 명령어

### `/deepinit`
계층적 CONTEXT.md 파일로 전체 코드베이스를 재귀적으로 색인합니다.

**사용법:**
```
/deepinit              # 현재 디렉토리 초기화
/deepinit ./src        # ./src 디렉토리 초기화
/deepinit --update     # 기존 CONTEXT.md만 업데이트
/deepinit --dry-run    # 실행 없이 미리보기
```

**기능:**
- 전체 디렉토리 재귀 분석
- 각 디렉토리에 CONTEXT.md 자동 생성
- 계층적 참조 구조 유지
- 기존 문서와 스마트 병합

## 커스텀 명령어 추가하기

`.claude/commands/` 디렉토리에 마크다운 파일을 추가하면 새로운 슬래시 명령어를 만들 수 있습니다.

### 명령어 파일 형식

```markdown
---
description: 명령어에 대한 간단한 설명
allowed-tools: Task, Read, Write, Glob, Grep
---

명령어 실행 시 Claude에게 전달될 프롬프트 내용

$ARGUMENTS 변수로 사용자가 입력한 인자를 받을 수 있습니다.
```

## 라이선스

MIT License
