#!/usr/bin/env python3
"""
Simple comparison between OpenAI and Ollama analysis performance
"""

import sys
import time
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Load .env file from project root
from dotenv import load_dotenv
load_dotenv(project_root / '.env')

from src.utils.optimized_analysis_engine import OptimizedAnalysisEngine
from src.models.document import ProcessedDocument, DocumentMetadata, DocumentPage
from src.utils.llm_providers import LLMProviderManager

def create_test_document():
    """Create a test document for comparison"""
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
    - Customer experience enhancement
    """
    
    metadata = DocumentMetadata(
        filename="test_comparison.txt",
        file_type="txt",
        total_pages=1,
        word_count=len(sample_text.split())
    )
    
    page = DocumentPage(page_number=1, text=sample_text)
    return ProcessedDocument(
        pages=[page],
        metadata=metadata,
        full_text=sample_text
    )

def run_analysis_comparison():
    """Compare OpenAI vs Ollama analysis performance"""
    print("🔄 Simple Comparison: OpenAI vs Ollama")
    print("=" * 50)
    
    # Check available providers
    manager = LLMProviderManager()
    available_providers = manager.get_available_providers()
    
    print(f"Available providers: {available_providers}")
    
    # Create test document
    test_doc = create_test_document()
    print(f"Test document: {len(test_doc.full_text)} characters")
    
    # Initialize engine
    engine = OptimizedAnalysisEngine()
    
    results = {}
    
    # Test providers that are available
    providers_to_test = []
    if "openai" in available_providers:
        providers_to_test.append("openai")
    if "ollama" in available_providers:
        providers_to_test.append("ollama")
    
    if not providers_to_test:
        print("❌ No providers available for comparison")
        return False
    
    for provider in providers_to_test:
        print(f"\n🧪 Testing {provider.upper()}...")
        try:
            start_time = time.time()
            analysis_results = engine.analyze_document_optimized(test_doc, provider=provider)
            end_time = time.time()
            
            duration = end_time - start_time
            
            results[provider] = {
                "duration": duration,
                "success": True,
                "commitments": len(analysis_results.get('enhanced_commitments', [])),
                "risks": len(analysis_results.get('risk_assessment', [])),
                "financial": len(analysis_results.get('financial_insights', [])),
                "results": analysis_results
            }
            
            print(f"✅ {provider.capitalize()} completed in {duration:.1f}s")
            print(f"   Commitments: {results[provider]['commitments']}")
            print(f"   Risks: {results[provider]['risks']}")
            print(f"   Financial insights: {results[provider]['financial']}")
            
        except Exception as e:
            print(f"❌ {provider.capitalize()} failed: {e}")
            results[provider] = {
                "duration": 0,
                "success": False,
                "error": str(e)
            }
    
    # Display comparison
    print(f"\n📊 COMPARISON RESULTS")
    print("=" * 50)
    
    successful_tests = [p for p in providers_to_test if results[p]['success']]
    
    if len(successful_tests) >= 2:
        # Performance comparison
        print("⚡ Performance Comparison:")
        for provider in successful_tests:
            result = results[provider]
            print(f"   {provider.capitalize():10}: {result['duration']:6.1f}s")
        
        # Quality comparison
        print("\n🎯 Quality Comparison:")
        for provider in successful_tests:
            result = results[provider]
            print(f"   {provider.capitalize():10}: {result['commitments']} commitments, {result['risks']} risks, {result['financial']} financial")
        
        # Speed winner
        fastest = min(successful_tests, key=lambda p: results[p]['duration'])
        print(f"\n🏆 Fastest: {fastest.capitalize()} ({results[fastest]['duration']:.1f}s)")
        
    elif len(successful_tests) == 1:
        provider = successful_tests[0]
        print(f"✅ Only {provider.capitalize()} available and working")
        print(f"   Duration: {results[provider]['duration']:.1f}s")
        print(f"   Results: {results[provider]['commitments']} commitments, {results[provider]['risks']} risks")
    else:
        print("❌ No successful analyses")
        return False
    
    return True

def main():
    """Main comparison function"""
    print("🚀 Simple Comparison Test")
    print("=" * 50)
    
    success = run_analysis_comparison()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Comparison test completed successfully!")
    else:
        print("❌ Comparison test failed")
    print("=" * 50)

if __name__ == "__main__":
    main()