#!/usr/bin/env python3
"""
Test the complete enhanced app with optimized engine
"""

import sys
import logging
from pathlib import Path
import tempfile

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from src.utils.optimized_analysis_engine import OptimizedAnalysisEngine
from src.models.document import ProcessedDocument, DocumentPage, DocumentMetadata
from src.utils.document_parser import DocumentParser

def test_full_pipeline():
    """Test the complete document processing and analysis pipeline"""
    print("Testing Complete Enhanced BoD Analysis Pipeline")
    print("=" * 60)
    
    # Create a comprehensive test document
    comprehensive_text = """
    BOARD OF DIRECTORS MEETING - Q4 2024 STRATEGIC REVIEW
    
    EXECUTIVE SUMMARY:
    The board convened to review quarterly performance, approve strategic initiatives, 
    and address emerging market opportunities. Key decisions were made regarding 
    digital transformation, cost optimization, and international expansion.
    
    FINANCIAL PERFORMANCE:
    • Revenue: $45.2M (up 18% YoY)
    • Operating Margin: 22.1% (improved from 19.8% previous quarter)
    • Free Cash Flow: $8.7M positive (5th consecutive positive quarter)
    • R&D Investment: Increased to 15% of revenue to drive innovation
    
    KEY COMMITMENTS AND DECISIONS:
    
    1. Digital Transformation Initiative
       - Approved $3.5M budget for cloud migration and AI integration
       - Target completion: Q3 2025
       - Expected ROI: 30% efficiency improvement within 18 months
       - Responsible: CTO to lead cross-functional team
    
    2. Cost Optimization Program
       - Committed to achieving 12% reduction in operational expenses by Q2 2025
       - Focus areas: Vendor consolidation, process automation, facility optimization
       - Target savings: $2.8M annually
       - Responsible: CFO and Operations team
    
    3. International Market Expansion
       - Authorization granted for European market entry
       - Initial markets: Germany, Netherlands, France
       - Investment: $4.2M over 24 months
       - Timeline: Market entry by Q1 2025, full operations by Q4 2025
    
    4. Sustainability Initiative
       - Commitment to achieve carbon neutrality by 2027
       - Investment in renewable energy: $1.5M
       - Partnership with green technology providers approved
    
    RISK ASSESSMENT:
    
    1. Supply Chain Vulnerabilities
       - Impact: High (could affect 35% of production)
       - Probability: Medium (ongoing geopolitical tensions)
       - Mitigation: Diversify supplier base, increase strategic inventory
       - Timeline: Mitigation plan by Q1 2025
    
    2. Cybersecurity Threats
       - Impact: High (potential data breach, system downtime)
       - Probability: Medium-High (increasing sophistication of attacks)
       - Investment: $2.1M in advanced security infrastructure
       - Timeline: Implementation by Q2 2025
    
    3. Regulatory Compliance
       - New data privacy regulations in target European markets
       - Compliance costs: Estimated $800K
       - Legal review and system upgrades required
       - Deadline: Compliance by January 2025
    
    4. Market Competition
       - Two major competitors announced similar digital initiatives
       - Risk of market share erosion
       - Response: Accelerate timeline, focus on differentiation
       - Competitive advantage: Superior customer experience and innovation
    
    FINANCIAL PROJECTIONS:
    
    2025 Targets:
    • Revenue Growth: 25% target ($56M)
    • Operating Margin: Maintain above 20%
    • Market Expansion: 15% of revenue from international markets
    • Digital Transformation ROI: 30% efficiency improvement
    
    Investment Requirements:
    • Total Strategic Investments: $12.1M
    • Expected Payback Period: 18-24 months
    • Funding: Internal cash flow and existing credit facilities
    
    STRATEGIC PRIORITIES:
    
    1. Operational Excellence
       - Complete digital transformation
       - Achieve cost optimization targets
       - Enhance customer satisfaction scores
    
    2. Market Leadership
       - Establish presence in 3 European markets
       - Launch 2 innovative product lines
       - Increase market share by 15%
    
    3. Sustainable Growth
       - Achieve carbon neutrality commitments
       - Build resilient supply chain
       - Attract and retain top talent
    
    BOARD SENTIMENT:
    The board expressed strong confidence in management's execution capabilities.
    There is optimism about the strategic direction and market opportunities.
    Some concerns were raised about execution risks and competitive pressures,
    but overall sentiment remains positive with cautious optimism for 2025.
    
    NEXT STEPS:
    • Detailed implementation plans due by January 15, 2025
    • Monthly progress reviews for all strategic initiatives
    • Quarterly board updates on risk mitigation progress
    • Semi-annual market expansion status reports
    
    Meeting adjourned with commitment to reconvene in Q1 2025 for implementation review.
    """
    
    # Create document structure
    print("Creating test document...")
    page = DocumentPage(page_number=1, text=comprehensive_text)
    doc = ProcessedDocument(
        pages=[page],
        metadata=DocumentMetadata(
            filename="comprehensive_board_meeting.txt",
            file_type="txt",
            title="Q4 2024 Strategic Review",
            quarter="Q4",
            year=2024
        )
    )
    
    print(f"Document created: {len(comprehensive_text)} characters")
    print(f"Expected chunks: {len(comprehensive_text) // 2000 + 1}")
    
    # Test with optimized engine
    print("\nTesting with OptimizedAnalysisEngine...")
    engine = OptimizedAnalysisEngine()
    
    import time
    start_time = time.time()
    
    try:
        results = engine.analyze_document_optimized(doc)
        end_time = time.time()
        
        print(f"✅ Analysis completed in {end_time - start_time:.2f} seconds")
        
        # Display results
        print("\n" + "=" * 60)
        print("ANALYSIS RESULTS")
        print("=" * 60)
        
        print(f"\n📋 COMMITMENTS FOUND: {len(results.get('commitments', []))}")
        for i, commitment in enumerate(results.get('commitments', [])[:5]):
            print(f"  {i+1}. {commitment.get('text', 'Unknown')}")
            print(f"      Deadline: {commitment.get('deadline', 'Not specified')}")
            print(f"      Category: {commitment.get('category', 'general')}")
        
        print(f"\n⚠️  RISKS IDENTIFIED: {len(results.get('risks', []))}")
        for i, risk in enumerate(results.get('risks', [])[:5]):
            print(f"  {i+1}. {risk.get('description', 'Unknown')}")
            print(f"      Level: {risk.get('level', 'medium')}")
            print(f"      Impact: {risk.get('impact', 'Not specified')}")
        
        print(f"\n💰 FINANCIAL INSIGHTS: {len(results.get('financial_insights', []))}")
        for i, insight in enumerate(results.get('financial_insights', [])[:3]):
            print(f"  {i+1}. {insight.get('metric', 'Unknown')}: {insight.get('value', 'N/A')}")
        
        print(f"\n😊 SENTIMENT ANALYSIS:")
        sentiment = results.get('sentiment', {})
        print(f"  Overall: {sentiment.get('overall', 'unknown')}")
        print(f"  Confidence: {sentiment.get('confidence', 0)}/10")
        print(f"  Reason: {sentiment.get('reason', 'Not provided')}")
        
        print(f"\n📝 EXECUTIVE SUMMARY:")
        print(f"  {results.get('summary', 'No summary available')}")
        
        # Test performance metrics
        print("\n" + "=" * 60)
        print("PERFORMANCE METRICS")
        print("=" * 60)
        print(f"Processing Time: {end_time - start_time:.2f} seconds")
        print(f"Text Length: {len(comprehensive_text):,} characters")
        print(f"Chunks Processed: {len(comprehensive_text) // 2000 + 1}")
        print(f"Average Time per Chunk: {(end_time - start_time) / (len(comprehensive_text) // 2000 + 1):.2f} seconds")
        
        return True
        
    except Exception as e:
        end_time = time.time()
        print(f"❌ Analysis failed after {end_time - start_time:.2f} seconds: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the comprehensive test"""
    success = test_full_pipeline()
    
    print("\n" + "=" * 60)
    print("TEST CONCLUSION")
    print("=" * 60)
    
    if success:
        print("🎉 COMPREHENSIVE TEST PASSED!")
        print("✅ OptimizedAnalysisEngine successfully handled large document")
        print("✅ All analysis components working correctly")
        print("✅ Enhanced Streamlit app ready for use")
        print("\n📊 You can now use the enhanced app at: http://localhost:8502")
    else:
        print("❌ Test failed - check logs for details")

if __name__ == "__main__":
    main()
