#!/usr/bin/env python3
"""
Quick test to verify the OptimizedAnalysisEngine fixes
"""

import sys
import time
sys.path.append('/Users/ginio/projects/Olympia/BoD Use Case')

from src.utils.optimized_analysis_engine import OptimizedAnalysisEngine

def quick_test():
    print("Testing OptimizedAnalysisEngine with Ollama...")
    
    # Simple test content
    test_content = """
    BOARD PRESENTATION Q1 2024
    
    We commit to launching the new product by June 2024.
    
    Main risks include supply chain issues and market competition.
    
    Revenue grew 15% to $2M this quarter.
    """
    
    try:
        engine = OptimizedAnalysisEngine("ollama", model="llama3.2:3b")
        
        print("Starting analysis...")
        start_time = time.time()
        
        result = engine.analyze_document(test_content)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"✅ Analysis completed in {duration:.2f} seconds")
        print(f"Result type: {type(result)}")
        
        if isinstance(result, dict):
            print("✅ No JSON parsing errors!")
            print(f"Keys in result: {list(result.keys())}")
            
            # Check commitments
            commitments = result.get('commitments', [])
            print(f"Found {len(commitments)} commitments")
            
            # Check risks  
            risks = result.get('risks', [])
            print(f"Found {len(risks)} risks")
            
            return True
        else:
            print(f"❌ Unexpected result type: {type(result)}")
            print(f"Result: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = quick_test()
    if success:
        print("\n🎉 QUICK TEST PASSED - System appears to be working!")
    else:
        print("\n❌ QUICK TEST FAILED - Issues remain")
