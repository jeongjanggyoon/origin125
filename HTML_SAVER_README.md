# HTML Saver

URL을 입력받아 HTML 컨텐츠를 파일로 저장하는 유틸리티입니다.

## 기능

- URL에서 HTML 컨텐츠 다운로드
- 자동 파일명 생성 (URL 기반 + 타임스탬프)
- 커스텀 파일명 지정 가능
- 여러 URL 일괄 처리
- 커스텀 출력 디렉토리 설정
- 에러 핸들링 및 상세한 결과 정보

## 설치

필요한 패키지:
```bash
pip install requests
```

## 사용 방법

### 1. CLI (커맨드 라인) 사용

#### 기본 사용법
```bash
python html_saver.py https://example.com
```

#### 커스텀 파일명 지정
```bash
python html_saver.py https://example.com -f my_page.html
```

#### 커스텀 출력 디렉토리
```bash
python html_saver.py https://example.com -o my_html_folder
```

#### 여러 URL 한번에 저장
```bash
python html_saver.py https://example.com https://google.com https://github.com
```

#### 기존 파일 덮어쓰기
```bash
python html_saver.py https://example.com --overwrite
```

#### 타임아웃 설정
```bash
python html_saver.py https://example.com --timeout 60
```

### 2. Python 코드에서 사용

#### 기본 사용 예제
```python
from html_saver import HTMLSaver

# HTMLSaver 인스턴스 생성
saver = HTMLSaver(output_dir="saved_html")

# URL에서 HTML 저장
result = saver.save_html("https://example.com")

if result['success']:
    print(f"저장 완료: {result['filepath']}")
    print(f"파일 크기: {result['size_bytes']} bytes")
else:
    print(f"오류: {result['error']}")
```

#### 커스텀 파일명 사용
```python
saver = HTMLSaver()
result = saver.save_html(
    "https://example.com",
    filename="my_page.html",
    overwrite=True
)
```

#### 여러 URL 저장
```python
saver = HTMLSaver()
urls = [
    "https://example.com",
    "https://google.com",
    "https://github.com"
]

results = saver.save_multiple(urls)

for result in results:
    if result['success']:
        print(f"✓ {result['url']} → {result['filepath']}")
    else:
        print(f"✗ {result['url']}: {result['error']}")
```

#### HTML 가져오기만 하기 (저장 안함)
```python
saver = HTMLSaver()
result = saver.fetch_html("https://example.com")

if result['success']:
    html_content = result['content']
    print(f"HTML 길이: {len(html_content)} characters")
```

### 3. 예제 실행

전체 예제를 확인하려면:
```bash
python example_html_saver.py
```

## API 문서

### HTMLSaver 클래스

#### `__init__(output_dir="saved_html", timeout=30)`
- `output_dir`: HTML 파일을 저장할 디렉토리 (기본값: "saved_html")
- `timeout`: 요청 타임아웃 (초 단위, 기본값: 30)

#### `save_html(url, filename=None, overwrite=False)`
URL에서 HTML을 가져와 파일로 저장합니다.

**Parameters:**
- `url` (str): 저장할 URL
- `filename` (str, optional): 커스텀 파일명
- `overwrite` (bool): 기존 파일 덮어쓰기 여부 (기본값: False)

**Returns:** Dictionary
```python
{
    'success': True,          # 성공 여부
    'filepath': 'path/to/file.html',  # 저장된 파일 경로
    'url': 'https://...',     # 최종 URL (리다이렉트 포함)
    'status_code': 200,       # HTTP 상태 코드
    'size_bytes': 12345       # 파일 크기 (bytes)
}
```

#### `fetch_html(url)`
URL에서 HTML을 가져오기만 합니다 (저장하지 않음).

**Parameters:**
- `url` (str): 가져올 URL

**Returns:** Dictionary
```python
{
    'success': True,
    'content': '<html>...</html>',  # HTML 컨텐츠
    'url': 'https://...',
    'status_code': 200,
    'headers': {...}
}
```

#### `save_multiple(urls, overwrite=False)`
여러 URL의 HTML을 한번에 저장합니다.

**Parameters:**
- `urls` (list): URL 리스트
- `overwrite` (bool): 기존 파일 덮어쓰기 여부

**Returns:** List of dictionaries (각 URL에 대한 결과)

#### `generate_filename(url, custom_name=None)`
URL 기반으로 파일명을 생성합니다.

**Parameters:**
- `url` (str): 소스 URL
- `custom_name` (str, optional): 커스텀 파일명

**Returns:** str (생성된 파일명)

## 파일명 생성 규칙

자동 생성되는 파일명 형식:
```
{domain}_{path}_{timestamp}.html
```

예시:
- `https://example.com` → `example.com_20240315_143022.html`
- `https://github.com/user/repo` → `github.com_repo_20240315_143022.html`

## 에러 처리

모든 메서드는 결과 딕셔너리에 `success` 필드를 포함합니다:
- `success=True`: 성공
- `success=False`: 실패 (에러 메시지는 `error` 필드에 포함)

```python
result = saver.save_html("https://invalid-url")
if not result['success']:
    print(f"Error: {result['error']}")
```

## 주의사항

1. **User-Agent**: 일부 웹사이트는 봇 요청을 차단할 수 있습니다. 이 모듈은 기본적으로 브라우저 User-Agent를 사용합니다.

2. **로봇 규칙**: 웹사이트의 robots.txt와 이용약관을 준수하세요.

3. **속도 제한**: 같은 사이트에서 많은 페이지를 다운로드할 때는 적절한 딜레이를 추가하세요.

4. **저작권**: 다운로드한 컨텐츠의 저작권을 존중하세요.

## 라이선스

이 모듈은 교육 및 연구 목적으로 자유롭게 사용할 수 있습니다.
