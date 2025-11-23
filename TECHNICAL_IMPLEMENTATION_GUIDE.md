# 🔧 기술 구현 가이드: 기능적 페르소나 MCP 서버

**목표**: 정적 텍스트 페르소나 → 동적 기능 기반 MCP 서버 전환

---

## 📁 파일 구조 (v3.0.0)

```
persona-mcp/
├── src/
│   ├── index.ts (기존 - 확장 필요)
│   ├── validation.ts (기존 - 유지)
│   ├── sampling.ts (신규)
│   ├── resources.ts (신규)
│   ├── tools.ts (신규)
│   ├── caching.ts (신규)
│   └── personaLoader.ts (신규)
├── community/
│   ├── 101-fullstack-dev.txt (YAML Frontmatter 추가)
│   ├── 410-llm-engineer.txt (YAML Frontmatter 추가)
│   └── ... (142개 모두 변환)
├── examples/
│   └── 410-llm-engineer-functional.txt (✅ 완료)
├── FUNCTIONAL_PERSONA_UPGRADE_PLAN.md (✅ 완료)
└── TECHNICAL_IMPLEMENTATION_GUIDE.md (현재 문서)
```

---

## 🎯 Phase 1: 페르소나 로더 구현

### personaLoader.ts

```typescript
import fs from 'fs/promises';
import yaml from 'yaml';
import path from 'path';

export interface PersonaMetadata {
  name: string;
  id: number;
  version: string;
  category: string;
  domain: string;
  author?: string;
  created?: string;
  updated?: string;
  
  // Capabilities
  tools?: ToolMetadata[];
  resources?: ResourceMetadata[];
  prompts?: PromptMetadata[];
  
  // Configuration
  sampling_enabled?: boolean;
  sampling_use_cases?: string[];
  context_caching?: boolean;
  cache_breakpoints?: number;
  min_tokens?: number;
  recommended_agreement_level?: number;
}

export interface ToolMetadata {
  name: string;
  description: string;
  category: string;
  input_schema?: any;
}

export interface ResourceMetadata {
  uri_template: string;
  description: string;
  mime_type?: string;
  examples?: string[];
}

export interface PromptMetadata {
  name: string;
  description: string;
  arguments?: Record<string, string>;
}

export interface PersonaContent {
  metadata: PersonaMetadata;
  markdown: string;
}

export class PersonaLoader {
  async loadPersona(filePath: string): Promise<PersonaContent> {
    const content = await fs.readFile(filePath, 'utf-8');
    
    // YAML Frontmatter 파싱
    if (content.startsWith('---\n')) {
      const parts = content.split('---\n');
      if (parts.length >= 3) {
        const yamlContent = parts[1];
        const markdownContent = parts.slice(2).join('---\n');
        
        const metadata = yaml.parse(yamlContent) as PersonaMetadata;
        
        return {
          metadata,
          markdown: markdownContent.trim()
        };
      }
    }
    
    // Legacy format (순수 Markdown)
    return {
      metadata: this.createDefaultMetadata(filePath),
      markdown: content
    };
  }
  
  private createDefaultMetadata(filePath: string): PersonaMetadata {
    const filename = path.basename(filePath, '.txt');
    const match = filename.match(/^(\d+)-(.+)$/);
    
    return {
      name: match ? match[2].replace(/-/g, ' ') : filename,
      id: match ? parseInt(match[1]) : 0,
      version: '2.4.0',
      category: 'unknown',
      domain: 'general'
    };
  }
  
  async loadAllPersonas(directory: string): Promise<Map<string, PersonaContent>> {
    const personas = new Map<string, PersonaContent>();
    const files = await fs.readdir(directory);
    
    for (const file of files) {
      if (file.endsWith('.txt')) {
        const personaId = file.replace('.txt', '');
        const filePath = path.join(directory, file);
        const persona = await this.loadPersona(filePath);
        personas.set(personaId, persona);
      }
    }
    
    return personas;
  }
}
```

---

## 🔧 Phase 2: Tools 구현

### tools.ts

