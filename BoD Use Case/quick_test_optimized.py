#!/usr/bin/env python3
"""
Quick test of optimized analysis engine
"""

import sys
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from src.utils.optimized_analysis_engine import OptimizedAnalysisEngine
from src.models.document import ProcessedDocument, DocumentPage, DocumentMetadata

def quick_test():
    print("Testing Optimized Analysis Engine...")
    
    # Simple test document
    text = """
    Board Meeting Q4 2024
    
    Decisions:
    1. Approved $2M budget for digital transformation
    2. Committed to 15% cost reduction by Q2 2025
    3. Risk: supply chain disruptions possible
    
    Revenue up 12% YoY. Board is optimistic about growth.
    """
    
    # Create document
    page = DocumentPage(page_number=1, text=text)
    doc = ProcessedDocument(
        pages=[page],
        metadata=DocumentMetadata(
            filename="test.txt",
            file_type="txt",
            title="Test"
        )
    )
    
    # Test analysis
    print("Creating OptimizedAnalysisEngine...")
    engine = OptimizedAnalysisEngine()
    
    try:
        print("Starting analysis...")
        results = engine.analyze_document_optimized(doc)
        
        print(f"✅ Analysis completed!")
        print(f"Commitments found: {len(results.get('commitments', []))}")
        print(f"Risks found: {len(results.get('risks', []))}")
        print(f"Financial insights: {len(results.get('financial_insights', []))}")
        print(f"Sentiment: {results.get('sentiment', {}).get('overall', 'unknown')}")
        
        if results.get('commitments'):
            print("\nCommitments:")
            for i, c in enumerate(results['commitments'][:2]):
                print(f"  {i+1}. {c.get('text', 'Unknown')}")
                
        print(f"Summary: {results.get('summary', 'No summary')}")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = quick_test()
    if success:
        print("\n🎉 Quick test passed!")
    else:
        print("\n❌ Quick test failed!")
