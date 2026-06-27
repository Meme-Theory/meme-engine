from typing import List, Optional
from datetime import datetime
import requests
import time
import os
from ..paper import Paper
import logging

logger = logging.getLogger(__name__)


class PaperSource:
    """Abstract base class for paper sources"""
    def search(self, query: str, **kwargs) -> List[Paper]:
        raise NotImplementedError

    def download_pdf(self, paper_id: str, save_path: str) -> str:
        raise NotImplementedError

    def read_paper(self, paper_id: str, save_path: str) -> str:
        raise NotImplementedError


class GoogleScholarSearcher(PaperSource):
    """Academic paper search via Semantic Scholar API.

    Replaces the original Google Scholar HTML scraper, which was blocked
    by Google's CAPTCHA/JavaScript wall and always returned empty results.
    Semantic Scholar provides a free, structured JSON API — 5,000 req / 5 min
    without a key, higher with one.

    Set SEMANTIC_SCHOLAR_API_KEY env var for higher rate limits.
    """

    API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
    FIELDS = "paperId,title,authors,abstract,year,citationCount,externalIds,url,publicationDate"
    MAX_RETRIES = 4

    def __init__(self):
        self.session = requests.Session()
        headers = {'Accept': 'application/json'}
        api_key = os.environ.get('SEMANTIC_SCHOLAR_API_KEY', '')
        if api_key:
            headers['x-api-key'] = api_key
        self.session.headers.update(headers)

    def _parse_paper(self, item: dict) -> Optional[Paper]:
        """Parse a single Semantic Scholar result into a Paper object."""
        try:
            paper_id = item.get('paperId', '')
            external = item.get('externalIds') or {}
            arxiv_id = external.get('ArXiv', '')
            doi = external.get('DOI', '')

            authors = []
            for author in (item.get('authors') or []):
                name = author.get('name', '')
                if name:
                    authors.append(name)

            year = item.get('year')
            pub_date_str = item.get('publicationDate')
            pub_date = None
            if pub_date_str:
                try:
                    pub_date = datetime.strptime(pub_date_str, '%Y-%m-%d')
                except ValueError:
                    pass
            if pub_date is None and year:
                pub_date = datetime(year, 1, 1)

            url = item.get('url', '')
            if arxiv_id:
                pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
                if not url:
                    url = f"https://arxiv.org/abs/{arxiv_id}"
            else:
                pdf_url = ''

            display_id = arxiv_id if arxiv_id else (doi if doi else paper_id)

            return Paper(
                paper_id=display_id,
                title=item.get('title', ''),
                authors=authors,
                abstract=item.get('abstract') or '',
                url=url,
                pdf_url=pdf_url,
                published_date=pub_date,
                updated_date=None,
                source='semantic_scholar',
                categories=[],
                keywords=[],
                doi=doi,
                citations=item.get('citationCount', 0),
            )
        except Exception as e:
            logger.warning(f"Failed to parse Semantic Scholar result: {e}")
            return None

    def _request_with_retry(self, params: dict) -> Optional[requests.Response]:
        """Make a request with retry on 429 using Retry-After header."""
        for attempt in range(self.MAX_RETRIES):
            response = self.session.get(self.API_URL, params=params, timeout=15)

            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 10))
                # Exponential backoff: 10s, 20s, 40s, 60s
                wait = min(retry_after * (2 ** attempt), 60)
                logger.warning(f"[Semantic Scholar] 429 rate limited, waiting {wait}s (attempt {attempt+1}/{self.MAX_RETRIES})")
                time.sleep(wait)
                continue

            return response

        logger.error("[Semantic Scholar] Rate limited after all retries.")
        return None

    def search(self, query: str, max_results: int = 10) -> List[Paper]:
        """Search Semantic Scholar API.

        Accepts natural language queries (e.g., "inflation cosmological constant
        vacuum energy mathematical formalism"). Returns papers ranked by relevance.
        """
        papers = []
        offset = 0
        limit = min(max_results, 100)  # API max per request is 100

        while len(papers) < max_results:
            try:
                params = {
                    'query': query,
                    'offset': offset,
                    'limit': limit,
                    'fields': self.FIELDS,
                }
                response = self._request_with_retry(params)

                if response is None:
                    break

                if response.status_code != 200:
                    logger.error(f"[Semantic Scholar] HTTP {response.status_code}: {response.text[:200]}")
                    break

                data = response.json()
                results = data.get('data', [])

                if not results:
                    if not papers:
                        logger.info(f"[Semantic Scholar] No results for query: {query}")
                    break

                for item in results:
                    if len(papers) >= max_results:
                        break
                    paper = self._parse_paper(item)
                    if paper:
                        papers.append(paper)

                total = data.get('total', 0)
                offset += limit
                if offset >= total:
                    break

            except requests.exceptions.ConnectionError as e:
                logger.error(f"[Semantic Scholar] Connection error: {e}")
                break
            except Exception as e:
                logger.error(f"[Semantic Scholar] Search error: {e}")
                break

        return papers[:max_results]

    def download_pdf(self, paper_id: str, save_path: str) -> str:
        """Semantic Scholar does not host PDFs directly.

        If the paper has an arXiv ID, use download_arxiv instead.
        """
        raise NotImplementedError(
            "Semantic Scholar doesn't host PDFs directly. "
            "If the paper has an arXiv ID, use download_arxiv instead."
        )

    def read_paper(self, paper_id: str, save_path: str = "./downloads") -> str:
        """Semantic Scholar does not support direct paper reading."""
        return (
            "Semantic Scholar doesn't support direct paper reading. "
            "Use the arXiv ID from search results with read_arxiv_paper instead."
        )


if __name__ == "__main__":
    searcher = GoogleScholarSearcher()

    print("Testing Semantic Scholar search...")
    query = "inflation cosmological constant vacuum energy"
    max_results = 5

    try:
        papers = searcher.search(query, max_results=max_results)
        print(f"\nFound {len(papers)} papers for query '{query}':")
        for i, paper in enumerate(papers, 1):
            print(f"\n{i}. {paper.title}")
            print(f"   Authors: {', '.join(paper.authors[:3])}{'...' if len(paper.authors) > 3 else ''}")
            print(f"   Year: {paper.published_date.year if paper.published_date else 'N/A'}")
            print(f"   Citations: {paper.citations}")
            print(f"   ID: {paper.paper_id}")
            print(f"   URL: {paper.url}")
    except Exception as e:
        print(f"Error during search: {e}")