```typescript
import { CallToolRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { PersonaMetadata } from './personaLoader.js';

export interface ToolDefinition {
  name: string;
  description: string;
  inputSchema: {
    type: 'object';
    properties: Record<string, any>;
    required?: string[];
  };
  handler: (args: any) => Promise<any>;
}

export class PersonaToolsRegistry {
  private tools: Map<string, Map<string, ToolDefinition>> = new Map();
  
  registerTools(personaId: string, metadata: PersonaMetadata) {
    if (!metadata.tools) return;
    
    const personaTools = new Map<string, ToolDefinition>();
    
    for (const toolMeta of metadata.tools) {
      const tool = this.createToolFromMetadata(personaId, toolMeta);
      personaTools.set(tool.name, tool);
    }
    
    this.tools.set(personaId, personaTools);
  }
  
  private createToolFromMetadata(
    personaId: string,
    toolMeta: any
  ): ToolDefinition {
    return {
      name: toolMeta.name,
      description: toolMeta.description,
      inputSchema: {
        type: 'object',
        properties: toolMeta.input_schema || {},
        required: this.extractRequired(toolMeta.input_schema)
      },
      handler: this.getHandler(personaId, toolMeta.name)
    };
  }
  
  private extractRequired(schema: any): string[] {
    if (!schema) return [];
    return Object.entries(schema)
      .filter(([_, v]: [string, any]) => v.required === true)
      .map(([k, _]) => k);
  }
  
  private getHandler(personaId: string, toolName: string) {
    // Dynamic handler lookup
    const handlers = {
      '410-llm-engineer': this.getLLMEngineerHandlers(),
      '108-devops-engineer': this.getDevOpsHandlers(),
      '223-ux-researcher': this.getUXResearcherHandlers()
      // ... 142개 페르소나 매핑
    };
    
    const personaHandlers = handlers[personaId as keyof typeof handlers];
    return personaHandlers?.[toolName] || this.defaultHandler;
  }
  
  private getLLMEngineerHandlers() {
    return {
      analyze_transformer_architecture: async (args: any) => {
        const { model_config, target_metrics = ['latency'] } = args;
        
        // 실제 분석 로직
        const numParams = this.calculateParameters(model_config);
        const flops = this.estimateFLOPs(model_config);
        const memory = this.estimateMemory(model_config);
        
        const recommendations = [];
        if (target_metrics.includes('latency')) {
          recommendations.push('Use FlashAttention for 2x speedup');
        }
        if (target_metrics.includes('memory')) {
          recommendations.push('Apply INT8 quantization for 4x reduction');
        }
        
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              model_size: `${numParams / 1e9}B parameters`,
              estimated_flops: `${flops / 1e12}T FLOPs`,
              memory_usage: `${memory} GB`,
              recommendations,
              estimated_improvements: {
                latency: '-40%',
                memory: '-75%'
              }
            }, null, 2)
          }]
        };
      },
      
      design_prompt_template: async (args: any) => {
        const { task_description, input_schema, output_format = 'json' } = args;
        
        const template = `<role>
You are an expert specialized in ${task_description}
</role>

<task>
${task_description}
</task>

<input>
${JSON.stringify(input_schema, null, 2)}
</input>

<instructions>
1. Analyze the input carefully
2. Apply best practices
3. Generate output in ${output_format} format
</instructions>

