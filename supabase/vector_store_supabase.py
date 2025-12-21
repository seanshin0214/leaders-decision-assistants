"""
Persona MCP - Supabase Vector Store
Supabase + pgvector 기반 벡터 스토어

로컬 ChromaDB 대신 Supabase를 사용하여:
- 모든 사용자가 동일한 지식 베이스 접근
- 142개 페르소나 지식 원격 검색
- 하이브리드 검색 (벡터 + 메타데이터)

환경변수:
    SUPABASE_URL: Supabase 프로젝트 URL
    SUPABASE_KEY: Supabase anon/service key
    OPENAI_API_KEY: OpenAI API key (임베딩용)
"""

import os
import sys
from typing import List, Dict, Any, Optional


class PersonaVectorStoreSupabase:
    """Supabase 기반 페르소나 벡터 스토어"""

    def __init__(
        self,
        supabase_url: Optional[str] = None,
        supabase_key: Optional[str] = None,
        openai_key: Optional[str] = None
    ):
        self.supabase_url = supabase_url or os.environ.get('SUPABASE_URL')
        self.supabase_key = supabase_key or os.environ.get('SUPABASE_KEY')
        self.openai_key = openai_key or os.environ.get('OPENAI_API_KEY')

        self._supabase = None
        self._openai = None
        self._initialized = False

        # 필요한 키가 모두 있는지 확인
        self.available = bool(
            self.supabase_url and
            self.supabase_key and
            self.openai_key
        )

    def _ensure_initialized(self):
        """Lazy initialization"""
        if self._initialized:
            return

        if not self.available:
            return

        try:
            from supabase import create_client
            from openai import OpenAI

            self._supabase = create_client(self.supabase_url, self.supabase_key)
            self._openai = OpenAI(api_key=self.openai_key)
            self._initialized = True
            print("Supabase Persona Vector Store initialized", file=sys.stderr)
        except Exception as e:
            print(f"Supabase init error: {e}", file=sys.stderr)
            self.available = False

    def _generate_embedding(self, text: str) -> List[float]:
        """텍스트 임베딩 생성"""
        response = self._openai.embeddings.create(
            model="text-embedding-3-small",
            input=text[:8000]
        )
        return response.data[0].embedding

    def search(
        self,
        query: str,
        n_results: int = 5,
        filter_metadata: Optional[dict] = None
    ) -> List[Dict[str, Any]]:
        """
        전체 페르소나 지식에서 시맨틱 검색

        Args:
            query: 검색 쿼리
            n_results: 결과 수
            filter_metadata: 필터 (예: {"persona_id": "410-llm-engineer"})

        Returns:
            검색 결과 리스트
        """
        self._ensure_initialized()

        if not self.available or not self._supabase:
            return []

        try:
            query_embedding = self._generate_embedding(query)

            filter_persona = None
            filter_category = None
            if filter_metadata:
                filter_persona = filter_metadata.get("persona_id")
                filter_category = filter_metadata.get("category")

            result = self._supabase.rpc(
                'search_persona_knowledge',
                {
                    'query_embedding': query_embedding,
                    'match_threshold': 0.5,
                    'match_count': n_results,
                    'filter_persona': filter_persona,
                    'filter_category': filter_category
                }
            ).execute()

            # 로컬 ChromaDB 포맷으로 변환
            output = []
            for row in result.data:
                output.append({
                    "id": row["id"],
                    "content": row["content"],
                    "metadata": {
                        "persona_id": row["persona_id"],
                        "persona_name": row["persona_name"],
                        "section": row.get("section", "")
                    },
                    "distance": 1 - row["similarity"]  # similarity를 distance로 변환
                })

            return output

        except Exception as e:
            print(f"Search error: {e}", file=sys.stderr)
            return []

    def search_by_persona(
        self,
        query: str,
        persona_id: str,
        n_results: int = 5
    ) -> List[Dict[str, Any]]:
        """특정 페르소나 지식에서 검색"""
        self._ensure_initialized()

        if not self.available or not self._supabase:
            return []

        try:
            query_embedding = self._generate_embedding(query)

            result = self._supabase.rpc(
                'search_by_persona',
                {
                    'query_embedding': query_embedding,
                    'target_persona': persona_id,
                    'match_count': n_results
                }
            ).execute()

            # 포맷 변환
            output = []
            for row in result.data:
                output.append({
                    "id": row["id"],
                    "content": row["content"],
                    "metadata": {
                        "persona_id": persona_id,
                        "section": row.get("section", "")
                    },
                    "distance": 1 - row["similarity"]
                })

            return output

        except Exception as e:
            print(f"Search by persona error: {e}", file=sys.stderr)
            return []

    def get_all_personas(self) -> List[str]:
        """모든 페르소나 ID 목록"""
        self._ensure_initialized()

        if not self.available or not self._supabase:
            return []

        try:
            result = self._supabase.rpc('get_all_personas').execute()
            return [row["id"] for row in result.data]
        except Exception as e:
            print(f"Get personas error: {e}", file=sys.stderr)
            return []

    def get_document_count(self) -> int:
        """총 청크 수"""
        self._ensure_initialized()

        if not self.available or not self._supabase:
            return 0

        try:
            result = self._supabase.rpc('get_persona_stats').execute()
            if result.data:
                return result.data[0].get("total_chunks", 0)
            return 0
        except:
            return 0

    # 하위 호환 메서드
    @property
    def encoder(self):
        """SentenceTransformer 호환 (사용 안함)"""
        return None


