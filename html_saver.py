"""
HTML Saver Module
A utility to fetch and save HTML content from URLs
"""

import requests
from typing import Optional, Dict
from pathlib import Path
from datetime import datetime
import re
from urllib.parse import urlparse, quote


class HTMLSaver:
    """Class for fetching and saving HTML content from URLs"""

    def __init__(self, output_dir: str = "saved_html", timeout: int = 30):
        """
        Initialize the HTML Saver

        Args:
            output_dir: Directory to save HTML files (default: 'saved_html')
            timeout: Request timeout in seconds (default: 30)
        """
        self.output_dir = Path(output_dir)
        self.timeout = timeout
        self.session = requests.Session()

        # Set a proper User-Agent to avoid blocking
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def fetch_html(self, url: str) -> Dict:
        """
        Fetch HTML content from a URL

        Args:
            url: URL to fetch HTML from

        Returns:
            Dictionary containing 'success', 'content', 'url', 'status_code', and optional 'error'
        """
        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            response.raise_for_status()

            # Get the encoding from the response or detect it
            response.encoding = response.apparent_encoding

            return {
                'success': True,
                'content': response.text,
                'url': response.url,  # Final URL after redirects
                'status_code': response.status_code,
                'headers': dict(response.headers)
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'url': url,
                'status_code': None
            }

    def generate_filename(self, url: str, custom_name: Optional[str] = None) -> str:
        """
        Generate a filename for saving HTML

        Args:
            url: Source URL
            custom_name: Optional custom filename

        Returns:
            Generated filename
        """
        if custom_name:
            # Sanitize custom name
            filename = re.sub(r'[^\w\-_.]', '_', custom_name)
            if not filename.endswith('.html'):
                filename += '.html'
            return filename

        # Parse URL to extract domain and path
        parsed = urlparse(url)
        domain = parsed.netloc.replace('www.', '')
        path = parsed.path.strip('/')

        # Create filename from domain and path
        if path:
            # Take last part of path as base name
            base = path.split('/')[-1]
            if '.' in base:
                base = base.rsplit('.', 1)[0]
            filename = f"{domain}_{base}"
        else:
            filename = domain

        # Sanitize filename
        filename = re.sub(r'[^\w\-_.]', '_', filename)

        # Add timestamp to avoid collisions
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{filename}_{timestamp}.html"

        return filename

    def save_html(self, url: str, filename: Optional[str] = None,
                  overwrite: bool = False) -> Dict:
        """
        Fetch and save HTML from a URL

        Args:
            url: URL to fetch HTML from
            filename: Optional custom filename
            overwrite: Whether to overwrite existing files (default: False)

        Returns:
            Dictionary containing 'success', 'filepath', 'url', and optional 'error'
        """
        # Fetch HTML content
        result = self.fetch_html(url)

        if not result['success']:
            return {
                'success': False,
                'error': result['error'],
                'url': url
            }

        # Generate filename
        filename = self.generate_filename(result['url'], filename)
        filepath = self.output_dir / filename

        # Check if file exists
        if filepath.exists() and not overwrite:
            return {
                'success': False,
                'error': f'File already exists: {filepath}',
                'filepath': str(filepath),
                'url': url
            }

        # Save HTML to file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(result['content'])

            return {
                'success': True,
                'filepath': str(filepath),
                'url': result['url'],
                'status_code': result['status_code'],
                'size_bytes': len(result['content'].encode('utf-8'))
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to save file: {str(e)}',
                'filepath': str(filepath),
                'url': url
            }

    def save_multiple(self, urls: list, overwrite: bool = False) -> list:
        """
        Save HTML from multiple URLs

        Args:
            urls: List of URLs to fetch and save
            overwrite: Whether to overwrite existing files

        Returns:
            List of result dictionaries for each URL
        """
        results = []
        for url in urls:
            result = self.save_html(url, overwrite=overwrite)
            results.append(result)

        return results


def main():
    """CLI interface for HTML Saver"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Save HTML content from URLs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Save single URL
  python html_saver.py https://example.com

  # Save with custom filename
  python html_saver.py https://example.com -f my_page.html

  # Save to custom directory
  python html_saver.py https://example.com -o my_html_folder

  # Save multiple URLs
  python html_saver.py https://example.com https://google.com

  # Overwrite existing files
  python html_saver.py https://example.com --overwrite
        """
    )

    parser.add_argument('urls', nargs='+', help='URL(s) to save')
    parser.add_argument('-o', '--output-dir', default='saved_html',
                        help='Output directory (default: saved_html)')
    parser.add_argument('-f', '--filename', help='Custom filename (only for single URL)')
    parser.add_argument('--overwrite', action='store_true',
                        help='Overwrite existing files')
    parser.add_argument('--timeout', type=int, default=30,
                        help='Request timeout in seconds (default: 30)')

    args = parser.parse_args()

    # Validate filename argument
    if args.filename and len(args.urls) > 1:
        print("Error: --filename can only be used with a single URL")
        return 1

    # Initialize saver
    saver = HTMLSaver(output_dir=args.output_dir, timeout=args.timeout)

    print(f"Saving HTML to: {saver.output_dir.absolute()}\n")

    # Save HTML from URLs
    if len(args.urls) == 1:
        result = saver.save_html(args.urls[0], filename=args.filename,
                                 overwrite=args.overwrite)

        if result['success']:
            print(f"✓ Success!")
            print(f"  URL: {result['url']}")
            print(f"  File: {result['filepath']}")
            print(f"  Size: {result['size_bytes']:,} bytes")
            print(f"  Status: {result['status_code']}")
        else:
            print(f"✗ Failed!")
            print(f"  URL: {result['url']}")
            print(f"  Error: {result['error']}")
            return 1
    else:
        results = saver.save_multiple(args.urls, overwrite=args.overwrite)

        success_count = sum(1 for r in results if r['success'])
        print(f"Processed {len(results)} URLs:")
        print(f"  Success: {success_count}")
        print(f"  Failed: {len(results) - success_count}\n")

        for i, result in enumerate(results, 1):
            if result['success']:
                print(f"{i}. ✓ {result['url']}")
                print(f"   → {result['filepath']}")
            else:
                print(f"{i}. ✗ {result['url']}")
                print(f"   → Error: {result['error']}")

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
