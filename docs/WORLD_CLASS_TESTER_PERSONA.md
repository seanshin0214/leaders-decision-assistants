# 🎯 World-Class Tester Persona

**범용 소프트웨어 테스팅 핵심 실전 가이드**

> 모든 웹 애플리케이션 프로젝트에 적용 가능한 World-Class 테스팅 방법론입니다.

---

## 📋 목차

1. [서론: 테스트의 중요성](#서론)
2. [핵심 테스팅 워크플로우](#핵심-테스팅-워크플로우)
3. [Manual Testing 실전](#manual-testing-실전)
4. [E2E 자동화 테스팅](#e2e-자동화-테스팅)
5. [버그 리포트 작성법](#버그-리포트-작성법)
6. [Pre-release 검증](#pre-release-검증)

---

## 서론

### 테스트가 중요한 이유

**IEEE Software** 연구에 따르면 테스트는 **프로젝트의 40-50%**를 차지하는 핵심 활동입니다.

#### 테스트가 해결하는 문제

- ✅ **기능 결함 발견**: 요구사항 미달성 식별
- ✅ **사용자 경험 검증**: 실사용 환경 편의성 확인
- ✅ **회귀 결함 방지**: 기존 기능 보호
- ✅ **성능/보안 검증**: 속도, 안정성, 취약점 점검

#### 테스트 피라미드

```
        /\
       /E2E\         ← 가장 적게 (느리고 비쌈)
      /------\
     /  API  \       ← 중간 정도
    /----------\
   /    Unit    \    ← 가장 많이 (빠르고 저렴)
  /--------------\
```

| 레벨 | 비율 | 실행 빈도 | 도구 |
|------|------|----------|------|
| E2E | 10% | Daily | Playwright, Cypress |
| Integration | 20% | 매 커밋 | Vitest, Supertest |
| Unit | 70% | 매 커밋 | Vitest, Jest |

---

## 핵심 테스팅 워크플로우

### 1. 요구사항 분석

#### 핵심 질문 체크리스트

```markdown
📝 테스트 설계 전 필수 질문:
- [ ] 이 기능의 목적은 무엇인가?
- [ ] 성공 기준은?
- [ ] 예외 상황은 어떻게 처리하는가?
- [ ] 성능 요구사항이 있는가?
- [ ] 접근성 고려사항은?
- [ ] 보안 위험은 없는가?
```

#### 테스트 범위 정의 예시

**기능: AI Chat**

```
✅ In Scope:
- 메시지 송수신
- AI 응답 렌더링
- 대화 히스토리 유지
- 에러 처리 (API 실패, 타임아웃)
- 마크다운 렌더링

❌ Out of Scope (Phase 2):
- 멀티모달 (이미지)
- 음성 입력
- 검색 기능
```

### 2. 테스트 케이스 설계

#### Happy Path, Error Path, Edge Cases

```typescript
// 예시: Login Feature

// ✅ Happy Path
TC001: 유효한 자격증명으로 로그인 성공
TC002: "Remember me" 체크 시 세션 유지

// ⚠️ Error Paths  
TC003: 잘못된 이메일 → 에러 메시지
TC004: 잘못된 비밀번호 → 에러 메시지
TC005: 네트워크 오류 → 재시도 안내

// 🔥 Edge Cases
TC006: SQL injection 시도 → 차단
TC007: 256자 특수문자 비밀번호
TC008: 동시 다중 로그인
```

---

## Manual Testing 실전

### 환경 설정

#### Chrome DevTools 필수 단축키

```bash
F12              # DevTools 열기
Ctrl+Shift+M    # 모바일 뷰
Ctrl+Shift+C    # 요소 선택
Ctrl+Shift+I    # Console

# Network 탭 체크 항목
✓ Status codes (200, 400, 500)
✓ Response times (≤3초)
✓ Failed requests (빨간색)
✓ Payload 크기
```

### Manual Testing 4단계

#### Step 1: 준비

```markdown
✅ 시작 전 체크리스트:
- [ ] 최신 브라우저 (Chrome/Firefox/Safari)
- [ ] DevTools Network 탭 ON
- [ ] Console 에러 모니터링
- [ ] 화면 녹화 준비 (Loom/OBS)
- [ ] 테스트 계정 준비
```

#### Step 2: Happy Path

**예시: 프로젝트 생성**

```
1. 로그인 (researcher 권한)
2. Dashboard → "Create Project"
3. 이름: "Test Project Alpha"
4. Description 입력
5. Start/End Date 선택
6. "Create" 클릭
7. 로딩 확인 (≤2초)
8. 성공 메시지 확인
9. 프로젝트 리스트에서 확인
10. 상세 페이지 리다이렉션 확인

✅ 예상: 모든 입력 저장, 에러 없음
```

#### Step 3: Error Path

```
Scenario: 필수 필드 누락

1. "Create Project" 클릭
2. 이름 입력 없이 "Create"
3. 에러 메시지: "Project name is required"
4. 입력 필드 빨간 테두리
5. 포커스 이동 확인
```

```
Scenario: 네트워크 오류

1. DevTools → Offline 모드
2. "Create" 클릭
3. 에러: "Network error. Please check connection."
4. Retry 버튼 제공 확인
5. 사용자 입력 유지 확인
```

#### Step 4: Edge Cases

```
Case 1: 긴 입력
- 이름 500자 → UI 안 깨짐 확인
- 서버 400 응답 + 명확한 메시지

Case 2: 특수문자
- <script>alert('XSS')</script> 입력
- XSS 차단 확인 (이스케이프 처리)

Case 3: 중복 요청
- "Create" 버튼 더블 클릭
- 중복 생성 방지
- 버튼 비활성화 처리
```

### 버그 발견 시 프로세스

#### 1. 화면 녹화/스크린샷

```
📹 Loom 녹화:
- 버그 재현 전체 과정
- Console 로그 포함
- Network 탭 열어서 API 상태
- 에러 메시지 클로즈업

📸 스크린샷:
- 에러 화면 전체
- Console 로그
- Network 실패 요청
- 사용자 입력 (민감정보 제외)
```

#### 2. Console/Network 로그

```javascript
// Console 에러 전체 복사
Uncaught TypeError: Cannot read 'name' of undefined
    at ProjectForm.handleSubmit (ProjectForm.tsx:45)
    
// Network 로그
POST /api/projects - 500 Internal Server Error
Response: {"error": "Database connection failed"}
```

---

## E2E 자동화 테스팅

### Playwright 기본 구조

```typescript
// playwright.config.ts
export default defineConfig({
  testDir: './tests/e2e',
  timeout: 30000,
  use: {
    baseURL: 'http://localhost:3000',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium' },
    { name: 'firefox' },
    { name: 'webkit' },
  ],
});
```

### Page Object Model (POM)

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.fill('[data-testid="email"]', email);
    await this.page.fill('[data-testid="password"]', password);
    await this.page.click('[data-testid="login-btn"]');
  }

  async expectSuccess() {
    await expect(this.page).toHaveURL('/dashboard');
  }
}
```

### 실전 E2E 예시

**AI Chat 테스트**

```typescript
// tests/e2e/ai-chat.spec.ts
test('should send message and receive AI response', async ({ page }) => {
  await loginAsResearcher(page);
  
  // Navigate
  await page.click('[data-testid="ai-chat-menu"]');
  
  // Send message
  await page.fill('[data-testid="chat-input"]', 'What is AI?');
  await page.click('[data-testid="send-btn"]');
  
  // Verify user message
  const userMsg = page.locator('[data-testid="msg-user"]').last();
  await expect(userMsg).toContainText('What is AI?');
  
  // Wait for AI response
  const aiMsg = page.locator('[data-testid="msg-ai"]').last();
  await expect(aiMsg).toBeVisible({ timeout: 10000 });
  await expect(aiMsg).toContainText('artificial intelligence');
});
```

**에러 처리 테스트**

```typescript
test('should handle API error gracefully', async ({ page }) => {
  // Mock API error
  await page.route('**/api/ai/chat', route => {
    route.fulfill({
      status: 500,
      body: JSON.stringify({ error: 'Service unavailable' }),
    });
  });

  await page.click('[data-testid="ai-chat-menu"]');
  await page.fill('[data-testid="chat-input"]', 'Test');
  await page.click('[data-testid="send-btn"]');

  // Verify error handling
  const error = page.locator('[data-testid="error-alert"]');
  await expect(error).toBeVisible();
  await expect(error).toContainText('unavailable');
  await expect(page.locator('[data-testid="retry-btn"]')).toBeVisible();
});
```

---

## 버그 리포트 작성법

### JIRA/GitHub Issue 템플릿

```markdown
## 🐛 버그 요약
AI Chat에서 메시지 중복 전송됨

## 📋 환경
- OS: Windows 11
- Browser: Chrome 120
- Version: v2.1.0
- User: Researcher

## 🔍 재현 단계
1. AI Chat 열기
2. "Test" 입력
3. Send 버튼 연속 2번 클릭

## ❌ 실제 결과
- 메시지 2번 전송
- Console: TypeError
- 채팅창에 중복 표시

## ✅ 기대 결과
- 1번만 전송
- 버튼 전송 중 비활성화
- 에러 없음

## 📹 증빙
- Loom: https://loom.com/share/abc
- Screenshot: [첨부]
- Console Log: [첨부]

## 💥 심각도
[x] P1 - High

## 🔄 재현율
[x] Always (100%)
```

---

## Pre-release 검증

### 필수 체크리스트

#### 1. CI/CD

```markdown
✅ 자동화:
- [ ] Unit tests 100% pass
- [ ] Integration tests pass
- [ ] E2E tests pass
- [ ] No flaky tests
- [ ] Code coverage ≥80%
```

#### 2. Critical Path (10개)

```markdown
✅ 수동 테스트:
- [ ] Login/Logout
- [ ] User registration
- [ ] Create project
- [ ] Edit project
- [ ] AI Chat
- [ ] File upload/download
- [ ] Report generation
- [ ] Team invite
- [ ] Dashboard
- [ ] User settings
```

#### 3. Cross-Browser

```markdown
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] iOS Safari
- [ ] Android Chrome
```

#### 4. Performance

```markdown
✅ Lighthouse (>90):
- [ ] Performance >90
- [ ] Accessibility >95
- [ ] Best Practices >90
- [ ] SEO >90
```

#### 5. Security

```markdown
- [ ] OWASP ZAP clean
- [ ] npm audit (0 critical)
- [ ] No hardcoded secrets
- [ ] HTTPS enforced
- [ ] XSS protection
```

### Release Sign-off

```markdown
## ✅ Release Approval

Tested by: [Name]
Date: 2024-01-15
Version: v2.1.0

Approved by:
- [ ] QA Lead
- [ ] Engineering Lead
- [ ] Product Manager

Decision: ✅ GO / ❌ NO-GO
```

---

## 참고 자료

- **IEEE Software**: Software Testing Methodologies
- **Atlassian**: Manual vs Automated Testing
- **Playwright Docs**: E2E Testing Best Practices
- **OWASP**: Web Security Testing Guide

---

**📌 다음 문서**: [World-Class Tester Competencies](WORLD_CLASS_TESTER_COMPETENCIES.md)
