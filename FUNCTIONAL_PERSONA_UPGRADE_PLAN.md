# 🔬 기능적 페르소나 업그레이드 계획서 v3.0.0

**목표**: 단순 역할극(Role-Play) → 실제 기능성(Functional Capability) 전환

**기반**: Gemini & Claude 리서치 결과 + Anthropic MCP Best Practices

---

## 📊 현재 vs 목표

| 구분 | 현재 (v2.4.0) | 목표 (v3.0.0 → v3.1.0) | 기대 효과 |
|------|---------------|------------------------|-----------|
| 페르소나 | 정적 텍스트 | YAML + Tools/Resources | 구조화 |
| 지식 깊이 | 15KB 제한 | **100MB+ RAG 지식 베이스** | **무한한 전문성** |
| Tools | ❌ 없음 | ✅ 도메인별 함수 | 실제 작업 |
| Resources | ❌ 없음 | ✅ URI 템플릿 + **RAG 검색** | 실시간 + 상세 |
| Sampling | ❌ 없음 | ✅ 서버 추론 | ExpertPrompting |
| Caching | ❌ 없음 | ✅ 4-Breakpoint | 90% 비용 절감 |
| 토큰 사용 | 150K/대화 | **3K/대화 (RAG)** | **98% 절감** |
| 정확도 | Baseline | **+7-10% (RAG 효과)** | **진짜 전문가** |

---

## 🎯 Phase 1: 페르소나 구조 재설계

### 새로운 파일 구조

```yaml
---
# community/410-llm-engineer.txt
name: LLM Engineer
id: 410
version: 3.0.0
category: ai-ml
domain: llm_engineering

# Capability Definitions
tools:
  - analyze_transformer_architecture
  - design_prompt_template
  - estimate_inference_cost

resources:
  - uri_template: "llm://papers/{topic}"
    description: Latest LLM research papers
  - uri_template: "llm://benchmarks/{model}/{task}"
    description: Model performance benchmarks

sampling_enabled: true
context_caching: true
---

# World-Class+ LLM Engineer

[기존 Markdown 내용]

## 🛠️ Available Tools

### analyze_transformer_architecture
Analyze model architecture and suggest optimizations...
```

### 페르소나별 기능 매핑

| ID | 페르소나 | Tools (최소 3개) | Resources |
|----|----------|------------------|-----------|
| 101 | Fullstack Dev | analyze_code, suggest_architecture, debug_stack | code://examples/{lang} |
| 108 | DevOps | diagnose_pipeline, optimize_ci_cd, security_scan | devops://configs/{tool} |
| 201 | UI/UX Designer | analyze_usability, generate_wireframe, audit_a11y | design://patterns/{type} |
| 223 | UX Researcher | design_research, analyze_data, synthesize_insights | research://methods/{method} |
| 410 | LLM Engineer | analyze_transformer, design_prompt, estimate_cost | llm://papers/{topic} |

**전체 142개 페르소나 적용 필요**

---

## 🔧 Phase 2: MCP 서버 고도화

### 2.1. Sampling 구현

**목적**: ExpertPrompting, Solo Performance Prompting(SPP) 구현

**핵심 패턴**:
1. **ExpertPrompting**: 전문가 정체성 동적 생성
2. **SPP**: 다중 페르소나 협업 (발산 → 비평 → 통합)
3. **Debate**: Agreement Intensity 조정 (90% = Medical Q&A에서 15% 향상)

**파일**: `src/sampling.ts` 신규 생성

### 2.2. Dynamic Resources

**목적**: URI 템플릿을 통한 Just-in-Time 데이터 제공

**예시**:
- `llm://papers/transformers` → arXiv API 호출
- `code://examples/python` → GitHub 검색
- `strategy://frameworks/swot` → 프레임워크 DB 조회

**파일**: `src/resources.ts` 신규 생성

### 2.3. Tools 구현

**목적**: 페르소나별 실행 가능한 함수

**구현 계획**:
- 142개 페르소나 × 3-5개 Tools = 500+ Tools
- 페르소나 ID별 Tool 매핑
- JSON Schema 정의
- Handler 함수 구현

**파일**: `src/tools.ts` 신규 생성

---

## 💾 Phase 3: Context Engineering

### 3.1. 4-Breakpoint Caching

**구조**:
1. System Instructions (~5K tokens, 월 1회 변경)
2. Tool Definitions (~15K tokens, 주 1회 변경)
3. Persona Definition (~3K tokens, 일 1-5회 변경)
4. Conversation History (~10K tokens, 매 턴 변경)

**효과**: 78.5% 비용 절감, 79% 지연 시간 감소

### 3.2. Progressive Disclosure

**원칙**: Context에는 Tool 메타데이터만, 실제 정의는 요청 시 로드

**구현**: Filesystem 기반 Tool Discovery

---

## 📋 Phase 4: 실행 계획

### Week 1-2: Foundation
- [ ] 페르소나 YAML Frontmatter 구조 설계
- [ ] 10개 핵심 페르소나 변환 (101, 108, 201, 223, 326, 337, 410, 411, 501, 601)
- [ ] MCP 서버 기본 구조 확장

### Week 3-4: Core Features
- [ ] Sampling 기능 구현 (ExpertPrompting, SPP)
- [ ] Dynamic Resources 구현 (5개 URI scheme)
- [ ] Tools 구현 (30개 핵심 Tools)

### Week 5-6: Optimization
- [ ] 4-Breakpoint Caching 적용
- [ ] Progressive Disclosure 패턴 적용
- [ ] Context Rot 방지 전략 구현

### Week 7-8: Scale Up
- [ ] 142개 페르소나 전체 변환
- [ ] 500+ Tools 구현
- [ ] 통합 테스트

### Week 9-10: Production
- [ ] 성능 벤치마크
- [ ] 문서화 완성
- [ ] v3.0.0 Release

---

## 📈 예상 성과

### 정량적 지표
- **토큰 사용**: 150K → 2K (98.7% 절감)
- **API 비용**: $0.99 → $0.21 (78.5% 절감)
- **지연 시간**: 11.5s → 2.4s (79% 향상)
- **작업 품질**: +7-18% (지식 집약 작업)

### 정성적 지표
- ✅ 실제 작업 수행 능력 (Tools 실행)
- ✅ 최신 데이터 제공 (Dynamic Resources)
- ✅ 깊이 있는 추론 (Sampling)
- ✅ 비용 효율성 (Caching)

---

## 🚀 우선순위 Action Items

### 즉시 시작 (이번 주)
1. 페르소나 구조 재설계 완료
2. 10개 핵심 페르소나 변환
3. Sampling 프로토타입 구현

### 다음 단계 (다음 주)
1. Dynamic Resources 구현
2. 30개 핵심 Tools 구현
3. 통합 테스트

### 장기 목표 (2주 후)
1. 142개 페르소나 전체 변환
2. 프로덕션 배포
3. 성능 검증 및 문서화

---

**작성자**: Cascade AI  
**날짜**: 2025-11-23  
**버전**: 1.0.0  
**상태**: 📋 계획 수립 완료
