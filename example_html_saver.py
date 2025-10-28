"""
Example usage of HTMLSaver module
Demonstrates various ways to use the HTML saver functionality
"""

from html_saver import HTMLSaver


def example_basic_usage():
    """Basic usage example"""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)

    # Create an HTMLSaver instance
    saver = HTMLSaver(output_dir="saved_html")

    # Save HTML from a single URL
    url = "https://example.com"
    result = saver.save_html(url)

    if result['success']:
        print(f"✓ Successfully saved HTML")
        print(f"  URL: {result['url']}")
        print(f"  File: {result['filepath']}")
        print(f"  Size: {result['size_bytes']:,} bytes")
    else:
        print(f"✗ Failed to save HTML")
        print(f"  Error: {result['error']}")

    print()


def example_custom_filename():
    """Example with custom filename"""
    print("=" * 60)
    print("Example 2: Custom Filename")
    print("=" * 60)

    saver = HTMLSaver(output_dir="saved_html")

    url = "https://example.com"
    result = saver.save_html(url, filename="my_custom_page.html", overwrite=True)

    if result['success']:
        print(f"✓ Saved with custom filename")
        print(f"  File: {result['filepath']}")
    else:
        print(f"✗ Failed: {result['error']}")

    print()


def example_multiple_urls():
    """Example saving multiple URLs"""
    print("=" * 60)
    print("Example 3: Multiple URLs")
    print("=" * 60)

    saver = HTMLSaver(output_dir="saved_html")

    urls = [
        "https://example.com",
        "https://www.wikipedia.org",
        "https://www.github.com"
    ]

    results = saver.save_multiple(urls)

    success_count = sum(1 for r in results if r['success'])
    print(f"Processed {len(results)} URLs")
    print(f"  Success: {success_count}")
    print(f"  Failed: {len(results) - success_count}")
    print()

    for i, result in enumerate(results, 1):
        status = "✓" if result['success'] else "✗"
        print(f"{i}. {status} {result['url']}")
        if result['success']:
            print(f"   → {result['filepath']}")
        else:
            print(f"   → Error: {result['error']}")

    print()


def example_custom_directory():
    """Example with custom output directory"""
    print("=" * 60)
    print("Example 4: Custom Output Directory")
    print("=" * 60)

    # Save to a different directory
    saver = HTMLSaver(output_dir="my_html_archive")

    url = "https://example.com"
    result = saver.save_html(url, overwrite=True)

    if result['success']:
        print(f"✓ Saved to custom directory")
        print(f"  File: {result['filepath']}")
    else:
        print(f"✗ Failed: {result['error']}")

    print()


def example_error_handling():
    """Example demonstrating error handling"""
    print("=" * 60)
    print("Example 5: Error Handling")
    print("=" * 60)

    saver = HTMLSaver()

    # Try to fetch from an invalid URL
    invalid_urls = [
        "https://this-domain-definitely-does-not-exist-12345.com",
        "not-a-valid-url",
        "https://httpstat.us/404"  # Will return 404 error
    ]

    for url in invalid_urls:
        result = saver.save_html(url)
        if not result['success']:
            print(f"✗ {url}")
            print(f"   Error: {result['error']}")
            print()


def example_fetch_only():
    """Example: Fetch HTML without saving"""
    print("=" * 60)
    print("Example 6: Fetch Only (No Saving)")
    print("=" * 60)

    saver = HTMLSaver()

    url = "https://example.com"
    result = saver.fetch_html(url)

    if result['success']:
        print(f"✓ Successfully fetched HTML")
        print(f"  URL: {result['url']}")
        print(f"  Status: {result['status_code']}")
        print(f"  Content length: {len(result['content'])} characters")
        print(f"  First 200 characters:")
        print(f"  {result['content'][:200]}...")
    else:
        print(f"✗ Failed: {result['error']}")

    print()


def main():
    """Run all examples"""
    print("\n")
    print("=" * 60)
    print("HTML SAVER - USAGE EXAMPLES")
    print("=" * 60)
    print()

    try:
        # Run examples
        example_basic_usage()
        example_custom_filename()
        example_multiple_urls()
        example_custom_directory()
        example_fetch_only()
        # example_error_handling()  # Uncomment to test error cases

        print("=" * 60)
        print("All examples completed!")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user")
    except Exception as e:
        print(f"\n\nError running examples: {e}")


if __name__ == "__main__":
    main()