class HybridPersonaVectorStore:
    """
    하이브리드 벡터 스토어
    - Supabase 사용 가능하면 원격 검색
    - 아니면 로컬 ChromaDB 사용
    """

    def __init__(self, persist_directory: str = "./data/chroma_db"):
        self.supabase_store = PersonaVectorStoreSupabase()
        self._local_store = None
        self.persist_directory = persist_directory

    @property
    def _use_supabase(self) -> bool:
        return self.supabase_store.available

    @property
    def local_store(self):
        """
        로컬 ChromaDB 스토어 (lazy load)
        NOTE: 사용자가 별도로 설정할 필요 없음 - 자동으로 rag/vector_store.py를 찾아서 임포트
        """
        if self._local_store is None:
            import sys
            from pathlib import Path
            # [자동] ../rag/vector_store.py 모듈 경로 설정
            rag_path = Path(__file__).parent.parent / "rag"
            if str(rag_path) not in sys.path:
                sys.path.insert(0, str(rag_path))
            from vector_store import PersonaVectorStore
            self._local_store = PersonaVectorStore(self.persist_directory)
        return self._local_store

    @property
    def encoder(self):
        """SentenceTransformer 인코더 (로컬 모드용)"""
        if self._use_supabase:
            return None
        return self.local_store.encoder

    def search(self, query: str, n_results: int = 5,
               filter_metadata: Optional[dict] = None) -> List[Dict[str, Any]]:
        """검색 - Supabase 우선"""
        if self._use_supabase:
            results = self.supabase_store.search(query, n_results, filter_metadata)
            if results:
                return results

        return self.local_store.search(query, n_results, filter_metadata)

    def search_by_persona(self, query: str, persona_id: str,
                          n_results: int = 5) -> List[Dict[str, Any]]:
        """특정 페르소나 검색"""
        if self._use_supabase:
            results = self.supabase_store.search_by_persona(query, persona_id, n_results)
            if results:
                return results

        return self.local_store.search_by_persona(query, persona_id, n_results)

    def get_all_personas(self) -> List[str]:
        """모든 페르소나 목록"""
        if self._use_supabase:
            personas = self.supabase_store.get_all_personas()
            if personas:
                return personas

        return self.local_store.get_all_personas()

    def get_document_count(self) -> int:
        """문서 수"""
        if self._use_supabase:
            return self.supabase_store.get_document_count()
        return self.local_store.get_document_count()


# 글로벌 인스턴스
def get_hybrid_vector_store(persist_directory: str = "./data/chroma_db"):
    """하이브리드 벡터 스토어 인스턴스 반환"""
    return HybridPersonaVectorStore(persist_directory)


if __name__ == "__main__":
    # 테스트
    store = PersonaVectorStoreSupabase()
    print(f"Available: {store.available}")

    if store.available:
        personas = store.get_all_personas()
        print(f"Personas: {len(personas)}")

        results = store.search("Python backend development", n_results=3)
        for r in results:
            print(f"- {r['metadata']['persona_name']}: {r['content'][:100]}...")
