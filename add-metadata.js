#!/usr/bin/env node

import fs from 'fs/promises';
import path from 'path';

const SOURCE_DIR = 'C:\\Users\\Sean K. S. Shin\\.persona';
const DEST_DIR = 'C:\\Users\\Sean K. S. Shin\\Documents\\persona-mcp\\community';

// 카테고리 매핑 (파일명 패턴으로 자동 분류)
const categoryMap = {
  'innovation': 'Business & Innovation',
  'business': 'Business & Professional',
  'education': 'Education & Learning',
  'intl': 'Education & Learning',
  'student': 'Education & Learning',
  'strategy': 'Business & Professional',
  'fullstack': 'Programming & Tech',
  'ai-engineer': 'Programming & Tech',
  'data-engineer': 'Programming & Tech',
  'analytics': 'Business & Professional',
  'devops': 'Programming & Tech',
  'product': 'Business & Professional',
  'startup': 'Business & Innovation',
  'entrepreneur': 'Business & Innovation',
  'vp': 'Business & Professional',
  'tutor': 'Education & Learning',
  'college': 'Education & Learning',
  'university': 'Education & Learning',
  'harvard': 'Education & Learning',
  'law': 'Business & Professional',
  'negotiation': 'Business & Professional'
};

function getCategory(filename) {
  const lower = filename.toLowerCase();
  for (const [key, category] of Object.entries(categoryMap)) {
    if (lower.includes(key)) {
      return category;
    }
  }
  return 'Business & Professional'; // default
}

function getDifficulty(filename) {
  // 전문가 수준 페르소나는 Advanced
  if (filename.includes('vp') || filename.includes('harvard') || filename.includes('president')) {
    return 'Advanced';
  }
  // 기술 관련은 Intermediate to Advanced
  if (filename.includes('engineer') || filename.includes('dev')) {
    return 'Intermediate to Advanced';
  }
  // 교육 관련은 All levels
  if (filename.includes('tutor') || filename.includes('education')) {
    return 'All levels';
  }
  return 'Intermediate to Advanced';
}

async function processFile(filename) {
  const sourcePath = path.join(SOURCE_DIR, filename);
  const content = await fs.readFile(sourcePath, 'utf-8');

  // 첫 번째 줄에서 페르소나 이름 추출
  const firstLine = content.split('\\n')[0].replace('#', '').trim();
  const personaName = firstLine;

  // 파일명에서 번호 제거
  const cleanName = filename.replace(/^\d+-/, '').replace('.txt', '');

  const category = getCategory(cleanName);
  const difficulty = getDifficulty(cleanName);

  // 메타데이터 생성
  const metadata = `# Persona: ${personaName}
# Author: @seanshin0214 (Sean Shin - Founder of Persona MCP)
# Category: ${category}
# Difficulty: ${difficulty}
# Use Cases: ${getUseCases(cleanName)}
# Version: 1.0
# License: MIT (Free on GitHub, Premium versions available on Persona Hub)

`;

  // 메타데이터 + 원본 내용
  const newContent = metadata + content;

  // community/ 디렉토리에 저장
  const destPath = path.join(DEST_DIR, cleanName + '.txt');
  await fs.writeFile(destPath, newContent, 'utf-8');

  console.log(`✅ Processed: ${filename} → ${cleanName}.txt`);
}

function getUseCases(cleanName) {
  const useCaseMap = {
    'innovation-expert': 'Startup ecosystem design, accelerator programs, entrepreneurship education',
    'business-mgmt': 'Business strategy, management consulting, organizational development',
    'education-policy': 'Education policy analysis, institutional strategy, reform planning',
    'intl-education': 'International education strategy, student mobility, global partnerships',
    'student-mobility': 'Study abroad programs, international recruitment, exchange partnerships',
    'strategy-consultant': 'Strategic planning, business analysis, competitive strategy',
    'fullstack-dev': 'Web development, system architecture, full-stack coding',
    'ai-engineer': 'AI/ML development, model training, AI system design',
    'data-engineer': 'Data pipeline, ETL, data infrastructure, big data',
    'business-analytics': 'Business intelligence, data analysis, KPI tracking',
    'education-analytics': 'Educational data analysis, learning outcomes, institutional research',
    'devops-engineer': 'CI/CD, infrastructure, cloud deployment, automation',
    'product-manager': 'Product strategy, roadmap planning, feature prioritization',
    'global-startup': 'Global expansion, international markets, startup scaling',
    'disruptive-entrepreneur': 'Disruptive innovation, market entry, entrepreneurship',
    'vp-innovation': 'Innovation strategy, R&D management, corporate innovation',
    'elite-tutor': 'Academic tutoring, college prep, exam strategy',
    'college-consultant': 'College admissions, application strategy, career planning',
    'university-president': 'University leadership, institutional strategy, higher education',
    'harvard-law-dispute': 'Legal dispute resolution, negotiation, conflict management',
    'harvard-phd-negotiation': 'Academic negotiation, research collaboration, partnership building'
  };

  return useCaseMap[cleanName] || 'Professional consulting, strategic advice, expert guidance';
}

async function main() {
  console.log('🚀 Adding metadata to all personas...\\n');

  const files = await fs.readdir(SOURCE_DIR);
  const txtFiles = files.filter(f => f.endsWith('.txt'));

  for (const file of txtFiles) {
    await processFile(file);
  }

  console.log(`\\n✅ Processed ${txtFiles.length} personas!`);
  console.log('📁 Saved to: ' + DEST_DIR);
}

main().catch(console.error);
