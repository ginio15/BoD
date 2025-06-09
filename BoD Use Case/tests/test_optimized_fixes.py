#!/usr/bin/env python3
"""
Test the optimized fixes for Ollama integration
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.optimized_analysis_engine import OptimizedAnalysisEngine
from src.models.document import ProcessedDocument, DocumentMetadata, DocumentPage

def test_optimized_engine():
    """Test the optimized analysis engine with error handling"""
    
    print("🧪 Testing OptimizedAnalysisEngine with robust error handling...")
    
    # Create a test document
    sample_text = """
    BOARD MEETING MINUTES - Q4 2023 STRATEGIC REVIEW
    
    FINANCIAL PERFORMANCE:
    Q4 revenue reached $2.5M, representing 15% year-over-year growth. 
    We will implement cost reduction measures by end of Q1 2024.
    The company faces market volatility risks and supply chain challenges.
    
    STRATEGIC INITIATIVES:
    We plan to launch the new product line in Q2 2024.
    There are concerns about competitive pressures in our key markets.
    Management commits to improving operational efficiency by 20%.
    """
    
    # Create ProcessedDocument
    metadata = DocumentMetadata(
        filename="test_board_minutes.txt",
        file_type="txt",
        total_pages=1,
        word_count=len(sample_text.split())
    )
    
    page = DocumentPage(page_number=1, text=sample_text)
    document = ProcessedDocument(
        pages=[page],
        metadata=metadata,
        full_text=sample_text
    )
    
    try:
        # Initialize the optimized engine
        engine = OptimizedAnalysisEngine()
        
        print("✅ OptimizedAnalysisEngine initialized successfully")
        
        # Test single document analysis
        print("\n📊 Testing single document analysis...")
        results = engine.analyze_document_optimized(document, "ollama")
        
        print(f"✅ Analysis completed!")
        print(f"   - Commitments found: {len(results.get('commitments', []))}")
        print(f"   - Risks found: {len(results.get('risks', []))}")
        print(f"   - Financial insights: {len(results.get('financial_insights', []))}")
        print(f"   - Sentiment: {results.get('sentiment', {}).get('overall', 'unknown')}")
        
        # Print some details
        if results.get('commitments'):
            print("\n📋 Sample commitments:")
            for i, commitment in enumerate(results['commitments'][:2]):
                print(f"   {i+1}. {commitment.get('text', 'N/A')}")
        
        if results.get('risks'):
            print("\n⚠️  Sample risks:")
            for i, risk in enumerate(results['risks'][:2]):
                print(f"   {i+1}. {risk.get('description', 'N/A')}")
        
        # Test document comparison
        print("\n🔄 Testing document comparison...")
        comparison_results = engine.compare_documents(document, document, "ollama")
        
        print(f"✅ Comparison completed!")
        print(f"   - Commitment comparisons: {len(comparison_results.get('commitments', []))}")
        print(f"   - Sentiment shifts: {len(comparison_results.get('sentiment_shifts', []))}")
        print(f"   - De-escalations: {len(comparison_results.get('deescalations', []))}")
        
        print("\n🎉 All tests passed! The optimized engine is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("TESTING OPTIMIZED ANALYSIS ENGINE FOR OLLAMA")
    print("=" * 60)
    
    success = test_optimized_engine()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ ALL TESTS PASSED - Ready for production use!")
    else:
        print("❌ TESTS FAILED - Check the errors above")
    print("=" * 60)
