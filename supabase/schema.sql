-- Persona MCP - Supabase Schema
-- pgvector extension for semantic search

-- Enable pgvector extension
create extension if not exists vector;

-- Persona definitions table
create table if not exists personas (
    id text primary key,                    -- 예: "410-llm-engineer"
    name text not null,                     -- 예: "LLM Engineer"
    name_kr text,                           -- 한글명
    category text not null,                 -- 예: "ai_data"
    category_kr text,                       -- 카테고리 한글명
    description text,                       -- 간단한 설명
    expertise jsonb default '[]'::jsonb,    -- 전문 분야 목록
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

-- Persona knowledge chunks table
create table if not exists persona_knowledge (
    id text primary key,                    -- 예: "410-llm-engineer-001"
    persona_id text not null references personas(id),
    content text not null,                  -- 청크 내용
    section text,                           -- 섹션 (예: "Core Expertise", "Best Practices")
    keywords jsonb default '[]'::jsonb,     -- 검색 키워드

    -- Vector embedding (OpenAI text-embedding-3-small: 1536 dimensions)
    embedding vector(1536),

    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

-- Categories reference table
create table if not exists persona_categories (
    id text primary key,
    name_kr text not null,
    description text,
    persona_count integer default 0
);

-- Insert categories
insert into persona_categories (id, name_kr, description) values
    ('engineering', '엔지니어링', '소프트웨어 개발 및 인프라'),
    ('design_creative', '디자인/크리에이티브', 'UX/UI, 그래픽, 애니메이션'),
    ('business_leadership', '비즈니스/리더십', '경영, 전략, 마케팅'),
    ('ai_data', 'AI/데이터', '머신러닝, 데이터 사이언스'),
    ('testing_qa', 'QA/테스팅', '품질 보증, 자동화 테스트'),
    ('education', '교육', '교수, 교사, 교육과정'),
    ('healthcare', '의료', '의사, 간호사, 약사'),
    ('other', '기타', '기타 전문가')
on conflict (id) do nothing;

-- Create indexes for fast search
create index if not exists idx_persona_knowledge_persona on persona_knowledge(persona_id);
create index if not exists idx_persona_knowledge_section on persona_knowledge(section);
create index if not exists idx_persona_knowledge_keywords on persona_knowledge using gin(keywords);

-- Vector similarity search index
create index if not exists idx_persona_knowledge_embedding on persona_knowledge
using ivfflat (embedding vector_cosine_ops) with (lists = 20);

-- Function: Semantic search across all personas
create or replace function search_persona_knowledge(
    query_embedding vector(1536),
    match_threshold float default 0.6,
    match_count int default 5,
    filter_persona text default null,
    filter_category text default null
)
returns table (
    id text,
    persona_id text,
    persona_name text,
    category text,
    content text,
    section text,
    similarity float
)
language plpgsql
as $$
begin
    return query
    select
        pk.id,
        pk.persona_id,
        p.name as persona_name,
        p.category,
        pk.content,
        pk.section,
        1 - (pk.embedding <=> query_embedding) as similarity
    from persona_knowledge pk
    join personas p on pk.persona_id = p.id
    where
        1 - (pk.embedding <=> query_embedding) > match_threshold
        and (filter_persona is null or pk.persona_id = filter_persona)
        and (filter_category is null or p.category = filter_category)
    order by pk.embedding <=> query_embedding
    limit match_count;
end;
$$;

-- Function: Search within specific persona
create or replace function search_by_persona(
    query_embedding vector(1536),
    target_persona text,
    match_count int default 5
)
returns table (
    id text,
    content text,
    section text,
    similarity float
)
language plpgsql
as $$
begin
    return query
    select
        pk.id,
        pk.content,
        pk.section,
        1 - (pk.embedding <=> query_embedding) as similarity
    from persona_knowledge pk
    where pk.persona_id = target_persona
    order by pk.embedding <=> query_embedding
    limit match_count;
end;
$$;

-- Function: Get all personas
create or replace function get_all_personas()
returns table (
    id text,
    name text,
    category text,
    description text,
    chunk_count bigint
)
language sql
as $$
    select
        p.id,
        p.name,
        p.category,
        p.description,
        count(pk.id) as chunk_count
    from personas p
    left join persona_knowledge pk on p.id = pk.persona_id
    group by p.id, p.name, p.category, p.description
    order by p.id;
$$;

-- Function: Get persona stats
create or replace function get_persona_stats()
returns table (
    total_personas bigint,
    total_chunks bigint,
    categories_count bigint
)
language sql
as $$
    select
        (select count(*) from personas) as total_personas,
        (select count(*) from persona_knowledge) as total_chunks,
        (select count(distinct category) from personas) as categories_count;
$$;

-- Update timestamp trigger
create or replace function update_updated_at()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

create trigger personas_updated_at
    before update on personas
    for each row
    execute function update_updated_at();

create trigger persona_knowledge_updated_at
    before update on persona_knowledge
    for each row
    execute function update_updated_at();

-- Row Level Security (optional)
-- alter table personas enable row level security;
-- alter table persona_knowledge enable row level security;
-- create policy "Public read access" on personas for select using (true);
-- create policy "Public read access" on persona_knowledge for select using (true);
