# Persona MCP 빠른 시작

## 1분 요약

**문제**: 시스템 프롬프트에 페르소나 넣으면 매 대화마다 토큰 낭비
**해결**: MCP 리소스로 관리, 필요할 때만 `@persona:이름` 으로 참조

---

## 설치 (3단계)

### 1. 의존성 설치 ✓
```bash
cd C:\Users\sshin\Documents\persona-mcp
npm install
```
→ 이미 완료됨

### 2. Claude Desktop 설정

파일: `%APPDATA%\Claude\claude_desktop_config.json`

다음 추가:
```json
"persona": {
  "command": "node",
  "args": ["C:\\Users\\sshin\\Documents\\persona-mcp\\index.js"]
}
```

### 3. Claude Desktop 재시작

---

## 사용법

### 페르소나 만들기
```
Claude Desktop에서:

페르소나 만들어줘. 이름은 "default", 내용은:
간결하고 직접적으로 소통합니다.
불필요한 이모지나 과한 표현 없이 실용적인 정보만 전달합니다.
```

### 페르소나 사용
```
기본 모드:
"안녕" → 일반 응답 (토큰 절약)

페르소나 활성화:
"@persona:default 안녕" → default 페르소나로 응답
```

---

## 토큰 절약 효과

**기존 방식:**
- 페르소나 500토큰 × 100회 대화 = 50,000토큰

**MCP 방식:**
- 기본: 0토큰
- 필요할 때만: 500토큰 (해당 대화만)
- 100회 중 10회만 사용: 5,000토큰
- **절약: 90%**

---

## 추천 페르소나

### default (현재 스타일)
```
간결하고 직접적으로 소통합니다.
불필요한 이모지나 과한 표현 없이 실용적인 정보만 전달합니다.
일을 위한 일은 하지 않습니다.
```

### coder (개발 작업)
```
기술적으로 정확하고 구체적으로 설명합니다.
코드 예제를 풍부하게 제공합니다.
베스트 프랙티스와 보안을 강조합니다.
```

### concise (초간결)
```
최소한의 말로 핵심만 전달합니다.
bullet point 형식을 선호합니다.
```

---

## 다음 단계

1. INSTALL.md - 상세 설치 가이드
2. README.md - 전체 기능 설명
3. 직접 페르소나 파일 수정: `C:\Users\sshin\.persona\이름.txt`

---

**제작일**: 2025-11-01
