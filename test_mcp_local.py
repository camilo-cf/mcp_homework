import main
import json

print("Testing search logic (internal function)...")
try:
    # Call the internal function directly to verify logic
    # The MCP tool wrapper simply calls this and dumps to JSON
    raw_results = main._search("demo")
    
    # Simulate the tool's behavior
    result_json = json.dumps(raw_results)
    
    print("\nResult JSON (simulated tool output):")
    print(result_json)
    
    results = json.loads(result_json)
    print(f"\nFound {len(results)} results.")
    if len(results) > 0:
        print(f"First result: {results[0]['filename']}")
except Exception as e:
    print(f"Error calling search: {e}")
