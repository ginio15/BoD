#!/usr/bin/env python3
"""
Comprehensive test of Enhanced BoD Analysis Engine with Ollama
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.utils.enhanced_analysis_engine import EnhancedAnalysisEngine
from src.models.document import ProcessedDocument, DocumentMetadata, DocumentPage
from datetime import datetime
import json
import time

def create_sample_document():
    """Create a sample board presentation document for testing"""
    
    # Sample comprehensive board presentation content
    presentation_content = """
    BOARD OF DIRECTORS MEETING MINUTES
    Q4 2023 Strategic Review and 2024 Planning Session
    Date: December 15, 2023
    
    EXECUTIVE SUMMARY
    The board convened to review Q4 2023 performance and establish strategic direction for 2024. 
    Despite challenging market conditions, the company achieved strong financial results and is 
    well-positioned for growth. However, several risks require immediate attention.
    
    FINANCIAL PERFORMANCE
    
    Q4 2023 Results:
    - Revenue: $2.5M (15% YoY growth, exceeding target of $2.3M)
    - Net profit margin: 12% (improved from 8% in Q4 2022)
    - Cash flow: Positive $400K (3rd consecutive quarter of positive cash flow)
    - Operating expenses: $1.8M (5% increase from Q4 2022)
    
    Full Year 2023 Performance:
    - Total revenue: $9.2M (22% YoY growth)
    - EBITDA: $1.1M (EBITDA margin of 12%)
    - Customer acquisition cost decreased by 20%
    - Customer retention rate improved to 92%
    
    STRATEGIC COMMITMENTS FOR 2024
    
    1. FINANCIAL TARGETS
    - We will achieve $12M in revenue for 2024 (30% growth target)
    - Committed to reducing operational costs by 10% by Q2 2024 through process optimization
    - Target EBITDA margin improvement to 15% by year-end 2024
    - Plan to maintain positive cash flow throughout 2024
    
    2. PRODUCT AND MARKET EXPANSION
    - Launch new AI-powered analytics platform by Q3 2024 with $500K development budget
    - Enter European markets by December 2024, targeting €1M in revenue
    - Complete acquisition of competitor XYZ Corp by Q2 2024 for $2M
    - Establish partnerships with 3 major distributors by September 2024
    
    3. OPERATIONAL EXCELLENCE
    - Improve customer satisfaction scores from 75% to 85% by end of 2024
    - Reduce customer support response time to under 2 hours by Q3 2024
    - Implement ISO 27001 security certification by Q4 2024
    - Achieve 99.9% system uptime throughout 2024
    
    4. HUMAN RESOURCES
    - Hire 15 additional engineers by September 2024 (current team: 25)
    - Implement new performance management system by Q2 2024
    - Reduce employee turnover rate to below 10% (currently 15%)
    - Launch leadership development program for senior staff by Q3 2024
    
    RISK ASSESSMENT
    
    HIGH PRIORITY RISKS:
    1. Supply Chain Disruptions: Recent supplier delays cost $200K in Q4. May impact Q1 2024 
       delivery schedules and customer commitments. Mitigation: Diversify supplier base.
    
    2. Cybersecurity Threats: Increased phishing attempts and industry-wide security breaches. 
       Potential impact: $1M+ in damages, regulatory fines, customer trust loss.
       Mitigation: Accelerate ISO 27001 implementation, additional security training.
    
    3. Economic Recession: 70% probability of recession in 2024 according to industry analysts.
       Impact: 15-20% revenue decline, delayed customer payments, budget cuts.
       
    MEDIUM PRIORITY RISKS:
    1. Key Personnel Departure: CTO considering external opportunities. Loss would delay 
       product development by 3-6 months.
    
    2. Currency Fluctuations: European expansion exposed to EUR/USD volatility. 
       Potential 5-10% impact on international revenue.
    
    3. Regulatory Changes: New data privacy regulations in EU may require $100K compliance investment.
    
    LOW PRIORITY RISKS:
    1. Office Lease Renewal: Current lease expires December 2024. Market rates increased 15%.
    2. Equipment Obsolescence: Some servers need replacement within 18 months.
    
    COMPETITIVE LANDSCAPE
    Main competitor ABC Inc launched similar product in Q4 2023 with aggressive pricing.
    Our analysis shows their solution lacks advanced features, but their 20% price advantage
    is concerning. We must accelerate our product roadmap to maintain market leadership.
    
    INVESTMENT AND FUNDING
    - Board approved $3M investment in R&D for 2024
    - Considering Series B funding round of $10M in Q3 2024
    - Current cash reserves: $2.1M (6 months operating expenses)
    - Approved emergency credit line of $1M with First National Bank
    
    STAKEHOLDER UPDATES
    
    Customers: Overall satisfaction remains high at 8.2/10. Key accounts (representing 40% of revenue) 
    renewed contracts with average 12% rate increases. Three enterprise prospects in final 
    negotiation stages for Q1 2024 deals worth $600K combined.
    
    Employees: Annual survey shows 78% satisfaction (target: 85%). Main concerns: work-life balance 
    and career development opportunities. HR implementing flexible work policy and mentorship program.
    
    Shareholders: Quarterly investor call scheduled for January 15, 2024. Key message: strong 
    growth trajectory despite market headwinds. Dividend payment of $0.50 per share approved 
    for Q1 2024.
    
    Partners: Strategic alliance with TechCorp performing well, contributing 15% of Q4 revenue. 
    Exploring similar partnerships with 2 additional firms in adjacent markets.
    
    BOARD DECISIONS AND ACTIONS
    
    UNANIMOUS DECISIONS:
    1. Approve 2024 budget of $10.5M with 30% allocated to growth initiatives
    2. Authorize CEO to proceed with XYZ Corp acquisition negotiations
    3. Establish board-level cybersecurity committee (quarterly meetings)
    4. Approve stock option pool expansion for employee retention
    
    MAJORITY DECISIONS (1 dissent):
    1. European expansion timeline (dissent: too aggressive given economic uncertainty)
    2. Series B funding timing (dissent: prefer waiting until Q4 2024)
    
    ACTION ITEMS:
    - CEO: Present detailed acquisition proposal by January 31, 2024
    - CFO: Develop scenario planning for recession impact by February 15, 2024
    - CTO: Finalize AI platform development timeline by January 15, 2024
    - CHRO: Implement retention strategies for key personnel by March 1, 2024
    
    NEXT BOARD MEETING: February 20, 2024
    Focus: Q1 2024 performance review and acquisition update
    
    MEETING SENTIMENT SUMMARY
    The board expressed cautious optimism about 2024 prospects. While financial performance 
    exceeded expectations, members emphasized the need for careful risk management and 
    contingency planning. There is strong confidence in the management team's ability to 
    execute the strategic plan, though some concern about aggressive growth targets in 
    an uncertain economic environment.
    
    The tone was professional and forward-looking, with robust discussion on risk mitigation 
    strategies. Board members appreciated the transparent presentation of challenges alongside 
    achievements. Overall assessment: well-positioned for growth with appropriate risk awareness.
    """
    
    # Create document object
    metadata = DocumentMetadata(
        filename="Q4_2023_Board_Minutes.txt",
        file_type="txt",
        total_pages=1
    )
    
    page_content = DocumentPage(
        page_number=1,
        text=presentation_content
    )
    
    document = ProcessedDocument(
        metadata=metadata,
        pages=[page_content],
        full_text=presentation_content
    )
    
    return document

def test_comprehensive_analysis():
    """Test the comprehensive enhanced analysis"""
    print("🚀 COMPREHENSIVE ENHANCED BOD ANALYSIS TEST")
    print("=" * 80)
    
    # Create enhanced analysis engine
    engine = EnhancedAnalysisEngine()
    
    # Create sample document
    print("📄 Creating sample board presentation document...")
    document = create_sample_document()
    print(f"   Document length: {len(document.full_text):,} characters")
    
    # Run comprehensive analysis
    print("\n🔍 Running comprehensive analysis with Ollama...")
    start_time = time.time()
    
    analysis_results = engine.analyze_document_enhanced(document, provider="ollama")
    
    analysis_time = time.time() - start_time
    print(f"✅ Analysis completed in {analysis_time:.1f} seconds")
    
    # Display results
    print("\n📊 ANALYSIS RESULTS SUMMARY")
    print("=" * 50)
    
    # Commitments
    commitments = analysis_results.get("enhanced_commitments", [])
    print(f"🎯 Enhanced Commitments: {len(commitments)}")
    if commitments:
        print("   Categories found:")
        categories = {}
        for commitment in commitments:
            cat = commitment.get("category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1
        for cat, count in categories.items():
            print(f"     • {cat}: {count}")
    
    # Risks
    risks = analysis_results.get("risk_assessment", [])
    print(f"\n⚠️  Risk Assessment: {len(risks)} risks identified")
    if risks:
        risk_levels = {}
        for risk in risks:
            level = risk.get("risk_level", "unknown")
            risk_levels[level] = risk_levels.get(level, 0) + 1
        for level, count in risk_levels.items():
            print(f"     • {level} risk: {count}")
    
    # Financial insights
    financial = analysis_results.get("financial_insights", [])
    print(f"\n💰 Financial Insights: {len(financial)} metrics extracted")
    
    # Strategic priorities
    strategic = analysis_results.get("strategic_priorities", [])
    print(f"\n🎯 Strategic Priorities: {len(strategic)} priorities identified")
    
    # Sentiment analysis
    sentiment = analysis_results.get("sentiment_analysis", {})
    if sentiment:
        overall = sentiment.get("overall_sentiment", "unknown")
        confidence = sentiment.get("overall_confidence", "N/A")
        print(f"\n😊 Sentiment Analysis: {overall} (confidence: {confidence})")
    
    # Executive summary
    summary = analysis_results.get("executive_summary", "")
    print(f"\n📋 Executive Summary: {len(summary)} characters generated")
    
    return analysis_results, analysis_time

def display_detailed_results(analysis_results):
    """Display detailed analysis results"""
    print("\n" + "="*80)
    print("📋 DETAILED ANALYSIS RESULTS")
    print("="*80)
    
    # Enhanced Commitments
    commitments = analysis_results.get("enhanced_commitments", [])
    if commitments:
        print(f"\n🎯 ENHANCED COMMITMENTS ({len(commitments)} found)")
        print("-" * 50)
        for i, commitment in enumerate(commitments[:5], 1):  # Show first 5
            print(f"{i}. Category: {commitment.get('category', 'N/A')}")
            print(f"   Text: {commitment.get('exact_text', 'N/A')[:100]}...")
            print(f"   Deadline: {commitment.get('deadline', 'N/A')}")
            print(f"   Confidence: {commitment.get('confidence_level', 'N/A')}")
            print(f"   Metric: {commitment.get('quantifiable_metric', 'N/A')}")
            print()
    
    # Risk Assessment
    risks = analysis_results.get("risk_assessment", [])
    if risks:
        print(f"\n⚠️  RISK ASSESSMENT ({len(risks)} risks identified)")
        print("-" * 50)
        for i, risk in enumerate(risks[:5], 1):  # Show first 5
            print(f"{i}. Risk Level: {risk.get('risk_level', 'N/A')}")
            print(f"   Category: {risk.get('category', 'N/A')}")
            print(f"   Description: {risk.get('risk_description', 'N/A')[:100]}...")
            print(f"   Impact: {risk.get('potential_impact', 'N/A')[:80]}...")
            print()
    
    # Financial Insights
    financial = analysis_results.get("financial_insights", [])
    if financial:
        print(f"\n💰 FINANCIAL INSIGHTS ({len(financial)} metrics)")
        print("-" * 50)
        for i, insight in enumerate(financial[:5], 1):  # Show first 5
            print(f"{i}. Metric: {insight.get('metric_type', 'N/A')}")
            print(f"   Current: {insight.get('current_value', 'N/A')}")
            print(f"   Target: {insight.get('target_value', 'N/A')}")
            print(f"   Trend: {insight.get('trend', 'N/A')}")
            print(f"   Significance: {insight.get('significance', 'N/A')}")
            print()
    
    # Executive Summary
    summary = analysis_results.get("executive_summary", "")
    if summary:
        print(f"\n📋 EXECUTIVE SUMMARY")
        print("-" * 50)
        print(summary[:500] + "..." if len(summary) > 500 else summary)
        print()

def main():
    """Run comprehensive enhanced analysis test"""
    try:
        # Run comprehensive analysis
        analysis_results, analysis_time = test_comprehensive_analysis()
        
        # Display detailed results
        display_detailed_results(analysis_results)
        
        # Performance summary
        print("\n" + "="*80)
        print("⚡ PERFORMANCE SUMMARY")
        print("="*80)
        print(f"Total analysis time: {analysis_time:.1f} seconds")
        print(f"Components analyzed:")
        print(f"  • Commitments: {len(analysis_results.get('enhanced_commitments', []))}")
        print(f"  • Risks: {len(analysis_results.get('risk_assessment', []))}")
        print(f"  • Financial insights: {len(analysis_results.get('financial_insights', []))}")
        print(f"  • Strategic priorities: {len(analysis_results.get('strategic_priorities', []))}")
        print(f"  • Sentiment analysis: {'✅' if analysis_results.get('sentiment_analysis') else '❌'}")
        print(f"  • Executive summary: {'✅' if analysis_results.get('executive_summary') else '❌'}")
        
        print(f"\n🎉 Enhanced BoD Analysis System with Ollama integration is working successfully!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
