#!/usr/bin/env python3
"""
Test the optimized analysis engine with various text lengths
"""

import sys
import time
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.optimized_analysis_engine import OptimizedAnalysisEngine
from src.models.document import ProcessedDocument, DocumentPage

def create_test_document(text: str, title: str = "Test Document") -> ProcessedDocument:
    """Create a test document from text"""
    page = DocumentPage(
        page_number=1,
        content=text,
        images=[]
    )
    
    return ProcessedDocument(
        filename=f"{title}.txt",
        pages=[page],
        full_text=text,
        metadata={"title": title}
    )

def test_short_text():
    """Test with short text (should work fine)"""
    print("\n" + "="*50)
    print("TEST 1: Short Text Analysis")
    print("="*50)
    
    short_text = """
    Board of Directors Meeting - Q4 2024
    
    Key Decisions:
    1. Approved $2M budget increase for digital transformation initiative
    2. Committed to reducing operational costs by 15% by Q2 2025
    3. Risk identified: potential supply chain disruptions in Asia
    4. Strategic priority: expand into European markets by end of 2025
    
    Financial Update:
    - Revenue up 12% YoY
    - Operating margins improved to 18.5%
    - Cash flow positive for 6 consecutive quarters
    
    The board expressed optimism about the company's growth trajectory.
    """
    
    engine = OptimizedAnalysisEngine()
    doc = create_test_document(short_text, "Short Board Meeting")
    
    start_time = time.time()
    try:
        results = engine.analyze_document_optimized(doc)
        end_time = time.time()
        
        print(f"✅ Analysis completed in {end_time - start_time:.2f} seconds")
        print(f"Found {len(results['commitments'])} commitments")
        print(f"Found {len(results['risks'])} risks") 
        print(f"Found {len(results['financial_insights'])} financial insights")
        print(f"Sentiment: {results['sentiment'].get('overall', 'unknown')}")
        print(f"Summary: {results['summary'][:100]}...")
        
        return True
        
    except Exception as e:
        end_time = time.time()
        print(f"❌ Analysis failed after {end_time - start_time:.2f} seconds: {e}")
        return False

def test_medium_text():
    """Test with medium-length text"""
    print("\n" + "="*50)
    print("TEST 2: Medium Text Analysis")
    print("="*50)
    
    # Create a longer text (around 1500 chars)
    medium_text = """
    Board of Directors Quarterly Meeting - Q4 2024
    
    EXECUTIVE SUMMARY:
    The board convened to review Q4 performance, approve strategic initiatives, and address emerging risks.
    Overall performance exceeded expectations with strong revenue growth and improved operational efficiency.
    
    KEY DECISIONS AND COMMITMENTS:
    1. Digital Transformation Initiative: Approved $2M budget allocation for enterprise software upgrade
       Timeline: Implementation to begin Q1 2025, completion by Q3 2025
       Expected ROI: 25% efficiency improvement within first year
    
    2. Cost Reduction Program: Committed to achieving 15% operational cost reduction by Q2 2025
       Target areas: Administrative overhead, vendor consolidation, process automation
       Responsible: CFO to lead cross-functional team
    
    3. Market Expansion: Authorization for European market entry strategy
       Budget: $5M over 18 months starting Q2 2025
       Markets: Germany, France, Netherlands as primary targets
    
    RISK ASSESSMENT:
    1. Supply Chain Vulnerability: Identified potential disruptions in Asian suppliers
       Impact: Could affect 30% of production capacity
       Mitigation: Diversifying supplier base, building strategic inventory
    
    2. Regulatory Changes: New data privacy regulations in target markets
       Impact: May require additional compliance investments
       Timeline: New regulations effective January 2025
    
    3. Competitive Pressure: Two major competitors announced similar digital initiatives
       Response: Accelerate our timeline and differentiate through customer experience
    
    FINANCIAL HIGHLIGHTS:
    - Revenue: $45M (up 12% YoY)
    - Operating Margin: 18.5% (improvement from 16.2% last year)
    - Free Cash Flow: $8.2M positive (6th consecutive positive quarter)
    - R&D Investment: Increased to 12% of revenue to support innovation
    
    STRATEGIC PRIORITIES FOR 2025:
    1. Complete digital transformation initiative
    2. Successfully enter European markets
    3. Achieve operational excellence targets
    4. Strengthen competitive positioning through innovation
    
    The board expressed strong confidence in management's execution capabilities and the company's strategic direction.
    Market conditions remain favorable, though we must remain vigilant about emerging risks.
    """
    
    engine = OptimizedAnalysisEngine()
    doc = create_test_document(medium_text, "Medium Board Meeting")
    
    start_time = time.time()
    try:
        results = engine.analyze_document_optimized(doc)
        end_time = time.time()
        
        print(f"✅ Analysis completed in {end_time - start_time:.2f} seconds")
        print(f"Text length: {len(medium_text)} characters")
        print(f"Found {len(results['commitments'])} commitments")
        print(f"Found {len(results['risks'])} risks")
        print(f"Found {len(results['financial_insights'])} financial insights")
        print(f"Sentiment: {results['sentiment'].get('overall', 'unknown')}")
        
        # Show some details
        if results['commitments']:
            print("\nSample Commitments:")
            for i, commitment in enumerate(results['commitments'][:2]):
                print(f"  {i+1}. {commitment['text'][:100]}...")
        
        return True
        
    except Exception as e:
        end_time = time.time()
        print(f"❌ Analysis failed after {end_time - start_time:.2f} seconds: {e}")
        return False

