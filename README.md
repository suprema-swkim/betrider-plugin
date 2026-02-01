# Betrider Plugin for Claude Code

Claude Code를 위한 커스텀 슬래시 명령어 플러그인 마켓플레이스입니다.

## 설치 방법

### 1. 마켓플레이스 추가
```
/plugin marketplace add suprema-swkim/betrider-plugin
```

### 2. 플러그인 설치
```
/plugin install betrider-plugin@betrider-plugins
```

## 포함된 명령어

### `/betrider-plugin:deepinit`

계층적 CONTEXT.md 파일로 전체 코드베이스를 재귀적으로 색인합니다.

**사용법:**
```
/betrider-plugin:deepinit              # 현재 디렉토리 초기화
/betrider-plugin:deepinit ./src        # ./src 디렉토리 초기화
/betrider-plugin:deepinit --update     # 기존 CONTEXT.md만 업데이트
/betrider-plugin:deepinit --dry-run    # 실행 없이 미리보기
```

**기능:**
- 전체 디렉토리 재귀 분석
- 각 디렉토리에 CONTEXT.md 자동 생성
- 계층적 참조 구조 유지
- 기존 문서와 스마트 병합

## Hooks

이 플러그인에는 코드 품질과 자동화를 위한 다양한 hooks가 포함되어 있습니다.

### 포함된 Hooks

| Hook 이벤트 | 기능 |
|------------|------|
| `PreToolUse (Bash)` | 위험한 Bash 명령어 차단 및 권장 사항 제안 |
| `PreToolUse (Write\|Edit)` | 민감한 파일(.env, 인증서 등) 수정 방지 |
| `PostToolUse (Write\|Edit)` | 파일 변경 후 린터 자동 실행 |
| `UserPromptSubmit` | Git 정보 등 컨텍스트 자동 주입 |
| `SessionStart` | 세션 시작 시 프로젝트 정보 로드 |
| `Stop` | 작업 완료 여부 지능형 판단 (LLM 기반) |

### Hooks 사용 예시

hooks는 플러그인 설치 시 자동으로 활성화됩니다. 수동으로 테스트하려면:

```bash
# 플러그인 디렉토리에서 Claude Code 실행
claude --plugin-dir ./betrider-plugin

# hooks 상태 확인
/hooks
```

### Hooks 커스터마이징

`hooks/hooks.json` 파일을 수정하여 hooks를 커스터마이징할 수 있습니다:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "your-custom-script.py",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## 플러그인 구조

```
betrider-plugin/
├── .claude-plugin/
│   ├── marketplace.json   # 마켓플레이스 카탈로그
│   └── plugin.json        # 플러그인 매니페스트
├── commands/
│   └── deepinit.md        # /deepinit 명령어
├── hooks/
│   ├── hooks.json         # hooks 설정
│   └── scripts/           # hook 스크립트
│       ├── validate-bash.py        # Bash 명령어 검증
│       ├── validate-file-write.py  # 파일 쓰기 검증
│       ├── post-file-change.py     # 파일 변경 후 처리
│       ├── prompt-logger.py        # 프롬프트 로깅
│       └── session-start.py        # 세션 시작 처리
└── README.md
```

## 라이선스

MIT License
