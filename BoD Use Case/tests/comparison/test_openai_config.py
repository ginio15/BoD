#!/usr/bin/env python3
"""
Test OpenAI configuration and basic analysis functionality
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

def test_openai_config():
    """Test OpenAI configuration and basic analysis"""
    print("🔍 Testing OpenAI Configuration")
    print("=" * 50)
    
    # Check if OpenAI is available
    manager = LLMProviderManager()
    available_providers = manager.get_available_providers()
    
    if "openai" not in available_providers:
        print("❌ OpenAI not available - check your API key configuration")
        print("   Set OPENAI_API_KEY in your .env file")
        return False
        
    print(f"✅ OpenAI provider available")
    
    # Create test document
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
        filename="test_openai_config.txt",
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
        # Test analysis with OpenAI
        print("\n📊 Running analysis with OpenAI...")
        engine = OptimizedAnalysisEngine()
        
        start_time = time.time()
        results = engine.analyze_document_optimized(document, provider="openai")
        analysis_time = time.time() - start_time
        
        print(f"✅ Analysis completed in {analysis_time:.1f} seconds")
        
        # Display results
        commitments = results.get('enhanced_commitments', [])
        risks = results.get('risk_assessment', [])
        financial = results.get('financial_insights', [])
        
        print(f"\n📋 Results Summary:")
        print(f"   Commitments found: {len(commitments)}")
        print(f"   Risks identified: {len(risks)}")
        print(f"   Financial insights: {len(financial)}")
        
        if commitments:
            print(f"\n📌 Sample Commitment:")
            commitment = commitments[0]
            print(f"   Text: {commitment.get('text', 'N/A')[:80]}...")
            print(f"   Confidence: {commitment.get('confidence', 'N/A')}")
            
        if risks:
            print(f"\n⚠️  Sample Risk:")
            risk = risks[0]
            print(f"   Description: {risk.get('description', 'N/A')[:80]}...")
            print(f"   Level: {risk.get('risk_level', 'N/A')}")
        
        print(f"\n✅ OpenAI configuration test passed!")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 OpenAI Configuration Test")
    print("=" * 50)
    
    success = test_openai_config()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ OpenAI configuration is working correctly!")
        print("   Ready for production use with OpenAI provider")
    else:
        print("❌ OpenAI configuration test failed")
        print("   Check your API key and configuration")
    print("=" * 50)

if __name__ == "__main__":
    main()