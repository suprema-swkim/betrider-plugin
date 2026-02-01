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

## 플러그인 구조

```
betrider-plugin/
├── .claude-plugin/
│   ├── marketplace.json   # 마켓플레이스 카탈로그
│   └── plugin.json        # 플러그인 매니페스트
├── commands/
│   └── deepinit.md        # /deepinit 명령어
└── README.md
```

## 라이선스

MIT License
