# 📖 World-Class Tester Usage Guide

**실전 활용 가이드**

---

## 📋 4가지 실전 시나리오

### 1. 신규 기능 테스트 (AI Chat 예시)

#### Step 1: 요구사항 분석 (30분)
- AI Chat 목적, 지원 모델, 입력 제한 파악
- 응답 시간 목표, 에러 시나리오 확인

#### Step 2: 테스트 케이스 작성 (1시간)
```yaml
Happy Paths:
  - 기본 메시지 송수신
  - Follow-up 컨텍스트 유지
  - 채팅 히스토리 표시

Error Paths:
  - 네트워크 오류 → Retry
  - API 타임아웃 → 안내 메시지

Edge Cases:
  - 10,000자 메시지
  - 특수문자/이모지
  - 50개 연속 메시지 → Rate limiting
```

#### Step 3: Manual Testing (1시간)
```bash
1. Chrome DevTools (F12) 열기
2. Happy Path 실행 → 응답시간, 렌더링 확인
3. Error Path → 에러 메시지, Retry 버튼
4. 발견된 버그 → Loom 녹화 + 스크린샷
```

#### Step 4: E2E 자동화 (2시간)
```typescript
test('should send message and get AI response', async ({ page }) => {
  await page.fill('[data-testid="chat-input"]', 'What is AI?');
  await page.click('[data-testid="send-btn"]');
  
  const aiMsg = page.locator('[data-testid="msg-ai"]').last();
  await expect(aiMsg).toBeVisible({ timeout: 10000 });
});
```

---

### 2. Pre-release 검증 (4시간)

```markdown
### CI/CD (30분)
- [ ] All tests pass (Unit/Integration/E2E)
- [ ] Code coverage >80%

### Critical Path (2시간)
- [ ] Login/Logout
- [ ] Project CRUD
- [ ] AI Chat
- [ ] File upload
- [ ] Report generation

### Cross-Browser (1시간)
- [ ] Chrome/Firefox/Safari/Edge
- [ ] iOS Safari, Android Chrome

### Performance (30분)
- [ ] Lighthouse >90
- [ ] Load time <2sec

### Security (30분)
- [ ] OWASP ZAP scan clean
- [ ] XSS/SQL injection blocked
```

---

### 3. 회귀 테스트

```bash
# E2E Regression Suite 실행
npm run test:e2e:regression

# Smoke Test (Critical paths만)
npm run test:e2e:smoke
```

---

### 4. 성능 부하 테스트

```javascript
// k6 load test
export let options = {
  stages: [
    { duration: '2m', target: 50 },
    { duration: '5m', target: 100 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% <500ms
  },
};
```

---

## 신규 QA 4주 온보딩

### Week 1: 기초
- 프로젝트 이해, 로컬 환경 설정
- Chrome DevTools 마스터
- 첫 버그 리포트 작성

### Week 2: 수동 테스트
- 테스트 케이스 작성 (10개)
- Critical Path 테스트 실행
- 버그 5개 발견 및 리포트

### Week 3: 자동화 기초
- Playwright 튜토리얼
- Page Object Model 이해
- 첫 E2E 테스트 3개 작성

### Week 4: 독립 작업
- 전체 기능 테스트 플랜 수립
- Pre-release checklist 실행
- 팀 회고 발표

---

## Daily/Weekly/Sprint 체크포인트

### Daily
```markdown
오전 (9:00-12:00):
- Standup 참여
- 계획된 테스트 실행

오후 (1:00-6:00):
- 버그 검증 및 회귀 테스트
- 탐색적 테스트
- 버그 리포트 작성

Daily Metrics:
- 테스트 케이스: ~20개
- 버그 발견: 2-3개
- E2E 작성: 1-2개
```

### Weekly
- Monday: Sprint planning
- Tue-Thu: 테스트 실행
- Friday: 주간 리포트, retrospective

### Sprint
- Start: 테스트 계획 수립
- Mid: 조기 테스트 (dev branch)
- End: Pre-release 검증

---

## FAQ

### Q1: Flaky test 수정?
```typescript
// ❌ Bad: 고정 대기
await page.waitForTimeout(5000);

// ✅ Good: 조건부 대기
await page.waitForSelector('[data-testid="result"]');
await page.waitForLoadState('networkidle');
```

### Q2: 버그 우선순위?
- **P0**: 서비스 중단 → 즉시 (1시간)
- **P1**: 주요 기능 불가 → 당일
- **P2**: 우회 가능 → 3일
- **P3**: 마이너 → 다음 Sprint

### Q3: 테스트 커버리지 낮을 때?
1. Critical paths 먼저
2. 복잡한 로직 (에러 처리)
3. Edge cases

### Q4: 개발자와 의견 차이?
✅ 데이터 기반 대화  
✅ 요구사항 참조  
✅ 타협안 제시

---

## 도구 설정

### Playwright
```bash
npm init playwright@latest
npx playwright test --ui       # 디버깅
npx playwright test --headed   # 브라우저 보기
```

### Chrome DevTools
```javascript
// Console 유용 명령어
$('[data-testid="button"]')           // 요소 선택
performance.timing.loadEventEnd       // 로딩 시간
```

### JIRA 템플릿
```markdown
Title: [Component] Brief description
Priority: P1
Labels: bug, sprint-22

[Bug report template 사용]
```

---

## 참고 문서
- [World-Class Tester Persona](WORLD_CLASS_TESTER_PERSONA.md)
- [Tester Competencies](WORLD_CLASS_TESTER_COMPETENCIES.md)
