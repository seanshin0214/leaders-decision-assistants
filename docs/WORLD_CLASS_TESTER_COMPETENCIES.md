# 🌟 World-Class Tester Competencies

**소프트웨어 테스터 역량 표준 및 성장 로드맵**

> World-Class 테스터가 갖춰야 할 기술적 역량, 태도, 도구 숙련도를 정의합니다.

---

## 📋 목차

1. [핵심 역량 개요](#핵심-역량-개요)
2. [테스팅 방법론 전문성](#테스팅-방법론-전문성)
3. [자동화 역량](#자동화-역량)
4. [도메인 지식](#도메인-지식)
5. [소프트 스킬](#소프트-스킬)
6. [품질 메트릭 & KPI](#품질-메트릭--kpi)
7. [성장 로드맵](#성장-로드맵)

---

## 핵심 역량 개요

### World-Class Tester의 4가지 기둥

```
┌─────────────────────────────────────┐
│   World-Class Tester Competencies   │
├─────────────────────────────────────┤
│                                     │
│  1. 테스팅 방법론   Testing Methods │
│  2. 자동화 역량     Automation      │
│  3. 도메인 지식     Domain Knowl.   │
│  4. 소프트 스킬     Soft Skills     │
│                                     │
└─────────────────────────────────────┘
```

### 역량 레벨 정의

| 레벨 | 설명 | 기대 경력 |
|------|------|----------|
| **L1 - Junior** | 기본 수동 테스트, 가이드 필요 | 0-2년 |
| **L2 - Mid** | 독립적 테스트, 기본 자동화 | 2-4년 |
| **L3 - Senior** | 복잡한 시나리오, 고급 자동화 | 4-7년 |
| **L4 - Staff** | 아키텍처 설계, 멘토링 | 7-10년 |
| **L5 - Principal** | 조직 전략, 업계 리더 | 10년+ |

---

## 테스팅 방법론 전문성

### 1. Unit Testing (단위 테스트)

#### 핵심 개념

```typescript
// Good Unit Test 특징: FIRST 원칙
// Fast, Independent, Repeatable, Self-validating, Timely

describe('Calculator', () => {
  it('should add two numbers correctly', () => {
    const result = add(2, 3);
    expect(result).toBe(5); // ✅ Fast, clear
  });

  it('should handle edge case: large numbers', () => {
    const result = add(Number.MAX_SAFE_INTEGER, 1);
    expect(result).toBe(Number.MAX_SAFE_INTEGER + 1); // 🔥 Edge case
  });
});
```

#### 역량 기준

| 레벨 | 역량 |
|------|------|
| L1 | 기존 테스트 실행, 간단한 assertion 작성 |
| L2 | 독립적 unit test 작성, mocking 이해 |
| L3 | TDD 실천, 복잡한 mock/spy 활용 |
| L4 | 테스트 아키텍처 설계, 팀 가이드라인 수립 |

### 2. Integration Testing (통합 테스트)

#### 핵심 개념

```typescript
// API Integration Test 예시
describe('POST /api/projects', () => {
  it('should create project with valid data', async () => {
    const response = await request(app)
      .post('/api/projects')
      .send({
        name: 'Test Project',
        startDate: '2024-01-01',
      })
      .expect(201);

    expect(response.body).toHaveProperty('id');
    expect(response.body.name).toBe('Test Project');

    // Verify in database
    const project = await db.projects.findById(response.body.id);
    expect(project).toBeTruthy();
  });
});
```

#### 역량 기준

| 레벨 | 역량 |
|------|------|
| L2 | API 테스트 작성, DB 상호작용 검증 |
| L3 | 복잡한 통합 시나리오, 트랜잭션 처리 |
| L4 | 마이크로서비스 통합 테스트 아키텍처 |

### 3. E2E Testing (엔드투엔드 테스트)

#### 핵심 개념

```typescript
// E2E Test: User Journey
test('complete user onboarding flow', async ({ page }) => {
  // 1. Registration
  await page.goto('/register');
  await page.fill('[name="email"]', 'new@user.com');
  await page.fill('[name="password"]', 'secure123');
  await page.click('button[type="submit"]');

  // 2. Email verification (mock)
  const verifyLink = await getVerificationLink('new@user.com');
  await page.goto(verifyLink);

  // 3. Profile setup
  await expect(page).toHaveURL('/profile/setup');
  await page.fill('[name="fullName"]', 'John Doe');
  await page.click('button:has-text("Complete Setup")');

  // 4. Dashboard access
  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('h1')).toContainText('Welcome, John');
});
```

#### 역량 기준

| 레벨 | 역량 |
|------|------|
| L2 | 간단한 E2E 시나리오 작성 |
| L3 | 복잡한 User Journey, Page Object Model 활용 |
| L4 | E2E 테스트 프레임워크 설계, CI/CD 통합 |

### 4. Performance Testing (성능 테스트)

#### 핵심 개념

```javascript
// k6 Load Testing 예시
import http from 'k6/http';
import { check } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 100 }, // Ramp up to 100 users
    { duration: '5m', target: 100 }, // Stay at 100 users
    { duration: '2m', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% requests < 500ms
  },
};

export default function () {
  const res = http.get('https://api.example.com/projects');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
}
```

#### 역량 기준

| 레벨 | 역량 |
|------|------|
| L2 | Lighthouse 점수 측정, 기본 부하 테스트 |
| L3 | k6/JMeter 시나리오 작성, 병목 분석 |
| L4 | 성능 최적화 전략 수립, 캐싱/CDN 설계 |

### 5. Security Testing (보안 테스트)

#### 핵심 개념

```bash
# OWASP ZAP Automated Scan
zap-cli quick-scan --self-contained \
  --start-options '-config api.disablekey=true' \
  https://app.example.com

# SQL Injection Test (Manual)
' OR '1'='1'; --
admin'--
'; DROP TABLE users; --

# XSS Test
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
```

#### OWASP Top 10 체크리스트

```markdown
✅ 보안 테스트 필수 항목:
- [ ] SQL Injection 방어
- [ ] XSS (Cross-Site Scripting) 차단
- [ ] CSRF (Cross-Site Request Forgery) 토큰
- [ ] Authentication/Authorization 검증
- [ ] Sensitive Data 암호화
- [ ] Security Misconfiguration 점검
- [ ] Insecure Deserialization 방지
- [ ] Known Vulnerabilities 스캔
- [ ] Insufficient Logging 개선
```

#### 역량 기준

| 레벨 | 역량 |
|------|------|
| L2 | OWASP Top 10 이해, 기본 취약점 스캔 |
| L3 | 침투 테스트, 보안 코드 리뷰 |
| L4 | 보안 아키텍처 설계, Threat modeling |

---

## 자동화 역량

### 1. 테스트 자동화 아키텍처

#### Layered Test Automation Architecture

```
┌─────────────────────────────────────┐
│    Business Layer (Test Cases)      │  ← Domain-specific test logic
├─────────────────────────────────────┤
│    Framework Layer (POM, Utils)     │  ← Reusable components
├─────────────────────────────────────┤
│    Driver Layer (Playwright/Axios)  │  ← Tool abstraction
├─────────────────────────────────────┤
│    System Under Test (SUT)          │  ← Application
└─────────────────────────────────────┘
```

#### Page Object Model (POM) 예시

```typescript
// Good POM Structure
export class ProjectsPage {
  private page: Page;

  // Locators (centralized)
  private get createButton() {
    return this.page.locator('[data-testid="create-project-btn"]');
  }

  // Actions (high-level methods)
  async createProject(data: ProjectData) {
    await this.createButton.click();
    await this.fillForm(data);
    await this.submit();
  }

  // Assertions (expected behaviors)
  async expectProjectCreated(name: string) {
    await expect(this.page.locator(`text=${name}`)).toBeVisible();
  }
}
```

### 2. CI/CD 통합

#### GitHub Actions 예시

```yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run unit tests
        run: npm run test:unit
      
      - name: Run E2E tests
        run: npm run test:e2e
      
      - name: Upload test results
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
```

### 3. Test Data Management

```typescript
// Fixture Management
export const testUsers = {
  researcher: {
    email: 'researcher@test.com',
    password: 'test123',
    role: 'RESEARCHER',
  },
  admin: {
    email: 'admin@test.com',
    password: 'admin123',
    role: 'ADMIN',
  },
};

// Database Seeding
export async function seedTestData() {
  await db.users.createMany(testUsers);
  await db.projects.createMany(testProjects);
}

// Cleanup
export async function cleanupTestData() {
  await db.projects.deleteMany();
  await db.users.deleteMany();
}
```

---

## 도메인 지식

### 1. 웹 기술 스택 이해

#### Frontend

```markdown
✅ 필수 지식:
- HTML/CSS/JavaScript 기본
- React/Vue/Angular 프레임워크
- State management (Redux, Zustand)
- Routing (React Router)
- HTTP/REST API
- WebSockets
- Browser DevTools
```

#### Backend

```markdown
✅ 필수 지식:
- Node.js/Express or Python/Django
- RESTful API 설계
- Database (SQL/NoSQL)
- Authentication (JWT, OAuth)
- Middleware & Error handling
```

### 2. 도메인 특화 지식 예시

**Healthcare (의료)**
- HIPAA 규정, PHI 보호
- HL7/FHIR 표준
- 임상 워크플로우

**Finance (금융)**
- PCI DSS 준수
- 거래 무결성
- 감사 로그

**E-commerce (전자상거래)**
- 결제 프로세스 (PG 연동)
- 장바구니 동작
- 재고 관리

---

## 소프트 스킬

### 1. 문제 발견 태도

> "오늘 무엇을 부술 수 있을까?" - NRC (미국 원자력규제위원회)

#### 테스터의 마인드셋

```markdown
✅ World-Class Tester 태도:
- 호기심: "만약 ~하면 어떻게 될까?"
- 비판적 사고: "정말 이것이 올바른가?"
- 창의성: "어떻게 이 기능을 망가뜨릴 수 있을까?"
- 끈기: "이 버그의 근본 원인을 찾을 때까지"
- 공감: "사용자 입장에서 생각하기"
```

### 2. 커뮤니케이션

#### 효과적인 버그 리포트

```
❌ Bad:
"로그인 안 됨"

✅ Good:
"Chrome 120에서 researcher 계정으로 로그인 시 
비밀번호 필드에 특수문자 포함 시 500 에러 발생.
재현율 100%. [스크린샷] [Console 로그]"
```

#### 개발자와의 협업

```markdown
✅ 협업 Best Practices:
- 공격적 X → 건설적 피드백 O
- "당신 코드 버그 있어요" X
- "이 시나리오에서 이런 동작이 발생하는데, 
   의도한 것인가요?" O
- 재현 단계 명확히 제공
- 우선순위 합리적 제안
```

### 3. 지속적 학습

```markdown
✅ 학습 루틴:
- 주 1회: 새 테스트 도구/기법 연구
- 월 1회: 테스트 컨퍼런스/웨비나 참여
- 분기 1회: 오픈소스 테스트 프로젝트 기여
- 연 1회: 테스트 자격증 취득 (ISTQB 등)
```

---

## 품질 메트릭 & KPI

### 1. 테스트 메트릭

| 지표 | 설명 | 목표 |
|------|------|------|
| **Test Coverage** | 코드 라인 커버리지 | >80% |
| **Defect Detection Rate** | 발견한 결함 비율 | >90% |
| **Test Execution Time** | 평균 실행 시간 | <30분 (E2E) |
| **Flaky Test Rate** | 불안정한 테스트 비율 | <5% |
| **Automation Rate** | 자동화된 테스트 비율 | >70% |

### 2. 품질 지표

```typescript
// 품질 대시보드 예시
interface QualityMetrics {
  testCoverage: number;        // 85%
  passRate: number;            // 98%
  avgExecutionTime: number;    // 25 minutes
  defectsFound: number;        // 23
  defectsFixed: number;        // 20
  p0Blockers: number;          // 0
  technicalDebt: number;       // 5 items
}
```

### 3. 릴리스 품질 기준

```markdown
✅ Release Criteria:
- [ ] All P0/P1 tests pass (100%)
- [ ] No critical/high severity bugs open
- [ ] Code coverage >80%
- [ ] Performance benchmarks met
- [ ] Security scan clean
- [ ] Accessibility (WCAG 2.1 AA)
- [ ] Cross-browser tested
```

---

## 성장 로드맵

### Junior (0-2년) → Mid (2-4년)

```markdown
✅ Focus Areas:
- [ ] 수동 테스트 마스터 (모든 타입)
- [ ] 기본 자동화 스크립트 작성
- [ ] Playwright/Cypress 숙련
- [ ] API 테스트 (Postman/REST Assured)
- [ ] Git/CI 기본 사용
- [ ] 버그 리포트 작성법

📚 학습 자료:
- Playwright University
- ISTQB Foundation 자격증
- Test Automation University
```

### Mid (2-4년) → Senior (4-7년)

```markdown
✅ Focus Areas:
- [ ] 테스트 아키텍처 설계
- [ ] Performance testing (k6/JMeter)
- [ ] Security testing (OWASP)
- [ ] CI/CD 파이프라인 구축
- [ ] Test strategy 수립
- [ ] 주니어 멘토링

📚 학습 자료:
- AWS Certified DevOps
- OWASP Certification
- Conference 발표
```

### Senior (4-7년) → Staff (7-10년)

```markdown
✅ Focus Areas:
- [ ] 조직 테스트 전략 수립
- [ ] 테스트 도구 선정 및 도입
- [ ] 크로스팀 협업 리드
- [ ] 테스트 표준화
- [ ] 업계 컨퍼런스 발표

📚 활동:
- 오픈소스 프로젝트 메인테이너
- 기술 블로그 운영
- 테스트 커뮤니티 리더
```

---

## 도구 체크리스트

### 필수 도구 숙련도

```markdown
✅ Level 2 (Mid):
- [ ] Playwright/Cypress (E2E)
- [ ] Vitest/Jest (Unit)
- [ ] Postman/Insomnia (API)
- [ ] Chrome DevTools
- [ ] Git/GitHub
- [ ] JIRA/Linear

✅ Level 3 (Senior):
- [ ] k6/JMeter (Performance)
- [ ] OWASP ZAP (Security)
- [ ] Docker (Test환경)
- [ ] GitHub Actions (CI/CD)
- [ ] Lighthouse (Performance)
- [ ] Accessibility tools (axe)

✅ Level 4 (Staff):
- [ ] Terraform (Infrastructure)
- [ ] Grafana/Prometheus (Monitoring)
- [ ] Custom test frameworks
- [ ] Test data generators
```

---

## 참고 자료

- **ISTQB**: International Software Testing Qualifications Board
- **NRC**: Good Software Tester Characteristics
- **OWASP**: Web Security Testing Guide
- **Test Automation University**: Free courses
- **Playwright Documentation**: Modern E2E testing

---

**📌 다음 문서**: [Tester Usage Guide](TESTER_USAGE_GUIDE.md)
