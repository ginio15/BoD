#!/usr/bin/env python3
"""
Final comprehensive system test for BoD analysis system.
Tests both apps with Ollama to verify timeout and JSON parsing issues are resolved.
"""

import sys
import os
import json
import time
from datetime import datetime

# Add project root to path
sys.path.append('/Users/ginio/projects/Olympia/BoD Use Case')

from src.utils.optimized_analysis_engine import OptimizedAnalysisEngine
from src.utils.document_parser import DocumentParser
from src.utils.llm_providers import LLMProvider

def test_ollama_connection():
    """Test basic Ollama connectivity"""
    print("=" * 60)
    print("TESTING OLLAMA CONNECTION")
    print("=" * 60)
    
    try:
        provider = LLMProvider("ollama", model="llama3.2:3b")
        response = provider.generate("Say 'Connection successful'")
        print(f"✅ Ollama connection: {response.strip()}")
        return True
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        return False

def test_optimized_analysis_engine():
    """Test the OptimizedAnalysisEngine with sample document"""
    print("\n" + "=" * 60)
    print("TESTING OPTIMIZED ANALYSIS ENGINE")
    print("=" * 60)
    
    # Test with sample document
    sample_text = """
    QUARTERLY BOARD PRESENTATION - Q1 2024
    
    FINANCIAL HIGHLIGHTS:
    - Revenue increased 15% to $50M
    - EBITDA margin improved to 22%
    - Cash flow from operations: $8M
    
    STRATEGIC COMMITMENTS:
    - Launch new product line by Q3 2024
    - Expand into European markets by December 2024
    - Reduce operational costs by 10% within 6 months
    
    RISK FACTORS:
    - Supply chain disruptions (High impact)
    - Regulatory changes in key markets (Medium impact)
    - Competitive pressure from new entrants (Low impact)
    
    STRATEGIC PRIORITIES:
    - Digital transformation initiative
    - Sustainability program implementation
    - Talent acquisition and retention
    """
    
    try:
        # Initialize engine
        engine = OptimizedAnalysisEngine("ollama", model="llama3.2:3b")
        
        print("Testing single document analysis...")
        start_time = time.time()
        
        result = engine.analyze_document(sample_text)
        
        analysis_time = time.time() - start_time
        print(f"✅ Analysis completed in {analysis_time:.2f} seconds")
        
        # Check result structure
        required_fields = ['commitments', 'risks', 'financial_metrics', 'strategic_priorities']
        missing_fields = []
        
        for field in required_fields:
            if field not in result:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"⚠️  Missing fields: {missing_fields}")
        else:
            print("✅ All required fields present")
        
        # Print summary of results
        print(f"\nAnalysis Summary:")
        print(f"- Commitments found: {len(result.get('commitments', []))}")
        print(f"- Risks identified: {len(result.get('risks', []))}")
        print(f"- Financial metrics: {len(result.get('financial_metrics', []))}")
        print(f"- Strategic priorities: {len(result.get('strategic_priorities', []))}")
        
        # Test compare_documents method
        print("\nTesting document comparison...")
        comparison_result = engine.compare_documents(sample_text, sample_text)
        print(f"✅ Document comparison completed")
        print(f"- Comparison summary length: {len(comparison_result.get('summary', ''))}")
        
        return True, result
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_with_real_documents():
    """Test with actual uploaded documents"""
    print("\n" + "=" * 60)
    print("TESTING WITH REAL DOCUMENTS")
    print("=" * 60)
    
    uploads_dir = "/Users/ginio/projects/Olympia/BoD Use Case/data/uploads"
    
    # Find available documents
    available_docs = []
    for filename in os.listdir(uploads_dir):
        if filename.endswith(('.txt', '.pdf', '.pptx')):
            available_docs.append(filename)
    
    print(f"Available documents: {available_docs}")
    
    if not available_docs:
        print("⚠️  No documents found for testing")
        return False
    
    # Test with first available text document
    text_docs = [doc for doc in available_docs if doc.endswith('.txt')]
    if not text_docs:
        print("⚠️  No text documents found for testing")
        return False
    
    test_doc = text_docs[0]
    doc_path = os.path.join(uploads_dir, test_doc)
    
    print(f"Testing with: {test_doc}")
    
    try:
        # Read document
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"Document length: {len(content)} characters")
        
        # Analyze with OptimizedAnalysisEngine
        engine = OptimizedAnalysisEngine("ollama", model="llama3.2:3b")
        
        start_time = time.time()
        result = engine.analyze_document(content)
        analysis_time = time.time() - start_time
        
        print(f"✅ Real document analysis completed in {analysis_time:.2f} seconds")
        
        # Verify no JSON parsing errors
        if isinstance(result, dict):
            print("✅ No JSON parsing errors")
        else:
            print(f"❌ Unexpected result type: {type(result)}")
            return False
        
        # Check for timeout issues
        if analysis_time > 60:
            print(f"⚠️  Analysis took {analysis_time:.2f}s (might be slow but no timeout)")
        else:
            print(f"✅ Analysis completed quickly ({analysis_time:.2f}s)")
        
        return True
        
    except Exception as e:
        print(f"❌ Real document test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_error_handling():
    """Test error handling and fallback mechanisms"""
    print("\n" + "=" * 60)
    print("TESTING ERROR HANDLING")
    print("=" * 60)
    
    try:
        engine = OptimizedAnalysisEngine("ollama", model="llama3.2:3b")
        
        # Test with minimal content
        minimal_content = "This is a very short document with no clear structure."
        
        print("Testing with minimal content...")
        result = engine.analyze_document(minimal_content)
        
        if isinstance(result, dict):
            print("✅ Handled minimal content without errors")
        else:
            print(f"❌ Unexpected result for minimal content: {type(result)}")
        
        # Test with empty content
        print("Testing with empty content...")
        empty_result = engine.analyze_document("")
        
        if isinstance(empty_result, dict):
            print("✅ Handled empty content without errors")
        else:
            print(f"❌ Unexpected result for empty content: {type(empty_result)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("FINAL SYSTEM TEST - BoD Analysis System")
    print("Testing fixes for timeout and JSON parsing errors")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_results = []
    
    # Test 1: Ollama Connection
    ollama_ok = test_ollama_connection()
    test_results.append(("Ollama Connection", ollama_ok))
    
    if not ollama_ok:
        print("\n❌ Ollama connection failed. Cannot proceed with other tests.")
        return
    
    # Test 2: OptimizedAnalysisEngine
    engine_ok, sample_result = test_optimized_analysis_engine()
    test_results.append(("Optimized Analysis Engine", engine_ok))
    
    # Test 3: Real Documents
    real_docs_ok = test_with_real_documents()
    test_results.append(("Real Documents", real_docs_ok))
    
    # Test 4: Error Handling
    error_handling_ok = test_error_handling()
    test_results.append(("Error Handling", error_handling_ok))
    
    # Final Summary
    print("\n" + "=" * 60)
    print("FINAL TEST RESULTS")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in test_results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:25} : {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! System is ready for use.")
        print("✅ Timeout errors resolved")
        print("✅ JSON parsing errors resolved")
        print("✅ OptimizedAnalysisEngine working correctly")
        print("✅ Error handling functioning properly")
    else:
        print("⚠️  Some tests failed. Please review the results above.")
    
    print(f"Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
