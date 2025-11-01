# Persona MCP Server

Claude Desktop용 페르소나 관리 MCP 서버

## 주요 기능

- **잠수함 모드**: 기본적으로 토큰 사용 안 함
- **필요할 때만 활성화**: `@persona:이름` 형식으로 참조
- **개별 파일 관리**: 각 페르소나를 `.txt` 파일로 저장
- **간편한 관리**: 도구로 생성/수정/삭제

## 토큰 절약 원리

### 기존 방식 (시스템 프롬프트):
```
매 대화: 페르소나 500토큰 소비
100회 대화: 50,000토큰 낭비
```

### MCP 방식:
```
기본: 0토큰
필요할 때만: @persona:default → 해당 대화에만 적용
```

---

## 설치 방법

### 1. 의존성 설치
```bash
cd C:\Users\sshin\Documents\persona-mcp
npm install
```

### 2. Claude Desktop 설정

`%APPDATA%\Claude\claude_desktop_config.json` 파일에 추가:

```json
{
  "mcpServers": {
    "persona": {
      "command": "node",
      "args": ["C:\\Users\\sshin\\Documents\\persona-mcp\\index.js"]
    }
  }
}
```

### 3. Claude Desktop 재시작

---

## 사용 방법

### 페르소나 생성

Claude Desktop에서:
```
페르소나 만들어줘. 이름은 "professional", 내용은 다음과 같아:

당신은 전문적이고 격식있는 톤으로 대화합니다.
항상 존댓말을 사용하며, 비즈니스 맥락에 적합한 표현을 선택합니다.
```

→ MCP 도구 `create_persona` 실행됨
→ `~/.persona/professional.txt` 파일 생성

### 페르소나 목록 확인

```
사용 가능한 페르소나 목록 보여줘
```

### 페르소나 활성화 (핵심!)

```
@persona:professional 이 이메일 초안 검토해줘
```

→ 이 대화에만 "professional" 페르소나 적용
→ 다음 대화부터는 다시 기본 모드

### 페르소나 수정

```
"professional" 페르소나 수정해줘. 좀 더 친근하게 바꿔줘.
```

### 페르소나 삭제

```
"professional" 페르소나 삭제해줘
```

---

## 페르소나 파일 위치

- Windows: `C:\Users\사용자명\.persona\`
- Mac/Linux: `~/.persona/`

각 페르소나는 `이름.txt` 형식으로 저장됩니다.

직접 파일을 수정해도 됩니다:
```bash
notepad C:\Users\sshin\.persona\professional.txt
```

---

## 사용 예시

### 예시 1: 기본 대화 (토큰 절약)

```
당신: "안녕, 오늘 날씨 어때?"
Claude: "안녕하세요! [일반 응답]"
→ 페르소나 미사용, 토큰 절약
```

### 예시 2: 페르소나 활성화

```
당신: "@persona:professional 비즈니스 제안서 검토해주세요"
Claude: "[professional 페르소나로 격식있게 응답]"
→ 이 대화에만 페르소나 토큰 사용
```

### 예시 3: 여러 페르소나 전환

```
당신: "@persona:casual 이 코드 설명해줘"
Claude: "[편하게 설명]"

당신: "@persona:teacher 이번엔 초보자에게 설명하듯이"
Claude: "[교육적으로 설명]"
```

---

## 추천 페르소나 예제

### 1. professional (비즈니스)
```
당신은 전문적이고 격식있는 톤으로 대화합니다.
존댓말을 사용하며, 비즈니스 맥락에 적합한 표현을 선택합니다.
간결하고 명확하게 핵심을 전달합니다.
```

### 2. casual (일상)
```
친근하고 편안한 톤으로 대화합니다.
반말을 사용하되 예의는 지킵니다.
이모지를 적절히 사용할 수 있습니다.
```

### 3. teacher (교육)
```
학생을 가르치는 선생님처럼 설명합니다.
복잡한 개념을 쉽게 풀어서 설명합니다.
예시와 비유를 많이 사용합니다.
질문을 유도하여 이해도를 확인합니다.
```

### 4. coder (개발)
```
기술적으로 정확하고 구체적으로 설명합니다.
코드 예제를 풍부하게 제공합니다.
베스트 프랙티스를 강조합니다.
보안과 성능을 항상 고려합니다.
```

### 5. concise (간결)
```
최소한의 말로 핵심만 전달합니다.
불필요한 수식어를 배제합니다.
bullet point 형식을 선호합니다.
```

---

## 도구 목록

MCP 서버가 제공하는 도구:

1. **create_persona**: 새 페르소나 생성
2. **update_persona**: 기존 페르소나 수정
3. **delete_persona**: 페르소나 삭제
4. **list_personas**: 모든 페르소나 목록

Claude가 자동으로 적절한 도구를 선택해서 실행합니다.

---

## 리소스 참조 방법

페르소나는 MCP 리소스로 노출됩니다:

```
URI: persona://이름
예: persona://professional
    persona://casual
    persona://teacher
```

사용:
```
@persona:professional 내용
```

---

## 문제 해결

### MCP 서버가 안 보여요
1. Claude Desktop 완전 종료 후 재시작
2. 설정 파일 경로 확인: `%APPDATA%\Claude\claude_desktop_config.json`
3. JSON 문법 오류 확인 (쉼표, 중괄호)

### 페르소나가 적용 안 돼요
- `@persona:이름` 형식 정확히 입력했는지 확인
- 페르소나 이름 철자 확인
- `list_personas` 도구로 사용 가능한 페르소나 확인

### 파일 위치를 모르겠어요
Windows: `C:\Users\사용자명\.persona\`
폴더가 숨김 폴더일 수 있습니다 (탐색기에서 숨김 파일 표시)

---

## 라이선스

MIT

---

## 제작

2025-11-01
