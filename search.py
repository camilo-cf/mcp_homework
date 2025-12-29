from main import _search

def main():
    query = "demo"
    print(f"Searching for: '{query}'")
    results = _search(query, top_k=5)
    
    print(f"\nFound {len(results)} results:")
    for i, result in enumerate(results):
        print(f"{i+1}. {result['filename']}")
    
    if results:
        print(f"\nFirst result: {results[0]['filename']}")

if __name__ == "__main__":
    main()