<output_format>
${this.generateOutputFormat(output_format)}
</output_format>`;
        
        return {
          content: [{ type: 'text', text: template }]
        };
      },
      
      estimate_inference_cost: async (args: any) => {
        const { model_name, requests_per_day, avg_input_tokens = 1000, avg_output_tokens = 500 } = args;
        
        const pricing = this.getPricing(model_name);
        const dailyCost = requests_per_day * (
          (avg_input_tokens / 1000000) * pricing.input +
          (avg_output_tokens / 1000000) * pricing.output
        );
        
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              daily_cost: dailyCost.toFixed(2),
              monthly_cost: (dailyCost * 30).toFixed(2),
              annual_cost: (dailyCost * 365).toFixed(2),
              breakdown: {
                input_tokens_cost: (requests_per_day * avg_input_tokens / 1000000 * pricing.input).toFixed(2),
                output_tokens_cost: (requests_per_day * avg_output_tokens / 1000000 * pricing.output).toFixed(2)
              },
              optimization_suggestions: [
                `Implement prompt caching: save $${(dailyCost * 0.3 * 30).toFixed(0)}/month`,
                `Use shorter system prompts: save $${(dailyCost * 0.15 * 30).toFixed(0)}/month`
              ]
            }, null, 2)
          }]
        };
      }
    };
  }
  
  private getDevOpsHandlers() {
    return {
      diagnose_pipeline: async (args: any) => {
        // CI/CD 파이프라인 진단 로직
        return {
          content: [{
            type: 'text',
            text: 'Pipeline diagnosis complete...'
          }]
        };
      }
    };
  }
  
  private getUXResearcherHandlers() {
    return {
      design_research_plan: async (args: any) => {
        // UX 리서치 계획 생성 로직
        return {
          content: [{
            type: 'text',
            text: '# UX Research Plan\n\n...'
          }]
        };
      }
    };
  }
  
  private defaultHandler = async (args: any) => {
    return {
      content: [{
        type: 'text',
        text: 'Tool not yet implemented'
      }]
    };
  };
  
  // 헬퍼 메서드
  private calculateParameters(config: any): number {
    const { num_layers = 12, hidden_size = 768, num_heads = 12, vocab_size = 50257 } = config;
    // 간략화된 계산
    return num_layers * hidden_size * hidden_size * 12 + vocab_size * hidden_size;
  }
  
  private estimateFLOPs(config: any): number {
    // 간략화된 FLOPs 추정
    return this.calculateParameters(config) * 2;
  }
  
  private estimateMemory(config: any): number {
    // bytes → GB
    return (this.calculateParameters(config) * 4) / (1024 ** 3);
  }
  
  private generateOutputFormat(format: string): string {
    if (format === 'json') {
      return '{\n  "result": "...",\n  "confidence": 0.95\n}';
    } else if (format === 'xml') {
      return '<result>\n  <text>...</text>\n  <confidence>0.95</confidence>\n</result>';
    } else {
      return '# Result\n\n...';
    }
  }
  
  private getPricing(model: string): { input: number, output: number } {
    const prices: Record<string, { input: number, output: number }> = {
      'gpt-4': { input: 30, output: 60 },
      'gpt-4-turbo': { input: 10, output: 30 },
      'claude-3-opus': { input: 15, output: 75 },
      'claude-3-sonnet': { input: 3, output: 15 },
      'claude-3-haiku': { input: 0.25, output: 1.25 }
    };
    return prices[model] || { input: 1, output: 2 };
  }
  
  getToolsForPersona(personaId: string): ToolDefinition[] {
    const personaTools = this.tools.get(personaId);
    return personaTools ? Array.from(personaTools.values()) : [];
  }
  
  async executeTool(personaId: string, toolName: string, args: any): Promise<any> {
    const personaTools = this.tools.get(personaId);
    if (!personaTools) {
      throw new Error(`No tools for persona ${personaId}`);
    }
    
    const tool = personaTools.get(toolName);
    if (!tool) {
      throw new Error(`Tool ${toolName} not found`);
    }
    
    return await tool.handler(args);
  }
}
```

---

## 📚 Phase 3: Resources 구현

### resources.ts

