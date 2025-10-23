"""
Test script for SciSciNet API wrapper
"""

import sys
from sciscinet_api import SciSciNetAPI

def test_api_wrapper():
    print("=" * 60)
    print("Testing SciSciNet API Wrapper")
    print("=" * 60)
    print()

    # Initialize API
    print("1. Initializing API...")
    api = SciSciNetAPI()
    print("   ✓ API initialized successfully")
    print()

    # Test search works
    print("2. Testing paper search (query: 'machine learning')...")
    results = api.search_works("machine learning", per_page=5)

    if 'error' in results:
        print(f"   ✗ Error: {results['error']}")
        return False

    works = results.get('results', [])
    total_count = results.get('meta', {}).get('count', 0)

    if works:
        print(f"   ✓ Found {total_count:,} papers (showing {len(works)})")
        print(f"   First paper: {works[0].get('title', 'Untitled')[:80]}...")
    else:
        print("   ✗ No results found")
        return False
    print()

    # Test get work by ID
    print("3. Testing get work by ID...")
    work_id = works[0].get('id', '').split('/')[-1]
    work = api.get_work_by_id(work_id)

    if 'error' in work:
        print(f"   ✗ Error: {work['error']}")
        return False

    print(f"   ✓ Retrieved work: {work.get('title', 'Untitled')[:60]}...")
    print(f"   Citations: {work.get('cited_by_count', 0)}")
    print()

    # Test search authors
    print("4. Testing author search (query: 'John Smith')...")
    author_results = api.search_authors("John Smith", per_page=3)

    if 'error' in author_results:
        print(f"   ✗ Error: {author_results['error']}")
        return False

    authors = author_results.get('results', [])
    if authors:
        print(f"   ✓ Found {len(authors)} authors")
        print(f"   First author: {authors[0].get('display_name', 'Unknown')}")
    else:
        print("   ✗ No authors found")
        return False
    print()

    # Test search institutions
    print("5. Testing institution search (query: 'MIT')...")
    inst_results = api.search_institutions("MIT", per_page=3)

    if 'error' in inst_results:
        print(f"   ✗ Error: {inst_results['error']}")
        return False

    institutions = inst_results.get('results', [])
    if institutions:
        print(f"   ✓ Found {len(institutions)} institutions")
        print(f"   First: {institutions[0].get('display_name', 'Unknown')}")
    else:
        print("   ✗ No institutions found")
        return False
    print()

    # Test search concepts
    print("6. Testing concept search (query: 'artificial intelligence')...")
    concept_results = api.search_concepts("artificial intelligence", per_page=3)

    if 'error' in concept_results:
        print(f"   ✗ Error: {concept_results['error']}")
        return False

    concepts = concept_results.get('results', [])
    if concepts:
        print(f"   ✓ Found {len(concepts)} concepts")
        print(f"   First: {concepts[0].get('display_name', 'Unknown')}")
    else:
        print("   ✗ No concepts found")
        return False
    print()

    # Test get citations
    print("7. Testing get citations...")
    citations = api.get_citations(work_id, per_page=5)

    if 'error' in citations:
        print(f"   ✗ Error: {citations['error']}")
        return False

    citing_works = citations.get('results', [])
    print(f"   ✓ Found {len(citing_works)} citing papers")
    print()

    # Test get references
    print("8. Testing get references...")
    references = api.get_references(work_id)
    print(f"   ✓ Found {len(references)} referenced works")
    print()

    print("=" * 60)
    print("All API tests passed successfully! ✓")
    print("=" * 60)
    return True


if __name__ == "__main__":
    try:
        success = test_api_wrapper()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
