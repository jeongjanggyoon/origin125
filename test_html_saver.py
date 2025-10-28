"""
Unit tests for HTML Saver module
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
from html_saver import HTMLSaver


class TestHTMLSaver(unittest.TestCase):
    """Test cases for HTMLSaver class"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary directory for tests
        self.test_dir = tempfile.mkdtemp()
        self.saver = HTMLSaver(output_dir=self.test_dir)

    def tearDown(self):
        """Clean up test fixtures"""
        # Remove the temporary directory
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)

    def test_initialization(self):
        """Test HTMLSaver initialization"""
        self.assertTrue(Path(self.test_dir).exists())
        self.assertEqual(self.saver.timeout, 30)

    def test_generate_filename_with_custom_name(self):
        """Test filename generation with custom name"""
        filename = self.saver.generate_filename(
            "https://example.com",
            custom_name="my_page"
        )
        self.assertEqual(filename, "my_page.html")

    def test_generate_filename_with_custom_name_with_extension(self):
        """Test filename generation with custom name that has .html"""
        filename = self.saver.generate_filename(
            "https://example.com",
            custom_name="my_page.html"
        )
        self.assertEqual(filename, "my_page.html")

    def test_generate_filename_auto(self):
        """Test automatic filename generation"""
        filename = self.saver.generate_filename("https://example.com/page")
        self.assertIn("example.com", filename)
        self.assertIn("page", filename)
        self.assertTrue(filename.endswith(".html"))

    def test_generate_filename_sanitization(self):
        """Test that filenames are properly sanitized"""
        filename = self.saver.generate_filename(
            "https://example.com/page/with/special?chars=test",
            custom_name="test<>:file"
        )
        # Should not contain special characters
        self.assertNotIn("<", filename)
        self.assertNotIn(">", filename)
        self.assertNotIn(":", filename)
        self.assertTrue(filename.endswith(".html"))

    @patch('html_saver.requests.Session.get')
    def test_fetch_html_success(self, mock_get):
        """Test successful HTML fetching"""
        # Mock response
        mock_response = Mock()
        mock_response.text = "<html><body>Test</body></html>"
        mock_response.url = "https://example.com"
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "text/html"}
        mock_response.apparent_encoding = "utf-8"
        mock_get.return_value = mock_response

        result = self.saver.fetch_html("https://example.com")

        self.assertTrue(result['success'])
        self.assertEqual(result['content'], "<html><body>Test</body></html>")
        self.assertEqual(result['status_code'], 200)
        self.assertEqual(result['url'], "https://example.com")

    @patch('html_saver.requests.Session.get')
    def test_fetch_html_failure(self, mock_get):
        """Test HTML fetching failure"""
        # Mock exception
        mock_get.side_effect = Exception("Network error")

        result = self.saver.fetch_html("https://example.com")

        self.assertFalse(result['success'])
        self.assertIn('error', result)

    @patch('html_saver.requests.Session.get')
    def test_save_html_success(self, mock_get):
        """Test successful HTML saving"""
        # Mock response
        mock_response = Mock()
        mock_response.text = "<html><body>Test Content</body></html>"
        mock_response.url = "https://example.com"
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "text/html"}
        mock_response.apparent_encoding = "utf-8"
        mock_get.return_value = mock_response

        result = self.saver.save_html(
            "https://example.com",
            filename="test.html"
        )

        self.assertTrue(result['success'])
        self.assertIn('filepath', result)
        self.assertTrue(Path(result['filepath']).exists())

        # Verify file content
        with open(result['filepath'], 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertEqual(content, "<html><body>Test Content</body></html>")

    @patch('html_saver.requests.Session.get')
    def test_save_html_no_overwrite(self, mock_get):
        """Test that existing files are not overwritten by default"""
        # Mock response
        mock_response = Mock()
        mock_response.text = "<html><body>Test</body></html>"
        mock_response.url = "https://example.com"
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "text/html"}
        mock_response.apparent_encoding = "utf-8"
        mock_get.return_value = mock_response

        # Save first time
        result1 = self.saver.save_html(
            "https://example.com",
            filename="test.html"
        )
        self.assertTrue(result1['success'])

        # Try to save again without overwrite
        result2 = self.saver.save_html(
            "https://example.com",
            filename="test.html",
            overwrite=False
        )
        self.assertFalse(result2['success'])
        self.assertIn('already exists', result2['error'])

    @patch('html_saver.requests.Session.get')
    def test_save_html_with_overwrite(self, mock_get):
        """Test overwriting existing files"""
        # Mock responses
        mock_response1 = Mock()
        mock_response1.text = "<html><body>First</body></html>"
        mock_response1.url = "https://example.com"
        mock_response1.status_code = 200
        mock_response1.headers = {"Content-Type": "text/html"}
        mock_response1.apparent_encoding = "utf-8"

        mock_response2 = Mock()
        mock_response2.text = "<html><body>Second</body></html>"
        mock_response2.url = "https://example.com"
        mock_response2.status_code = 200
        mock_response2.headers = {"Content-Type": "text/html"}
        mock_response2.apparent_encoding = "utf-8"

        mock_get.side_effect = [mock_response1, mock_response2]

        # Save first time
        result1 = self.saver.save_html(
            "https://example.com",
            filename="test.html"
        )
        self.assertTrue(result1['success'])

        # Save again with overwrite
        result2 = self.saver.save_html(
            "https://example.com",
            filename="test.html",
            overwrite=True
        )
        self.assertTrue(result2['success'])

        # Verify content was overwritten
        with open(result2['filepath'], 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertEqual(content, "<html><body>Second</body></html>")

    @patch('html_saver.requests.Session.get')
    def test_save_multiple(self, mock_get):
        """Test saving multiple URLs"""
        # Mock response
        mock_response = Mock()
        mock_response.text = "<html><body>Test</body></html>"
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "text/html"}
        mock_response.apparent_encoding = "utf-8"

        def mock_get_side_effect(*args, **kwargs):
            response = Mock()
            response.text = f"<html><body>{args[0]}</body></html>"
            response.url = args[0]
            response.status_code = 200
            response.headers = {"Content-Type": "text/html"}
            response.apparent_encoding = "utf-8"
            return response

        mock_get.side_effect = mock_get_side_effect

        urls = [
            "https://example1.com",
            "https://example2.com",
            "https://example3.com"
        ]

        results = self.saver.save_multiple(urls, overwrite=True)

        self.assertEqual(len(results), 3)
        for result in results:
            self.assertTrue(result['success'])
            self.assertTrue(Path(result['filepath']).exists())


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestHTMLSaver)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    import sys
    sys.exit(run_tests())
