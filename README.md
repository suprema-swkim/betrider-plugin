# Betrider Plugin for Claude Code

Claude Code를 위한 종합 플러그인입니다. 코드베이스 문서화, 전문 에이전트, 코드 리뷰, 자동화 hooks, MCP 통합을 제공합니다.

## 주요 기능

| 기능 | 개수 | 설명 |
|------|------|------|
| **Agents** | 8 | 분석, 설계, 코딩, 테스트, PR 생성 등 전문 에이전트 |
| **Skills** | 1 | 코드 리뷰 스킬 |
| **Commands** | 1 | /deepinit 코드베이스 문서화 |
| **Hooks** | 5 | 코드 품질 및 자동화 |
| **MCP** | 1 | Context7 통합 |

## 설치 방법

### 1. 마켓플레이스 추가
```
/plugin marketplace add suprema-swkim/betrider-plugin
```

### 2. 플러그인 설치
```
/plugin install betrider-plugin@betrider-plugins
```

---

## Agents

전문화된 에이전트들이 페이지 개발 파이프라인을 자동화합니다.

| Agent | 역할 | 색상 |
|-------|------|------|
| **analyst** | 자연어 요청을 구조화된 요구사항으로 변환 | 🔵 blue |
| **planner** | 페이지 단위 작업 계획 수립, 워크트리/브랜치 계획 | 🟣 purple |
| **designer** | UI 구조 설계, 컴포넌트 트리 정의 | 🩷 pink |
| **api-mapper** | API 스펙 분석, 엔드포인트 매핑, 타입 정의 | 🟠 orange |
| **coder** | 실제 코드 작성, TypeScript/ESLint 검증 | 🟢 green |
| **tester** | 브라우저 테스트, 스크린샷 캡처 | 🟡 yellow |
| **pr-creator** | 커밋 생성, GitHub PR 생성, 워크트리 정리 | 🔴 red |
| **page-pipeline** | 전체 파이프라인 오케스트레이터 | 🩵 cyan |

### 파이프라인 흐름

```
Analyst → Planner → Designer → API Mapper → Coder → Tester → PR Creator
                         ↑
                   Page Pipeline (오케스트레이터)
```

### 사용 예시

```
@analyst 사용자 관리 페이지를 만들어줘
@planner 요구사항을 페이지별로 분해해줘
@page-pipeline 전체 구현 파이프라인 실행
```

---

## Skills

### `/betrider-plugin:code-review`

코드 리뷰 스킬입니다. 다음 항목을 검토합니다:

1. 코드 구조 및 조직
2. 에러 처리
3. 보안 문제
4. 테스트 커버리지

---

## Commands

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

---

## Hooks

코드 품질과 자동화를 위한 다양한 hooks가 포함되어 있습니다.

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

---

## MCP 통합

### Context7

최신 문서를 가져오기 위한 Context7 MCP 서버가 통합되어 있습니다.

```json
{
  "context7": {
    "command": "cmd",
    "args": ["/c", "npx", "-y", "@upstash/context7-mcp@latest"]
  }
}
```

---

## 플러그인 구조

```
betrider-plugin/
├── .claude-plugin/
│   ├── marketplace.json       # 마켓플레이스 카탈로그
│   └── plugin.json            # 플러그인 매니페스트
├── agents/
│   ├── analyst.md             # 요구사항 분석 에이전트
│   ├── api-mapper.md          # API 매핑 에이전트
│   ├── coder.md               # 코드 작성 에이전트
│   ├── designer.md            # UI 설계 에이전트
│   ├── page-pipeline.md       # 파이프라인 오케스트레이터
│   ├── planner.md             # 작업 계획 에이전트
│   ├── pr-creator.md          # PR 생성 에이전트
│   └── tester.md              # 테스트 에이전트
├── commands/
│   └── deepinit.md            # /deepinit 명령어
├── hooks/
│   ├── hooks.json             # hooks 설정
│   └── scripts/               # hook 스크립트
│       ├── validate-bash.py          # Bash 명령어 검증
│       ├── validate-file-write.py    # 파일 쓰기 검증
│       ├── post-file-change.py       # 파일 변경 후 처리
│       ├── prompt-logger.py          # 프롬프트 로깅
│       └── session-start.py          # 세션 시작 처리
├── skills/
│   └── code-review/
│       └── SKILL.md           # 코드 리뷰 스킬
├── .mcp.json                  # MCP 서버 설정
└── README.md
```

---

## 라이선스

MIT License
