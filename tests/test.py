import sys
sys.path.insert(0, '..')
from main import _fetch_page_content

def main():
    url = "https://github.com/alexeygrigorev/minsearch"
    print(f"Fetching content from: {url}")
    content = _fetch_page_content(url)
    print(f"Content length: {len(content)}")
    print("-" * 20)
    print("Preview:")
    print(content[:200])

if __name__ == "__main__":
    main()
