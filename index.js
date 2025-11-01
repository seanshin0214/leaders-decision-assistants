#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import os from 'os';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 페르소나 저장 디렉토리
const PERSONA_DIR = path.join(os.homedir(), '.persona');

// 페르소나 디렉토리 초기화
async function initPersonaDir() {
  try {
    await fs.mkdir(PERSONA_DIR, { recursive: true });
  } catch (error) {
    console.error('Failed to create persona directory:', error);
  }
}

// 페르소나 파일 목록 가져오기
async function listPersonas() {
  try {
    const files = await fs.readdir(PERSONA_DIR);
    return files.filter(f => f.endsWith('.txt')).map(f => f.replace('.txt', ''));
  } catch (error) {
    return [];
  }
}

// 페르소나 읽기
async function readPersona(name) {
  const filePath = path.join(PERSONA_DIR, `${name}.txt`);
  try {
    const content = await fs.readFile(filePath, 'utf-8');
    return content;
  } catch (error) {
    throw new Error(`Persona "${name}" not found`);
  }
}

// 페르소나 저장
async function savePersona(name, content) {
  const filePath = path.join(PERSONA_DIR, `${name}.txt`);
  await fs.writeFile(filePath, content, 'utf-8');
}

// 페르소나 삭제
async function deletePersona(name) {
  const filePath = path.join(PERSONA_DIR, `${name}.txt`);
  await fs.unlink(filePath);
}

// MCP 서버 생성
const server = new Server(
  {
    name: 'persona-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
      resources: {},
    },
  }
);

// 도구 목록
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'create_persona',
        description: '새로운 페르소나 프로필을 생성합니다',
        inputSchema: {
          type: 'object',
          properties: {
            name: {
              type: 'string',
              description: '페르소나 이름 (예: default, professional, casual)',
            },
            content: {
              type: 'string',
              description: '페르소나 프롬프트 내용',
            },
          },
          required: ['name', 'content'],
        },
      },
      {
        name: 'update_persona',
        description: '기존 페르소나 프로필을 수정합니다',
        inputSchema: {
          type: 'object',
          properties: {
            name: {
              type: 'string',
              description: '수정할 페르소나 이름',
            },
            content: {
              type: 'string',
              description: '새로운 페르소나 프롬프트 내용',
            },
          },
          required: ['name', 'content'],
        },
      },
      {
        name: 'delete_persona',
        description: '페르소나 프로필을 삭제합니다',
        inputSchema: {
          type: 'object',
          properties: {
            name: {
              type: 'string',
              description: '삭제할 페르소나 이름',
            },
          },
          required: ['name'],
        },
      },
      {
        name: 'list_personas',
        description: '사용 가능한 모든 페르소나 목록을 조회합니다',
        inputSchema: {
          type: 'object',
          properties: {},
        },
      },
    ],
  };
});

// 도구 실행
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'create_persona': {
        await savePersona(args.name, args.content);
        return {
          content: [
            {
              type: 'text',
              text: `페르소나 "${args.name}"이(가) 생성되었습니다.\n위치: ${path.join(PERSONA_DIR, args.name + '.txt')}`,
            },
          ],
        };
      }

      case 'update_persona': {
        await savePersona(args.name, args.content);
        return {
          content: [
            {
              type: 'text',
              text: `페르소나 "${args.name}"이(가) 업데이트되었습니다.`,
            },
          ],
        };
      }

      case 'delete_persona': {
        await deletePersona(args.name);
        return {
          content: [
            {
              type: 'text',
              text: `페르소나 "${args.name}"이(가) 삭제되었습니다.`,
            },
          ],
        };
      }

      case 'list_personas': {
        const personas = await listPersonas();
        return {
          content: [
            {
              type: 'text',
              text: personas.length > 0
                ? `사용 가능한 페르소나:\n${personas.map(p => `- ${p}`).join('\n')}\n\n사용법: @persona:${personas[0]} 형식으로 참조하세요.`
                : '저장된 페르소나가 없습니다.',
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: `오류: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

// 리소스 목록
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  const personas = await listPersonas();
  return {
    resources: personas.map(name => ({
      uri: `persona://${name}`,
      mimeType: 'text/plain',
      name: `Persona: ${name}`,
      description: `${name} 페르소나 프로필`,
    })),
  };
});

// 리소스 읽기
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;
  const match = uri.match(/^persona:\/\/(.+)$/);

  if (!match) {
    throw new Error('Invalid persona URI');
  }

  const personaName = match[1];
  const content = await readPersona(personaName);

  return {
    contents: [
      {
        uri,
        mimeType: 'text/plain',
        text: content,
      },
    ],
  };
});

// 서버 시작
async function main() {
  await initPersonaDir();

  const transport = new StdioServerTransport();
  await server.connect(transport);

  console.error('Persona MCP server running on stdio');
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
