#!/usr/bin/env python3
"""
Debug the OptimizedAnalysisEngine to see why it's returning zero results
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from src.utils.optimized_analysis_engine import OptimizedAnalysisEngine
from src.models.document import ProcessedDocument, DocumentMetadata, DocumentPage

def debug_analysis():
    """Debug the analysis engine step by step"""
    
    # Sample text with clear commitments and risks
    sample_text = """
    BOARD MEETING MINUTES - Q4 2023 STRATEGIC REVIEW
    
    FINANCIAL PERFORMANCE:
    Q4 revenue reached $2.5M, representing 15% year-over-year growth and exceeding our 
    target of $2.3M. Net profit margin improved to 12% from 8% in Q4 2022.
    
    STRATEGIC COMMITMENTS FOR 2024:
    1. Cost Optimization: We will reduce operational expenses by 10% by Q2 2024
    2. Product Launch: Committed to launching new AI analytics platform in Q3 2024
    3. Market Expansion: Target European market entry by December 2024 with $500K investment
    
    RISK ASSESSMENT:
    High Priority: Supply chain disruptions may impact Q1 delivery schedules
    Medium Priority: Currency fluctuations could affect European expansion costs
    Low Priority: Regulatory changes in data privacy laws require monitoring
    """
    
    print("🧪 DEBUG: Testing OptimizedAnalysisEngine")
    print("=" * 60)
    
    # Create ProcessedDocument
    metadata = DocumentMetadata(
        filename="debug_test.txt",
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
        # Initialize the engine
        print("📋 Initializing OptimizedAnalysisEngine...")
        engine = OptimizedAnalysisEngine()
        print("✅ Engine initialized")
        
        # Test each extraction method individually
        print("\n🔍 Testing individual extraction methods:")
        
        # Test commitment extraction
        print("\n1. Testing commitment extraction...")
        commitments = engine._extract_commitments_simple(sample_text, "ollama")
        print(f"   Found {len(commitments)} commitments:")
        for i, commitment in enumerate(commitments):
            print(f"   {i+1}. {commitment}")
        
        # Test risk extraction
        print("\n2. Testing risk extraction...")
        risks = engine._extract_risks_simple(sample_text, "ollama")
        print(f"   Found {len(risks)} risks:")
        for i, risk in enumerate(risks):
            print(f"   {i+1}. {risk}")
        
        # Test financial extraction
        print("\n3. Testing financial extraction...")
        financial = engine._extract_financial_simple(sample_text, "ollama")
        print(f"   Found {len(financial)} financial insights:")
        for i, insight in enumerate(financial):
            print(f"   {i+1}. {insight}")
        
        # Test sentiment analysis
        print("\n4. Testing sentiment analysis...")
        sentiment = engine._analyze_sentiment_simple(sample_text, "ollama")
        print(f"   Sentiment result: {sentiment}")
        
        # Test full analysis
        print("\n🚀 Testing full document analysis...")
        results = engine.analyze_document_optimized(document, "ollama")
        
        print(f"\n📊 FULL ANALYSIS RESULTS:")
        print(f"   - Commitments: {len(results.get('commitments', []))}")
        print(f"   - Risks: {len(results.get('risks', []))}")
        print(f"   - Financial insights: {len(results.get('financial_insights', []))}")
        print(f"   - Sentiment: {results.get('sentiment', {})}")
        print(f"   - Summary: {results.get('summary', 'None')[:100]}...")
        
        # Test fallback methods
        print("\n🔄 Testing fallback methods...")
        fallback_commitments = engine._extract_commitments_fallback(sample_text)
        fallback_risks = engine._extract_risks_fallback(sample_text)
        
        print(f"   Fallback commitments: {len(fallback_commitments)}")
        print(f"   Fallback risks: {len(fallback_risks)}")
        
        return results
        
    except Exception as e:
        print(f"❌ Error during debug: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    debug_analysis()