def test_long_text():
    """Test with long text that would cause timeouts in the original engine"""
    print("\n" + "="*50)
    print("TEST 3: Long Text Analysis (Chunking Test)")
    print("="*50)
    
    # Create very long text by repeating content
    base_content = """
    Board of Directors Meeting Minutes - Strategic Planning Session
    
    The quarterly board meeting addressed multiple strategic initiatives, financial performance,
    and risk management considerations. Key stakeholders presented comprehensive reports on
    market conditions, competitive landscape, and operational performance metrics.
    
    Strategic Initiative Review:
    The digital transformation project continues to show promising results with initial
    implementation phases exceeding performance benchmarks. The investment in cloud
    infrastructure has improved system reliability by 35% and reduced operational costs
    by $1.2M annually. The board committed to accelerating the rollout to remaining
    business units by Q2 2025, with an additional budget allocation of $3M approved.
    
    Market Analysis and Expansion Plans:
    Management presented detailed analysis of European market opportunities, identifying
    Germany and France as primary targets for expansion. The total addressable market
    is estimated at $150M with projected capture rate of 5-8% within three years.
    Risk factors include regulatory compliance costs, cultural adaptation requirements,
    and competitive response from established local players.
    
    Financial Performance Review:
    Q4 results demonstrate strong momentum with revenue growth of 18% year-over-year,
    driven primarily by new product launches and improved customer retention rates.
    Operating margins expanded to 22.1%, reflecting operational efficiency improvements
    and favorable product mix shifts toward higher-margin offerings.
    
    Risk Management Discussion:
    The board reviewed enterprise risk framework updates, focusing on cybersecurity
    threats, supply chain vulnerabilities, and regulatory compliance requirements.
    Three critical risks were identified requiring immediate attention and mitigation
    strategies. Investment in cybersecurity infrastructure approved at $2.5M over
    18 months to address growing threat landscape.
    """
    
    # Repeat to create very long text
    long_text = (base_content + "\n\n") * 5  # About 5000+ characters
    
    engine = OptimizedAnalysisEngine()
    doc = create_test_document(long_text, "Long Board Meeting")
    
    print(f"Text length: {len(long_text)} characters")
    print(f"Expected chunks: {len(long_text) // 2000 + 1}")
    
    start_time = time.time()
    try:
        results = engine.analyze_document_optimized(doc)
        end_time = time.time()
        
        print(f"✅ Analysis completed in {end_time - start_time:.2f} seconds")
        print(f"Found {len(results['commitments'])} commitments")
        print(f"Found {len(results['risks'])} risks")
        print(f"Found {len(results['financial_insights'])} financial insights")
        print(f"Sentiment: {results['sentiment'].get('overall', 'unknown')}")
        
        return True
        
    except Exception as e:
        end_time = time.time()
        print(f"❌ Analysis failed after {end_time - start_time:.2f} seconds: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing Optimized Analysis Engine")
    print("This tests the timeout-resistant version with chunking")
    
    results = []
    
    # Test 1: Short text
    results.append(test_short_text())
    
    # Test 2: Medium text  
    results.append(test_medium_text())
    
    # Test 3: Long text (chunking)
    results.append(test_long_text())
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Optimized engine is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the logs above for details.")

if __name__ == "__main__":
    main()
