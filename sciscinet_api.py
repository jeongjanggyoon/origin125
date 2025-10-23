"""
SciSciNet API Wrapper
A simple Python wrapper for accessing OpenAlex/SciSciNet data
"""

import requests
from typing import Dict, List, Optional
import time


class SciSciNetAPI:
    """Wrapper class for OpenAlex API to access SciSciNet data"""

    def __init__(self, email: Optional[str] = None):
        """
        Initialize the API wrapper

        Args:
            email: Optional email for polite pool (faster API access)
        """
        self.base_url = "https://api.openalex.org"
        self.email = email
        self.session = requests.Session()

        # Set required User-Agent header
        self.session.headers.update({
            'User-Agent': 'SciSciNet-Explorer/1.0 (https://github.com/sciscinet-explorer; mailto:research@example.com)'
        })

        # Set up polite pool if email provided
        if email:
            self.session.params = {'mailto': email}
            self.session.headers.update({
                'User-Agent': f'SciSciNet-Explorer/1.0 (https://github.com/sciscinet-explorer; mailto:{email})'
            })

    def search_works(self, query: str, page: int = 1, per_page: int = 25,
                     filters: Optional[Dict] = None) -> Dict:
        """
        Search for scientific works/papers

        Args:
            query: Search query string
            page: Page number for pagination
            per_page: Results per page (max 200)
            filters: Optional filters (e.g., publication_year, type)

        Returns:
            Dictionary containing search results
        """
        url = f"{self.base_url}/works"
        params = {
            'search': query,
            'page': page,
            'per_page': min(per_page, 200)
        }

        # Add filters if provided
        if filters:
            for key, value in filters.items():
                params[f'filter'] = f"{key}:{value}"

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "results": []}

    def get_work_by_id(self, work_id: str) -> Dict:
        """
        Get detailed information about a specific work

        Args:
            work_id: OpenAlex work ID (e.g., 'W2741809807' or full URL)

        Returns:
            Dictionary containing work details
        """
        # Clean the ID if it's a full URL
        if work_id.startswith('http'):
            work_id = work_id.split('/')[-1]

        url = f"{self.base_url}/works/{work_id}"

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def search_authors(self, query: str, page: int = 1, per_page: int = 25) -> Dict:
        """
        Search for authors

        Args:
            query: Author name or search query
            page: Page number for pagination
            per_page: Results per page (max 200)

        Returns:
            Dictionary containing author search results
        """
        url = f"{self.base_url}/authors"
        params = {
            'search': query,
            'page': page,
            'per_page': min(per_page, 200)
        }

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "results": []}

    def get_author_by_id(self, author_id: str) -> Dict:
        """
        Get detailed information about a specific author

        Args:
            author_id: OpenAlex author ID

        Returns:
            Dictionary containing author details
        """
        if author_id.startswith('http'):
            author_id = author_id.split('/')[-1]

        url = f"{self.base_url}/authors/{author_id}"

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def search_institutions(self, query: str, page: int = 1, per_page: int = 25) -> Dict:
        """
        Search for institutions

        Args:
            query: Institution name or search query
            page: Page number for pagination
            per_page: Results per page (max 200)

        Returns:
            Dictionary containing institution search results
        """
        url = f"{self.base_url}/institutions"
        params = {
            'search': query,
            'page': page,
            'per_page': min(per_page, 200)
        }

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "results": []}

    def search_concepts(self, query: str, page: int = 1, per_page: int = 25) -> Dict:
        """
        Search for concepts/topics

        Args:
            query: Concept/topic search query
            page: Page number for pagination
            per_page: Results per page (max 200)

        Returns:
            Dictionary containing concept search results
        """
        url = f"{self.base_url}/concepts"
        params = {
            'search': query,
            'page': page,
            'per_page': min(per_page, 200)
        }

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "results": []}

    def get_citations(self, work_id: str, page: int = 1, per_page: int = 25) -> Dict:
        """
        Get works that cite a specific work

        Args:
            work_id: OpenAlex work ID
            page: Page number for pagination
            per_page: Results per page (max 200)

        Returns:
            Dictionary containing citing works
        """
        if work_id.startswith('http'):
            work_id = work_id.split('/')[-1]

        url = f"{self.base_url}/works"
        params = {
            'filter': f'cites:{work_id}',
            'page': page,
            'per_page': min(per_page, 200)
        }

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "results": []}

    def get_references(self, work_id: str) -> List[str]:
        """
        Get works referenced by a specific work

        Args:
            work_id: OpenAlex work ID

        Returns:
            List of referenced work IDs
        """
        work = self.get_work_by_id(work_id)

        if 'error' in work:
            return []

        return work.get('referenced_works', [])
