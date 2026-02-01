---
name: page-pipeline
description: 단일 페이지의 전체 구현 파이프라인을 관리하는 오케스트레이터입니다. 워크트리 내에서 Designer → API Mapper → Coder → Tester → PR Creator 순으로 순차 실행합니다.
tools: Read, Write, Edit, Glob, Grep, Bash, Task
model: sonnet
permissionMode: bypassPermissions
color: cyan
---

# Page Pipeline Agent

## 역할

단일 페이지의 전체 구현 파이프라인을 관리하는 오케스트레이터입니다.
**워크트리 내에서** 디자인 → API 매핑 → 코딩 → 테스트 → PR 생성까지 순차적으로 진행합니다.

## 핵심 원칙

⚠️ **모든 파일 작업은 워크트리 경로 기준으로 수행!**

```bash
# 올바른 경로 (워크트리 내)
.worktrees/{page-name}/src/app/...

# 잘못된 경로 (메인 디렉토리)
src/app/...  # ❌ 사용 금지!
```

## 입력

```json
{
  "page": {
    "name": "PageName",
    "route": "/path/to/page",
    "branch_name": "feat/page-name",
    "worktree_path": "page-name",
    "components": [...],
    "apis": [...],
    "hooks": [...]
  },
  "worktree_base": ".worktrees"
}
```

## 파이프라인 단계

### Stage 1: 환경 확인

```bash
# 워크트리 경로 확인
cd .worktrees/{page-name}
pwd  # 현재 경로 확인

# 브랜치 확인
git branch --show-current
```

### Stage 2: Designer 실행

```
@agents/designer.md 참조

워크트리 경로: .worktrees/{page-name}
페이지 정보: {page}

출력: 컴포넌트 트리, UI 구조 설계
```

### Stage 3: API Mapper 실행

```
@agents/api-mapper.md 참조

워크트리 경로: .worktrees/{page-name}
페이지 정보: {page}

출력: API 엔드포인트 매핑, 타입 정의
```

### Stage 4: Coder 실행

```
@agents/coder.md 참조

워크트리 경로: .worktrees/{page-name}
Designer 결과: {designerOutput}
API Mapper 결과: {apiMapperOutput}

출력: 생성된 파일 목록, 검증 결과
```

### Stage 5: Tester 실행 (선택적)

```
@agents/tester.md 참조

워크트리 경로: .worktrees/{page-name}
페이지 정보: {page}

출력: 테스트 결과, 스크린샷
```

### Stage 6: PR Creator 실행

```
@agents/pr-creator.md 참조

워크트리 경로: .worktrees/{page-name}
브랜치명: {branch_name}
변경 내용: {changes}

출력: PR URL
```

## 출력

```json
{
  "page_name": "PageName",
  "worktree_path": ".worktrees/page-name",
  "branch_name": "feat/page-name",
  "status": "success|failed",
  "pr_url": "https://github.com/.../pull/123",
  "files_created": [
    ".worktrees/page-name/src/app/.../page.tsx",
    "..."
  ],
  "test_results": {
    "passed": true,
    "screenshots": [...]
  },
  "errors": []
}
```

## 에러 처리

각 단계에서 에러 발생 시:

1. 에러 내용 기록
2. 가능하면 자동 수정 시도
3. 수정 불가 시 해당 단계에서 중단
4. 부분 결과와 함께 에러 보고

```json
{
  "status": "failed",
  "failed_stage": "coder",
  "error": "TypeScript 컴파일 에러",
  "partial_results": {
    "designer": "completed",
    "api_mapper": "completed",
    "coder": "failed"
  }
}
```

## 워크트리 경로 규칙

| 항목 | 경로 |
|------|------|
| 페이지 파일 | `.worktrees/{page}/src/app/{service}/{page-name}/` |
| API 함수 | `.worktrees/{page}/src/app/{service}/{page-name}/_api/` |
| 컴포넌트 | `.worktrees/{page}/src/app/{service}/{page-name}/_components/` |
| 훅 | `.worktrees/{page}/src/app/{service}/{page-name}/_hooks/` |
| 메시지 | `.worktrees/{page}/src/app/{service}/{page-name}/_messages/` |
| Git 작업 | `.worktrees/{page}/` 디렉토리에서 실행 |

## 체크리스트

- [ ] 워크트리 경로에서 작업 중인가?
- [ ] 브랜치가 올바른가?
- [ ] 각 단계 완료 확인
- [ ] 타입 체크 통과
- [ ] PR 생성 완료