```typescript
import { ReadResourceRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { PersonaMetadata } from './personaLoader.js';

export class DynamicResourceProvider {
  private resourceHandlers: Map<string, (uri: string) => Promise<any>> = new Map();
  
  constructor() {
    this.registerDefaultHandlers();
  }
  
  registerFromPersona(metadata: PersonaMetadata) {
    if (!metadata.resources) return;
    
    for (const resource of metadata.resources) {
      const prefix = this.extractPrefix(resource.uri_template);
      if (!this.resourceHandlers.has(prefix)) {
        this.resourceHandlers.set(prefix, this.createHandlerForTemplate(resource.uri_template));
      }
    }
  }
  
  private registerDefaultHandlers() {
    // LLM Papers
    this.resourceHandlers.set('llm://papers/', async (uri) => {
      const topic = this.extractParam(uri, 'llm://papers/{topic}');
      return this.fetchLLMPapers(topic);
    });
    
    // Code Examples
    this.resourceHandlers.set('code://examples/', async (uri) => {
      const language = this.extractParam(uri, 'code://examples/{language}');
      return this.fetchCodeExamples(language);
    });
    
    // Benchmarks
    this.resourceHandlers.set('llm://benchmarks/', async (uri) => {
      const params = this.extractMultiParam(uri, 'llm://benchmarks/{model}/{task}');
      return this.fetchBenchmarks(params.model, params.task);
    });
  }
  
  private extractPrefix(template: string): string {
    return template.split('{')[0];
  }
  
  private createHandlerForTemplate(template: string) {
    return async (uri: string) => {
      const params = this.extractAllParams(uri, template);
      return { template, params, uri };
    };
  }
  
  private extractParam(uri: string, template: string): string {
    const templateRegex = template.replace(/{(\w+)}/g, '([^/]+)');
    const match = uri.match(new RegExp(templateRegex));
    return match?.[1] || '';
  }
  
  private extractMultiParam(uri: string, template: string): Record<string, string> {
    const paramNames = (template.match(/{(\w+)}/g) || []).map(p => p.slice(1, -1));
    const templateRegex = template.replace(/{(\w+)}/g, '([^/]+)');
    const match = uri.match(new RegExp(templateRegex));
    
    const result: Record<string, string> = {};
    if (match) {
      paramNames.forEach((name, i) => {
        result[name] = match[i + 1];
      });
    }
    return result;
  }
  
  private extractAllParams(uri: string, template: string): Record<string, string> {
    return this.extractMultiParam(uri, template);
  }
  
  async handleResourceRead(uri: string): Promise<any> {
    for (const [prefix, handler] of this.resourceHandlers) {
      if (uri.startsWith(prefix)) {
        return await handler(uri);
      }
    }
    throw new Error(`Unknown resource URI: ${uri}`);
  }
  
  // 실제 데이터 페칭 메서드들
  private async fetchLLMPapers(topic: string): Promise<any> {
    // 실제 구현에서는 arXiv API 또는 로컬 캐시 사용
    const papers: Record<string, any[]> = {
      'transformers': [
        {
          title: 'Attention Is All You Need',
          authors: ['Vaswani et al.'],
          year: 2017,
          url: 'https://arxiv.org/abs/1706.03762',
          key_contributions: ['Self-attention mechanism', 'No recurrence']
        }
      ],
      'prompt-engineering': [
        {
          title: 'Chain-of-Thought Prompting Elicits Reasoning',
          authors: ['Wei et al.'],
          year: 2022,
          url: 'https://arxiv.org/abs/2201.11903'
        }
      ]
    };
    
    return {
      topic,
      papers: papers[topic] || [],
      updated: new Date().toISOString()
    };
  }
  
  private async fetchCodeExamples(language: string): Promise<any> {
    // GitHub API 또는 로컬 저장소
    const examples: Record<string, any> = {
      'python': {
        language: 'python',
        examples: [
          {
            title: 'FastAPI Best Practices',
            code: 'from fastapi import FastAPI\n\napp = FastAPI()',
            description: 'Modern async web framework'
          }
        ]
      }
    };
    
    return examples[language] || { language, examples: [] };
  }
  
  private async fetchBenchmarks(model: string, task: string): Promise<any> {
    // 벤치마크 데이터베이스
    const benchmarks: Record<string, any> = {
      'gpt-4-coding': {
        model: 'gpt-4',
        task: 'coding',
        benchmarks: {
          'HumanEval': { score: 85.4, rank: 1 },
          'MBPP': { score: 82.3, rank: 1 }
        }
      }
    };
    
    return benchmarks[`${model}-${task}`] || { model, task, benchmarks: {} };
  }
}
```

---

## 🔄 Phase 4: Sampling 구현

### sampling.ts

