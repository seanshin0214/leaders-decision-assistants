"""
Persona MCP - Supabase Knowledge Upload Script
페르소나 지식을 Supabase에 벡터화하여 업로드

사용법:
    export SUPABASE_URL="your-project-url"
    export SUPABASE_KEY="your-service-key"
    export OPENAI_API_KEY="your-openai-key"

    python supabase/upload_personas.py
    python supabase/upload_personas.py --persona 410-llm-engineer
    python supabase/upload_personas.py --dry-run
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
import argparse

try:
    from supabase import create_client, Client
    from openai import OpenAI
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install supabase openai")
    sys.exit(1)


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def parse_persona_file(file_path: Path) -> Dict[str, Any]:
    """
    페르소나 마크다운 파일 파싱

    Returns:
        {
            "id": "410-llm-engineer",
            "name": "LLM Engineer",
            "category": "ai_data",
            "content": "...",
            "sections": [{"title": "...", "content": "..."}, ...]
        }
    """
    content = file_path.read_text(encoding='utf-8')
    filename = file_path.stem

    # ID 추출 (예: "410-llm-engineer")
    persona_id = filename.lower().replace(' ', '-')

    # 이름 추출 (헤더에서)
    name_match = re.search(r'^#\s*(.+?)(?:\s*\(|$)', content, re.MULTILINE)
    name = name_match.group(1).strip() if name_match else filename

    # 카테고리 추론
    try:
        num = int(filename.split('-')[0])
        if 100 <= num < 200:
            category = "engineering"
        elif 200 <= num < 300:
            category = "design_creative"
        elif 300 <= num < 400:
            category = "business_leadership"
        elif 400 <= num < 500:
            category = "ai_data"
        elif 500 <= num < 600:
            category = "testing_qa"
        elif 600 <= num < 700:
            category = "education"
        elif 700 <= num < 800:
            category = "healthcare"
        else:
            category = "other"
    except:
        category = "other"

    # 섹션 분리 (## 헤더 기준)
    sections = []
    current_section = {"title": "Overview", "content": ""}
    lines = content.split('\n')

    for line in lines:
        if line.startswith('## '):
            if current_section["content"].strip():
                sections.append(current_section)
            current_section = {
                "title": line[3:].strip(),
                "content": ""
            }
        else:
            current_section["content"] += line + "\n"

    if current_section["content"].strip():
        sections.append(current_section)

    return {
        "id": persona_id,
        "name": name,
        "category": category,
        "full_content": content,
        "sections": sections
    }


def chunk_content(parsed: Dict[str, Any], max_chunk_size: int = 1500) -> List[Dict[str, Any]]:
    """
    페르소나 내용을 청크로 분할

    Returns:
        [{"id": "410-llm-engineer-001", "content": "...", "section": "...", "metadata": {...}}, ...]
    """
    chunks = []
    persona_id = parsed["id"]
    chunk_idx = 0

    for section in parsed["sections"]:
        content = section["content"].strip()
        if not content:
            continue

        # 큰 섹션은 분할
        if len(content) > max_chunk_size:
            paragraphs = content.split('\n\n')
            current_chunk = ""

            for para in paragraphs:
                if len(current_chunk) + len(para) > max_chunk_size and current_chunk:
                    chunks.append({
                        "id": f"{persona_id}-{chunk_idx:03d}",
                        "content": current_chunk.strip(),
                        "section": section["title"],
                        "metadata": {
                            "persona_id": persona_id,
                            "persona_name": parsed["name"],
                            "section": section["title"]
                        }
                    })
                    chunk_idx += 1
                    current_chunk = para
                else:
                    current_chunk += "\n\n" + para if current_chunk else para

            if current_chunk.strip():
                chunks.append({
                    "id": f"{persona_id}-{chunk_idx:03d}",
                    "content": current_chunk.strip(),
                    "section": section["title"],
                    "metadata": {
                        "persona_id": persona_id,
                        "persona_name": parsed["name"],
                        "section": section["title"]
                    }
                })
                chunk_idx += 1
        else:
            chunks.append({
                "id": f"{persona_id}-{chunk_idx:03d}",
                "content": content,
                "section": section["title"],
                "metadata": {
                    "persona_id": persona_id,
                    "persona_name": parsed["name"],
                    "section": section["title"]
                }
            })
            chunk_idx += 1

    return chunks


def generate_embedding(client: OpenAI, text: str) -> List[float]:
    """텍스트 임베딩 생성"""
    max_chars = 8000 * 4
    if len(text) > max_chars:
        text = text[:max_chars]

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def upload_persona(
    supabase: Client,
    openai_client: OpenAI,
    parsed: Dict[str, Any],
    chunks: List[Dict[str, Any]],
    dry_run: bool = False
) -> Dict[str, int]:
    """페르소나와 청크들을 업로드"""
    results = {"persona": 0, "chunks": 0, "errors": 0}

    # 1. personas 테이블에 페르소나 정보 삽입
    persona_data = {
        "id": parsed["id"],
        "name": parsed["name"],
        "category": parsed["category"],
        "description": parsed["sections"][0]["content"][:500] if parsed["sections"] else ""
    }

    if dry_run:
        print(f"  [DRY RUN] Would upload persona: {parsed['id']}")
        results["persona"] = 1
    else:
        try:
            supabase.table('personas').upsert(persona_data).execute()
            results["persona"] = 1
        except Exception as e:
            print(f"  Error uploading persona: {e}")
            results["errors"] += 1

    # 2. persona_knowledge 테이블에 청크들 삽입
    for chunk in chunks:
        if dry_run:
            print(f"  [DRY RUN] Would upload chunk: {chunk['id']}")
            results["chunks"] += 1
            continue

        try:
            # 임베딩 생성
            embedding = generate_embedding(openai_client, chunk["content"])

            chunk_data = {
                "id": chunk["id"],
                "persona_id": parsed["id"],
                "content": chunk["content"],
                "section": chunk["section"],
                "embedding": embedding
            }

            supabase.table('persona_knowledge').upsert(chunk_data).execute()
            results["chunks"] += 1
            print(f"  Uploaded: {chunk['id']}")

        except Exception as e:
            print(f"  Error uploading chunk {chunk['id']}: {e}")
            results["errors"] += 1

    return results


def main():
    parser = argparse.ArgumentParser(description='Upload persona knowledge to Supabase')
    parser.add_argument('--persona', type=str, help='Upload specific persona only (ID or filename)')
    parser.add_argument('--dry-run', action='store_true', help='Parse without uploading')
    parser.add_argument('--knowledge-dir', type=str, help='Knowledge directory path')
    args = parser.parse_args()

    # 환경변수 확인
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY')
    openai_key = os.environ.get('OPENAI_API_KEY')

    if not all([supabase_url, supabase_key, openai_key]) and not args.dry_run:
        print("Error: Missing environment variables")
        print("Required: SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY")
        sys.exit(1)

    # 클라이언트 초기화
    supabase = None
    openai_client = None
    if not args.dry_run:
        supabase = create_client(supabase_url, supabase_key)
        openai_client = OpenAI(api_key=openai_key)

    # Knowledge 폴더 경로 찾기
    project_root = get_project_root()
    possible_dirs = [
        args.knowledge_dir,
        project_root / "gpts-knowledge",
        project_root / "gpt-knowledge",
        project_root / "knowledge-base",
        project_root / "community"
    ]

    knowledge_dir = None
    for d in possible_dirs:
        if d and Path(d).exists():
            knowledge_dir = Path(d)
            break

    if not knowledge_dir:
        print("Error: Knowledge directory not found")
        print(f"Checked: {[str(d) for d in possible_dirs if d]}")
        sys.exit(1)

    print(f"Knowledge directory: {knowledge_dir}")

    # 파일 목록
    if args.persona:
        # 특정 페르소나만
        pattern = f"*{args.persona}*.md"
        files = list(knowledge_dir.glob(pattern))
        if not files:
            files = list(knowledge_dir.rglob(pattern))
    else:
        # 모든 페르소나
        files = list(knowledge_dir.glob("*.md"))
        if not files:
            files = list(knowledge_dir.rglob("*.md"))

    # README 등 제외
    files = [f for f in files if not f.name.lower().startswith('readme')]

    print(f"Found {len(files)} persona files\n")

    # 업로드 실행
    total_results = {"personas": 0, "chunks": 0, "errors": 0}

    for file_path in files:
        print(f"Processing: {file_path.name}")

        try:
            parsed = parse_persona_file(file_path)
            chunks = chunk_content(parsed)

            print(f"  Persona: {parsed['name']} ({parsed['category']})")
            print(f"  Chunks: {len(chunks)}")

            results = upload_persona(
                supabase, openai_client, parsed, chunks,
                dry_run=args.dry_run
            )

            total_results["personas"] += results["persona"]
            total_results["chunks"] += results["chunks"]
            total_results["errors"] += results["errors"]

        except Exception as e:
            print(f"  Error processing file: {e}")
            total_results["errors"] += 1

    # 결과 출력
    print(f"\n{'='*50}")
    print("Upload complete!")
    print(f"  Personas: {total_results['personas']}")
    print(f"  Chunks:   {total_results['chunks']}")
    print(f"  Errors:   {total_results['errors']}")


if __name__ == "__main__":
    main()
