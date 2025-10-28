"""
실제 동작 데모 - HTML Saver
"""

from html_saver import HTMLSaver
from unittest.mock import Mock, patch

def demo_with_mock():
    """Mock을 사용한 실제 동작 데모"""
    print("=" * 70)
    print("HTML Saver 실행 데모")
    print("=" * 70)
    print()

    # HTMLSaver 인스턴스 생성
    saver = HTMLSaver(output_dir="demo_output")
    print(f"✓ HTMLSaver 초기화 완료")
    print(f"  출력 디렉토리: {saver.output_dir.absolute()}")
    print()

    # Mock HTML 응답 생성
    with patch('html_saver.requests.Session.get') as mock_get:
        # 가짜 HTML 페이지 생성
        mock_response = Mock()
        mock_response.text = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>테스트 페이지</title>
</head>
<body>
    <h1>안녕하세요!</h1>
    <p>이것은 HTML Saver로 저장된 테스트 페이지입니다.</p>
    <ul>
        <li>항목 1</li>
        <li>항목 2</li>
        <li>항목 3</li>
    </ul>
</body>
</html>
        """
        mock_response.url = "https://example.com/test-page"
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "text/html; charset=utf-8"}
        mock_response.apparent_encoding = "utf-8"
        mock_get.return_value = mock_response

        print("-" * 70)
        print("테스트 1: 단일 URL 저장")
        print("-" * 70)

        result = saver.save_html(
            "https://example.com/test-page",
            filename="my_test_page.html"
        )

        if result['success']:
            print(f"✓ 저장 성공!")
            print(f"  URL: {result['url']}")
            print(f"  파일 경로: {result['filepath']}")
            print(f"  파일 크기: {result['size_bytes']:,} bytes")
            print(f"  HTTP 상태: {result['status_code']}")

            # 저장된 파일 내용 확인
            with open(result['filepath'], 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"\n  파일 내용 (처음 200자):")
                print(f"  {content[:200]}...")
        else:
            print(f"✗ 저장 실패: {result['error']}")

        print()

        # 여러 URL 저장 테스트
        print("-" * 70)
        print("테스트 2: 여러 URL 동시 저장")
        print("-" * 70)

        def mock_get_multiple(*args, **kwargs):
            """각 URL마다 다른 응답 생성"""
            url = args[0]
            response = Mock()
            response.url = url
            response.status_code = 200
            response.headers = {"Content-Type": "text/html"}
            response.apparent_encoding = "utf-8"

            # URL에 따라 다른 HTML 생성
            if "page1" in url:
                response.text = "<html><body><h1>페이지 1</h1></body></html>"
            elif "page2" in url:
                response.text = "<html><body><h1>페이지 2</h1></body></html>"
            else:
                response.text = "<html><body><h1>페이지 3</h1></body></html>"

            return response

        mock_get.side_effect = mock_get_multiple

        urls = [
            "https://example.com/page1",
            "https://example.com/page2",
            "https://example.com/page3"
        ]

        results = saver.save_multiple(urls, overwrite=True)

        success_count = sum(1 for r in results if r['success'])
        print(f"✓ 처리 완료: {len(results)}개 URL")
        print(f"  성공: {success_count}개")
        print(f"  실패: {len(results) - success_count}개")
        print()

        for i, result in enumerate(results, 1):
            if result['success']:
                print(f"  {i}. ✓ {result['url']}")
                print(f"     → {result['filepath']}")
            else:
                print(f"  {i}. ✗ {result['url']}")
                print(f"     → {result['error']}")

        print()

        # HTML 가져오기만 하기 (저장 안함)
        print("-" * 70)
        print("테스트 3: HTML 가져오기만 (저장 안함)")
        print("-" * 70)

        mock_response2 = Mock()
        mock_response2.text = "<html><body><h1>Fetch only test</h1></body></html>"
        mock_response2.url = "https://example.com/fetch-only"
        mock_response2.status_code = 200
        mock_response2.headers = {"Content-Type": "text/html"}
        mock_response2.apparent_encoding = "utf-8"
        mock_get.side_effect = None
        mock_get.return_value = mock_response2

        result = saver.fetch_html("https://example.com/fetch-only")

        if result['success']:
            print(f"✓ HTML 가져오기 성공!")
            print(f"  URL: {result['url']}")
            print(f"  상태 코드: {result['status_code']}")
            print(f"  컨텐츠 길이: {len(result['content'])} 문자")
            print(f"  컨텐츠 미리보기: {result['content'][:100]}...")
        else:
            print(f"✗ 실패: {result['error']}")

    print()
    print("=" * 70)
    print("데모 완료!")
    print("=" * 70)
    print()

    # 저장된 파일 목록 확인
    print("저장된 파일 목록:")
    import os
    if os.path.exists("demo_output"):
        files = os.listdir("demo_output")
        for f in files:
            file_path = os.path.join("demo_output", f)
            size = os.path.getsize(file_path)
            print(f"  - {f} ({size:,} bytes)")
    else:
        print("  (파일 없음)")


def demo_filename_generation():
    """파일명 생성 테스트"""
    print()
    print("=" * 70)
    print("파일명 자동 생성 테스트")
    print("=" * 70)
    print()

    saver = HTMLSaver()

    test_urls = [
        "https://example.com",
        "https://example.com/about",
        "https://github.com/user/repo",
        "https://docs.python.org/3/library/os.html",
    ]

    for url in test_urls:
        filename = saver.generate_filename(url)
        print(f"URL: {url}")
        print(f"  → {filename}")
        print()


if __name__ == "__main__":
    demo_with_mock()
    demo_filename_generation()
