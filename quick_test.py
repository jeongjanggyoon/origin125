#!/usr/bin/env python3
"""빠른 테스트 스크립트"""

from html_saver import HTMLSaver

print("HTML Saver 빠른 테스트")
print("=" * 50)

# 1. 기본 사용법
print("\n1. HTMLSaver 초기화")
saver = HTMLSaver(output_dir="test_html")
print(f"   ✓ 출력 디렉토리: {saver.output_dir}")

# 2. 파일명 자동 생성 테스트
print("\n2. 파일명 자동 생성")
urls = [
    "https://example.com",
    "https://github.com/user/repo",
    "https://docs.python.org/3/tutorial/index.html",
]
for url in urls:
    filename = saver.generate_filename(url)
    print(f"   {url}")
    print(f"   → {filename}")

# 3. 커스텀 파일명
print("\n3. 커스텀 파일명")
custom = saver.generate_filename("https://example.com", "my_page")
print(f"   커스텀: {custom}")

print("\n" + "=" * 50)
print("테스트 완료!")
