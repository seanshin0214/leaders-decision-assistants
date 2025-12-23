# Persona MCP 설치 가이드

## 빠른 설치 (5분)

### 1단계: 의존성 설치

```bash
cd C:\Users\Sean K. S. Shin\Documents\persona-mcp
npm install
```

### 2단계: Claude Desktop 설정 파일 수정

**파일 위치**: `%APPDATA%\Claude\claude_desktop_config.json`

탐색기 주소창에 다음 입력:
```
%APPDATA%\Claude
```

**기존 파일 내용:**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\Sean K. S. Shin\\Documents"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

**추가할 내용** (기존 내용 유지하고 persona만 추가):
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\Sean K. S. Shin\\Documents"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "persona": {
      "command": "node",
      "args": ["C:\\Users\\Sean K. S. Shin\\Documents\\persona-mcp\\index.js"]
    }
  }
}
```

**주의**: 마지막에서 두 번째 항목 끝에 쉼표(`,`) 추가 필수!

### 3단계: Claude Desktop 재시작

1. Claude Desktop 완전 종료 (시스템 트레이도 확인)
2. Claude Desktop 다시 실행

### 4단계: 설치 확인

Claude Desktop에서 입력:
```
사용 가능한 도구 중에 persona 관련된 거 있어?
```

또는:
```
페르소나 목록 보여줘
```

---

## 첫 페르소나 만들기

Claude Desktop에서:

```
페르소나 하나 만들어줘.
이름: default
내용:
당신은 간결하고 직접적으로 소통합니다.
불필요한 이모지나 과한 표현 없이, 실용적인 정보만 전달합니다.
일을 위한 일은 하지 않습니다.
```

생성 확인:
```
C:\Users\Sean K. S. Shin\.persona\default.txt
```

---

## 테스트

### 기본 모드 (페르소나 없음):
```
당신: "안녕"
Claude: [일반 응답]
```

### 페르소나 활성화:
```
당신: "@persona:default 안녕"
Claude: [default 페르소나 톤으로 응답]
```

---

## 설치 문제 해결

### 1. MCP 서버가 목록에 안 보여요

**확인사항:**
- JSON 파일 문법 오류 확인 (쉼표, 중괄호)
- 파일 경로에 백슬래시 2개 (`\\`) 사용했는지 확인
- Claude Desktop 완전 재시작했는지 확인

**JSON 검증:**
https://jsonlint.com/ 에서 설정 파일 내용 복사해서 검증

### 2. npm install 오류

Node.js가 설치되어 있는지 확인:
```bash
node --version
```

없으면 설치:
https://nodejs.org/

### 3. 권한 오류

관리자 권한으로 CMD 실행 후:
```bash
cd C:\Users\Sean K. S. Shin\Documents\persona-mcp
npm install
```

### 4. MCP SDK 버전 오류

```bash
npm install @modelcontextprotocol/sdk@latest
```

---

## 제거 방법

### MCP 서버만 제거:
`claude_desktop_config.json`에서 `persona` 항목 삭제

### 완전 제거:
1. MCP 서버 제거 (위)
2. 프로젝트 폴더 삭제: `C:\Users\Sean K. S. Shin\Documents\persona-mcp`
3. 페르소나 파일 삭제: `C:\Users\Sean K. S. Shin\.persona`

---

## 다음 단계

설치 완료 후:
1. README.md에서 추천 페르소나 예제 참고
2. 자주 쓰는 톤으로 페르소나 생성
3. `@persona:이름` 형식으로 사용

---

문제가 계속되면:
1. Claude Desktop 로그 확인
2. 설정 파일 백업 후 재작성
3. 프로젝트 재설치
