# Persona MCP - Supabase Integration

**142개 월드클래스+ 페르소나 지식을 원격으로 제공**

---

## 개요

Supabase + pgvector를 사용하여:
- 사용자가 로컬에 지식 파일을 다운로드하지 않아도 됨
- 지식 업데이트 시 모든 사용자에게 즉시 반영
- 빠른 시맨틱 검색 (벡터 유사도 + 메타데이터 필터)

---

## 아키텍처

```
┌──────────────────────────────────────────────────────────┐
│                   User's Claude Code                      │
│                          ↓                                │
│                    Persona RAG MCP                        │
│  ┌────────────────────────────────────────────────────┐  │
│  │           HybridPersonaVectorStore                 │  │
│  │  ┌────────────────┬─────────────────────────────┐ │  │
│  │  │ Supabase 가능? │  Yes → SupabaseVectorStore  │ │  │
│  │  │                │  No  → ChromaDB (local)     │ │  │
│  │  └────────────────┴─────────────────────────────┘ │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
                           ↓
           ┌───────────────────────────────┐
           │      Supabase (PostgreSQL)     │
           │  ┌─────────────────────────┐  │
           │  │       personas          │  │
           │  │  - 142 personas         │  │
           │  │  - categories           │  │
           │  └─────────────────────────┘  │
           │  ┌─────────────────────────┐  │
           │  │   persona_knowledge     │  │
           │  │  - ~2000 chunks         │  │
           │  │  - vector embeddings    │  │
           │  └─────────────────────────┘  │
           └───────────────────────────────┘
```

---

## 1. Supabase 설정

### 1.1 프로젝트 생성
[Supabase](https://supabase.com)에서 새 프로젝트 생성

### 1.2 스키마 적용
SQL Editor에서 `schema.sql` 실행:
```sql
-- pgvector 활성화
create extension if not exists vector;

-- 테이블 생성
-- (schema.sql 전체 실행)
```

---

## 2. 지식 업로드

### 2.1 환경변수 설정
```bash
export SUPABASE_URL="https://xxxxx.supabase.co"
export SUPABASE_KEY="eyJhbGci..."  # service_role 키
export OPENAI_API_KEY="sk-..."
```

### 2.2 업로드 실행
```bash
# 모든 페르소나 업로드
python supabase/upload_personas.py

# 특정 페르소나만
python supabase/upload_personas.py --persona llm-engineer

# 테스트 (실제 업로드 안함)
python supabase/upload_personas.py --dry-run
```

---

## 3. 사용자 설정

### 3.1 Claude Desktop 설정

`claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "persona-rag": {
      "command": "python",
      "args": ["rag/server.py"],
      "cwd": "C:\\Users\\YourName\\Documents\\persona-mcp",
      "env": {
        "SUPABASE_URL": "https://xxxxx.supabase.co",
        "SUPABASE_KEY": "eyJhbGci...",
        "OPENAI_API_KEY": "sk-..."
      }
    }
  }
}
```

**참고**: 사용자는 `anon` 키 사용 (읽기 전용)

### 3.2 로컬 모드 (Supabase 없이)

환경변수 없으면 자동으로 로컬 ChromaDB 사용

---

## 4. API 함수

### search_persona_knowledge
```sql
select * from search_persona_knowledge(
    query_embedding := '[...]'::vector,
    match_threshold := 0.6,
    match_count := 5,
    filter_persona := null,
    filter_category := 'ai_data'
);
```

### search_by_persona
```sql
select * from search_by_persona(
    query_embedding := '[...]'::vector,
    target_persona := '410-llm-engineer',
    match_count := 5
);
```

### get_all_personas
```sql
select * from get_all_personas();
```

---

## 5. 카테고리

| ID | 한글명 | 번호대 |
|----|--------|--------|
| engineering | 엔지니어링 | 1xx |
| design_creative | 디자인/크리에이티브 | 2xx |
| business_leadership | 비즈니스/리더십 | 3xx |
| ai_data | AI/데이터 | 4xx |
| testing_qa | QA/테스팅 | 5xx |
| education | 교육 | 6xx |
| healthcare | 의료 | 7xx |

---

## 6. 파일 구조

```
supabase/
├── README.md                   # 이 문서
├── schema.sql                  # 테이블 & 함수 정의
├── upload_personas.py          # 지식 업로드 스크립트
└── vector_store_supabase.py    # Supabase 벡터 스토어

rag/
├── server.py                   # MCP 서버
├── vector_store.py             # 로컬 ChromaDB 스토어
└── data/                       # 로컬 데이터
```

---

## 7. 다른 MCP 서버와 통합

Socratic Thinking MCP와 동일한 Supabase 프로젝트 사용 가능:

```
Supabase Project
├── thinking_tools      (Socratic Thinking)
├── personas            (Persona MCP)
├── persona_knowledge   (Persona MCP)
└── categories          (공용)
```

---

## 8. 비용

### Supabase Free Tier
- 500MB DB → 충분 (약 10-20MB 예상)
- 2GB 대역폭/월 → 일반 사용량 충분

### OpenAI Embeddings
- 업로드: ~$0.01 (일회성)
- 검색: ~$0.00001/쿼리

---

**문의**: [Issues](https://github.com/seanshin0214/persona-mcp/issues)
