# 🎯 MCP World-Class Tester 사용 가이드

**138번 테스터 페르소나를 활용한 체계적 테스팅**

> 이 가이드는 MCP (Model Context Protocol)를 통해 World-Class Tester 페르소나를 활용하는 실전 방법을 설명합니다.

---

## 📋 목차

1. [MCP 테스터 페르소나란?](#mcp-테스터-페르소나란)
2. [기본 사용법](#기본-사용법)
3. [실전 시나리오별 사용](#실전-시나리오별-사용)
4. [단계별 워크플로우](#단계별-워크플로우)
5. [문서 자동 참조 시스템](#문서-자동-참조-시스템)

---

## MCP 테스터 페르소나란?

### 특징

**138번 World-Class Tester**는 다음과 같은 특별한 기능을 가진 MCP 페르소나입니다:

```markdown
🎯 자동 문서 참조
- docs/WORLD_CLASS_TESTER_PERSONA.md (핵심 방법론)
- docs/WORLD_CLASS_TESTER_COMPETENCIES.md (역량 표준)
- docs/TESTER_USAGE_GUIDE.md (실전 시나리오)

🔄 체계적 5단계 워크플로우
Phase 1: Planning (15분)
Phase 2: Test Case Writing (30분)
Phase 3: Manual Testing (1-2시간)
Phase 4: Automation (2-4시간)
Phase 5: Reporting (30분)

📊 품질 메트릭 자동 추적
- Test Coverage: >80%
- Defect Detection Rate: >90%
- Flaky Test Rate: <5%
```

### 활성화 방법

모든 AI 도구 (Windsurf, Claude Desktop, Cursor, Antigravity)에서:

```
"138번 테스터 페르소나 불러와줘"
"138번 World-Class Tester로 전환해줘"
"@persona:138-world-class-tester"
```

---

## 기본 사용법

### 예시 1: 신규 기능 테스트

```markdown
User: "138번 테스터 페르소나로 AI Chat 기능 테스트해줘"

AI Response:
"World-Class Tester 페르소나로 전환했습니다. 
AI Chat 기능 테스트를 시작하겠습니다.

먼저 테스팅 문서를 확인하겠습니다...
[docs/WORLD_CLASS_TESTER_PERSONA.md 참조]
[docs/TESTER_USAGE_GUIDE.md의 AI Chat 시나리오 적용]

📋 PHASE 1: PLANNING (15분)

요구사항 분석을 위해 몇 가지 질문드리겠습니다:

1. AI Chat의 주요 목적은 무엇인가요?
   - 연구 질문 답변
   - 데이터 분석 지원
   - 기타

2. 지원하는 AI 모델은?
   - Claude 3.5 Sonnet
   - GPT-4
   - 둘 다

3. 입력 제한사항이 있나요?
   - 최대 텍스트 길이
   - 파일 업로드 지원 여부

4. 응답 시간 목표는?
   - 일반적으로 <10초 권장

5. 예상되는 에러 시나리오는?
   - API 실패, 타임아웃, 네트워크 오류

답변해주시면 테스트 계획을 수립하겠습니다."
```

### 예시 2: Pre-release 검증

```markdown
User: "138번 테스터로 v2.1.0 릴리스 전 검증해줘"

AI Response:
"World-Class Tester로 v2.1.0 Pre-release 검증을 시작합니다.

[docs/WORLD_CLASS_TESTER_PERSONA.md의 Pre-release Checklist 적용]

🚀 PRE-RELEASE VERIFICATION CHECKLIST

✅ Step 1: CI/CD Pipeline 확인
현재 상태를 알려주세요:
- [ ] Unit tests 결과?
- [ ] Integration tests 결과?
- [ ] E2E tests 결과?
- [ ] Code coverage %?

✅ Step 2: Critical Path Manual Testing (10개 핵심 흐름)
다음 기능들을 수동으로 테스트하겠습니다:
1. Login/Logout
2. User Registration
3. Create Project
4. Edit Project
5. AI Chat
6. File Upload/Download
7. Report Generation
8. Team Collaboration
9. Dashboard
10. User Settings

각 항목을 Chrome DevTools로 검증하고 결과를 보고하겠습니다.

✅ Step 3: Cross-Browser Testing
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Mobile (iOS/Android)

✅ Step 4: Performance & Security
- Lighthouse 점수
- OWASP ZAP 스캔
- 접근성 검사

모든 단계를 완료하고 GO/NO-GO 결정을 제공하겠습니다."
```

---

## 실전 시나리오별 사용

### 시나리오 1: 버그 발견 시

```markdown
User: "138번 테스터로 Login 페이지에서 버그 찾아줘"

AI:
"Login 페이지 테스트를 시작합니다.

[Manual Testing 4-Step Workflow 적용]

Step 1: Preparation
✅ Chrome DevTools 활성화 확인
✅ Network 탭 모니터링 시작
✅ Console 에러 추적

Step 2: Happy Path Testing
✅ 유효한 자격증명으로 로그인
✅ 'Remember me' 기능 확인
✅ 리다이렉션 정상 확인

Step 3: Error Path Testing
⚠️ 버그 발견!

🐛 BUG-001: 잘못된 비밀번호 입력 시 에러 메시지 누락

📋 Environment:
- OS: Windows 11
- Browser: Chrome 120
- Version: v2.1.0

🔍 Reproduction Steps:
1. Login 페이지 접속
2. 올바른 이메일 입력 (user@example.com)
3. 잘못된 비밀번호 입력 (wrong123)
4. Login 버튼 클릭

❌ Actual Result:
- 에러 메시지 표시 안 됨
- 페이지가 reload만 됨
- Console에 401 에러만 로그

✅ Expected Result:
- 명확한 에러 메시지: 'Invalid password. Please try again.'
- 비밀번호 필드에 포커스
- 입력한 이메일은 유지

💥 Severity: P1 - High (주요 사용성 문제)
🔄 Reproduction Rate: Always (100%)

📹 Evidence:
[스크린샷 필요]
[Console 로그 첨부]

🛠️ Suggested Fix:
\`\`\`typescript
// Add error handling in login handler
if (response.status === 401) {
  setError('Invalid email or password');
  passwordRef.current.focus();
}
\`\`\`

Step 4: Edge Case Testing 계속 진행하겠습니다..."
```

### 시나리오 2: E2E 테스트 작성 요청

```markdown
User: "138번 테스터로 Project Creation E2E 테스트 코드 작성해줘"

AI:
"Project Creation E2E 테스트를 작성하겠습니다.

[docs/WORLD_CLASS_TESTER_PERSONA.md의 E2E 방법론 적용]

📝 Test Plan:
1. Happy Path: 정상 프로젝트 생성
2. Error Path: 필수 필드 누락
3. Edge Case: 긴 이름, 특수문자

\`\`\`typescript
// tests/e2e/project-creation.spec.ts
import { test, expect } from '@playwright/test';
import { loginAsResearcher } from '../helpers/auth';

test.describe('Project Creation', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsResearcher(page);
    await page.goto('/projects');
  });

  test('TC001: should create project with valid data', async ({ page }) => {
    // Step 1: Navigate to create form
    await page.click('[data-testid="create-project-btn"]');
    await expect(page).toHaveURL(/\/projects\/new/);

    // Step 2: Fill form
    await page.fill('[data-testid="project-name"]', 'Test Project Alpha');
    await page.fill('[data-testid="project-description"]', 'E2E Test Project');
    
    // Step 3: Set dates
    const today = new Date().toISOString().split('T')[0];
    await page.fill('[data-testid="start-date"]', today);
    
    const futureDate = new Date();
    futureDate.setMonth(futureDate.getMonth() + 6);
    await page.fill('[data-testid="end-date"]', futureDate.toISOString().split('T')[0]);

    // Step 4: Submit
    await page.click('[data-testid="submit-btn"]');

    // Step 5: Verify success
    await expect(page.locator('[data-testid="success-toast"]')).toBeVisible();
    await expect(page).toHaveURL(/\/projects\/\\d+/);
    await expect(page.locator('h1')).toContainText('Test Project Alpha');
  });

  test('TC002: should show error for missing required field', async ({ page }) => {
    await page.click('[data-testid="create-project-btn"]');
    
    // Submit without name
    await page.click('[data-testid="submit-btn"]');
    
    // Verify error
    const errorMsg = page.locator('[data-testid="error-message"]');
    await expect(errorMsg).toBeVisible();
    await expect(errorMsg).toContainText('Project name is required');
    
    // Verify focus on name field
    await expect(page.locator('[data-testid="project-name"]')).toBeFocused();
  });

  test('TC003: should handle long project name', async ({ page }) => {
    await page.click('[data-testid="create-project-btn"]');
    
    // Try 500 character name
    const longName = 'A'.repeat(500);
    await page.fill('[data-testid="project-name"]', longName);
    await page.click('[data-testid="submit-btn"]');
    
    // Should show validation error
    const error = page.locator('[data-testid="error-message"]');
    await expect(error).toContainText('maximum 200 characters');
  });
});
\`\`\`

✅ Test Coverage:
- Happy Path: ✓
- Error Handling: ✓
- Edge Cases: ✓
- Data-testid selectors: ✓ (stable)
- Proper waits: ✓ (no fixed timeouts)

🚀 Next Steps:
1. Run tests: \`npx playwright test project-creation\`
2. Check for flakiness (run 10 times)
3. Add to CI/CD pipeline
4. Update test documentation"
```

---

## 단계별 워크플로우

### 5-Phase Testing Process

```markdown
PHASE 1: PLANNING (15 min)
━━━━━━━━━━━━━━━━━━━━━━━━
User: "138번 테스터로 [Feature] 테스트해줘"

AI:
1. 요구사항 분석 (5개 질문)
2. 테스트 범위 정의
3. 우선순위 결정

Output: Test Plan document


PHASE 2: TEST CASE WRITING (30 min)
━━━━━━━━━━━━━━━━━━━━━━━━
AI:
1. Happy Path 시나리오 (5-10개)
2. Error Path 시나리오 (3-5개)
3. Edge Cases (3-5개)

Output: Test Cases (yaml/markdown)


PHASE 3: MANUAL TESTING (1-2 hours)
━━━━━━━━━━━━━━━━━━━━━━━━
AI: "Chrome DevTools를 열고 테스트 시작..."
1. Preparation checklist
2. Execute all test cases
3. Document results
4. Capture bugs (screenshots/videos)

Output: Test Results + Bug Reports


PHASE 4: AUTOMATION (2-4 hours)
━━━━━━━━━━━━━━━━━━━━━━━━
AI: "E2E 테스트 코드 작성..."
1. Write Page Object Model
2. Implement test scripts
3. Add to CI/CD
4. Verify stability

Output: Playwright/Cypress code


PHASE 5: REPORTING (30 min)
━━━━━━━━━━━━━━━━━━━━━━━━
AI:
1. Summary (Pass/Fail counts)
2. Bug list (P0/P1/P2/P3)
3. Quality metrics
4. GO/NO-GO recommendation

Output: Test Report + Release Decision
```

---

## 문서 자동 참조 시스템

### MCP 페르소나가 자동으로 확인하는 문서

```markdown
📚 Documentation Auto-Reference Flow:

User Request
    ↓
138번 Tester Activated
    ↓
Auto-check docs/ folder
    ├─ WORLD_CLASS_TESTER_PERSONA.md
    │   └─ Manual Testing 4-step
    │   └─ E2E Automation patterns
    │   └─ Bug Report template
    │
    ├─ WORLD_CLASS_TESTER_COMPETENCIES.md
    │   └─ Testing levels (Unit/Integration/E2E)
    │   └─ Security testing (OWASP)
    │   └─ Quality metrics
    │
    └─ TESTER_USAGE_GUIDE.md
        └─ 4 real scenarios
        └─ Daily/Weekly/Sprint checklists
        └─ FAQ & troubleshooting
    ↓
Apply appropriate methodology
    ↓
Execute systematic testing
    ↓
Report with evidence
```

### 실제 동작 예시

```
User: "138번 테스터로 AI Chat 테스트해줘"

AI Internal Process:
1. Load persona (138-world-class-tester.txt)
2. Recognize: Testing request
3. Check: docs/TESTER_USAGE_GUIDE.md
4. Find: "Scenario 1: AI Chat testing"
5. Apply: Step-by-step workflow
6. Execute: Phase 1-5
7. Report: With evidence and recommendations

User sees:
"World-Class Tester 활성화. 문서 확인 중...
[Scenario 1 적용] AI Chat 테스트 시작합니다."
```

---

## 💡 실전 팁

### Tip 1: 문서 명시적 참조 요청

```
"138번 테스터로 전환하고, WORLD_CLASS_TESTER_PERSONA.md의 
Pre-release Checklist를 따라 검증해줘"
```

### Tip 2: 단계별 실행

```
"138번 테스터로 AI Chat 테스트해줘. 
Phase 1만 먼저 완료하고 다음 단계는 내가 지시할게"
```

### Tip 3: 특정 체크리스트 사용

```
"138번 테스터로 Security Testing Checklist 
(OWASP Top 10) 적용해서 검증해줘"
```

---

## 🎯 요약

### MCP World-Class Tester의 핵심 가치

```markdown
✅ 자동 문서 참조
   → 매번 가이드 찾을 필요 없음

✅ 체계적 워크플로우
   → 무작위 테스트 X, 5단계 방법론 O

✅ 표준 기반
   → IEEE, OWASP, NRC 표준 적용

✅ 실전 중심
   → 이론이 아닌 실제 코드 및 예시

✅ 품질 메트릭
   → 정량적 품질 측정
```

### 사용 시작

```bash
# AI 도구에서 (Windsurf, Claude Desktop, Cursor, Antigravity)
"138번 World-Class Tester 페르소나 불러와줘"

# 테스트 요청
"AI Chat 기능 테스트해줘"
"v2.1.0 릴리스 전 검증해줘"
"Login 버그 찾아줘"

# AI가 자동으로:
1. 문서 확인
2. 방법론 적용
3. 체계적 테스트
4. 증거 기반 보고
```

---

**🎉 이제 World-Class 수준의 테스팅을 자동화된 워크플로우로 수행할 수 있습니다!**