```typescript
export interface SamplingContext {
  session: {
    createMessage(params: {
      messages: Array<{ role: string; content: { type: string; text: string } }>;
      systemPrompt?: string;
      maxTokens?: number;
    }): Promise<{ content: { text: string } }>;
  };
}

export class ExpertSampler {
  /**
   * ExpertPrompting: 전문가 정체성 동적 생성
   */
  async generateExpertIdentity(
    domain: string,
    task: string,
    ctx: SamplingContext
  ): Promise<string> {
    const response = await ctx.session.createMessage({
      messages: [{
        role: 'user',
        content: {
          type: 'text',
          text: `Domain: ${domain}\nTask: ${task}\n\nWhat specific expertise is needed? Generate expert identity (2-3 sentences).`
        }
      }],
      systemPrompt: 'You are an expert identity generator.',
      maxTokens: 200
    });
    
    return response.content.text;
  }
  
  /**
   * Solo Performance Prompting (SPP): 다중 페르소나 협업
   */
  async collaborativeReasoning(
    problem: string,
    personas: string[],
    ctx: SamplingContext
  ): Promise<string> {
    const proposals: string[] = [];
    
    // Phase 1: 발산
    for (const persona of personas) {
      const response = await ctx.session.createMessage({
        messages: [{
          role: 'user',
          content: {
            type: 'text',
            text: `As a ${persona}, propose solution to: ${problem}`
          }
        }],
        maxTokens: 300
      });
      proposals.push(response.content.text);
    }
    
    // Phase 2: 비평
    const critique = await ctx.session.createMessage({
      messages: [{
        role: 'user',
        content: {
          type: 'text',
          text: `Critically review:\n\n${proposals.join('\n\n')}\n\nIdentify weaknesses.`
        }
      }],
      systemPrompt: 'You are a rigorous critic.',
      maxTokens: 500
    });
    
    // Phase 3: 통합
    const final = await ctx.session.createMessage({
      messages: [{
        role: 'user',
        content: {
          type: 'text',
          text: `Proposals:\n${proposals.join('\n\n')}\n\nCritique:\n${critique.content.text}\n\nSynthesize best solution.`
        }
      }],
      systemPrompt: 'You are a problem-solving expert.',
      maxTokens: 800
    });
    
    return final.content.text;
  }
  
  /**
   * Multi-Persona Debate
   */
  async debate(
    question: string,
    agreementLevel: number,
    rounds: number,
    ctx: SamplingContext
  ): Promise<string> {
    // Round 1
    const agent1 = await ctx.session.createMessage({
      messages: [{ role: 'user', content: { type: 'text', text: question } }],
      systemPrompt: `Agreement level: ${agreementLevel}%`,
      maxTokens: 400
    });
    
    // Round 2
    const agent2 = await ctx.session.createMessage({
      messages: [{
        role: 'user',
        content: {
          type: 'text',
          text: `Previous: ${agent1.content.text}\n\nYour perspective?`
        }
      }],
      systemPrompt: `Agreement level: ${agreementLevel}%`,
      maxTokens: 400
    });
    
    // Round 3: Vote
    const vote = await ctx.session.createMessage({
      messages: [{
        role: 'user',
        content: {
          type: 'text',
          text: `1. ${agent1.content.text}\n\n2. ${agent2.content.text}\n\nWhich is better?`
        }
      }],
      systemPrompt: 'You are an objective evaluator.',
      maxTokens: 300
    });
    
    return vote.content.text;
  }
}
```

---

## 📦 Phase 5: index.ts 통합

### 주요 변경사항

```typescript
// 기존 import에 추가
import { PersonaLoader } from './personaLoader.js';
import { PersonaToolsRegistry } from './tools.js';
import { DynamicResourceProvider } from './resources.js';
import { ExpertSampler } from './sampling.js';

// 초기화
const personaLoader = new PersonaLoader();
const toolsRegistry = new PersonaToolsRegistry();
const resourceProvider = new DynamicResourceProvider();
const sampler = new ExpertSampler();

// 서버 시작 시 모든 페르소나 로드
const personas = await personaLoader.loadAllPersonas(COMMUNITY_DIR);
for (const [id, persona] of personas) {
  toolsRegistry.registerTools(id, persona.metadata);
  resourceProvider.registerFromPersona(persona.metadata);
}

// ListToolsRequestSchema 핸들러 수정
server.setRequestHandler(ListToolsRequestSchema, async (request) => {
  // 현재 활성화된 페르소나의 Tools 반환
  const currentPersona = getCurrentPersona(); // 컨텍스트에서 가져오기
  const tools = toolsRegistry.getToolsForPersona(currentPersona);
  return { tools };
});

// CallToolRequestSchema 핸들러 수정
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const currentPersona = getCurrentPersona();
  return await toolsRegistry.executeTool(
    currentPersona,
    request.params.name,
    request.params.arguments
  );
});

// ReadResourceRequestSchema 핸들러 추가
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const data = await resourceProvider.handleResourceRead(request.params.uri);
  return {
    contents: [{
      uri: request.params.uri,
      mimeType: 'application/json',
      text: JSON.stringify(data, null, 2)
    }]
  };
});
```

---

## ✅ 구현 체크리스트

### Week 1-2
- [ ] `personaLoader.ts` 구현
- [ ] 10개 핵심 페르소나 YAML 변환
- [ ] 통합 테스트

### Week 3-4
- [ ] `tools.ts` 구현 (30개 Tools)
- [ ] `resources.ts` 구현 (5개 URI schemes)
- [ ] `sampling.ts` 프로토타입

### Week 5-6
- [ ] Caching 전략 문서화
- [ ] Progressive Disclosure 적용
- [ ] 성능 벤치마크

### Week 7-8
- [ ] 142개 페르소나 전체 변환
- [ ] 500+ Tools 완성
- [ ] 통합 테스트

### Week 9-10
- [ ] 프로덕션 배포
- [ ] 문서화 완성
- [ ] v3.0.0 Release

---

**다음 단계**: 10개 핵심 페르소나 변환 시작
