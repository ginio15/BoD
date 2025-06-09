#!/usr/bin/env python3
"""
Enhanced Board Analysis with Ollama Integration
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.utils.llm_providers import LLMProviderManager
from src.utils.analysis_engine import AnalysisEngine
import time

def test_enhanced_commitment_analysis():
    """Test enhanced commitment analysis with Ollama"""
    print("🔍 Testing Enhanced Commitment Analysis with Ollama")
    
    # Sample board presentation text
    board_text = """
    Board Meeting Minutes - Q4 2023 Strategic Review
    
    FINANCIAL PERFORMANCE:
    - Q4 revenue reached $2.5M (15% YoY growth)
    - Net profit margin improved to 12%
    - Cash flow positive for 3rd consecutive quarter
    
    STRATEGIC COMMITMENTS FOR 2024:
    1. Cost Optimization: We will reduce operational expenses by 10% by Q2 2024
    2. Product Launch: Committed to launching new AI-powered analytics platform in Q3 2024
    3. Market Expansion: Target European market entry by December 2024 with $500K investment
    4. Customer Success: Improve customer satisfaction scores from 75% to 85% by end of 2024
    5. Team Growth: Plan to hire 15 additional engineers by September 2024
    
    RISK ASSESSMENT:
    - High: Supply chain disruptions may impact Q1 delivery schedules
    - Medium: Currency fluctuations could affect European expansion costs
    - Low: Regulatory changes in data privacy laws
    
    FINANCIAL PROJECTIONS:
    - Q1 2024: Target revenue of $2.8M
    - Full year 2024: Projecting 20% revenue growth to $12M
    - R&D investment: Increase to 15% of revenue
    
    BOARD SENTIMENT:
    The board expressed cautious optimism about 2024 growth prospects while acknowledging 
    the need for careful risk management and operational excellence.
    """
    
    manager = LLMProviderManager()
    
    # Enhanced commitment extraction prompt
    commitment_prompt = f"""
    You are an expert board analyst. Analyze this board presentation and extract detailed commitment information.
    
    TEXT TO ANALYZE:
    {board_text}
    
    TASK: Extract and categorize all commitments with the following details:
    
    1. COMMITMENT DETAILS:
       - Exact commitment statement
       - Target deadline/timeframe
       - Quantifiable metrics (percentages, amounts, etc.)
       - Confidence level (High/Medium/Low based on language used)
       - Category (Financial/Operational/Strategic/HR)
    
    2. RISK ASSESSMENT:
       - Associated risks mentioned
       - Risk level (High/Medium/Low)
       - Potential impact on commitments
    
    3. FINANCIAL IMPLICATIONS:
       - Budget allocations mentioned
       - Revenue targets
       - Cost reduction goals
    
    FORMAT: Provide structured analysis in clear sections. Be specific and quantitative where possible.
    """
    
    print("Generating enhanced commitment analysis...")
    start_time = time.time()
    
    response = manager.generate_response(
        commitment_prompt, 
        provider="ollama", 
        model="llama3.2:3b",
        temperature=0.1
    )
    
    if response.error:
        print(f"❌ Error: {response.error}")
        return
    
    print(f"✅ Analysis completed in {time.time() - start_time:.1f} seconds")
    print(f"📄 Response ({len(response.content)} characters):")
    print("=" * 80)
    print(response.content)
    print("=" * 80)
    
    return response

def test_sentiment_and_risk_analysis():
    """Test advanced sentiment and risk analysis"""
    print("\n🎯 Testing Advanced Sentiment & Risk Analysis")
    
    board_text = """
    Executive Summary - Q4 2023 Board Review
    
    PERFORMANCE HIGHLIGHTS:
    Despite challenging market conditions, we exceeded revenue targets by 8%. 
    Customer retention improved significantly to 92%, and our new product line 
    showed promising early adoption rates.
    
    CONCERNS AND CHALLENGES:
    However, we face several headwinds: rising operational costs, increased 
    competition in key markets, and potential economic recession impacts. 
    The recent supply chain disruptions cost us approximately $200K in Q4.
    
    STRATEGIC OUTLOOK:
    We remain optimistic about our long-term prospects but acknowledge the need 
    for more aggressive cost management. The board has approved a comprehensive 
    restructuring plan that may result in workforce reductions.
    
    FINANCIAL POSITION:
    While cash flow remains positive, we're concerned about declining margins. 
    The board is considering additional funding options to support growth initiatives.
    """
    
    sentiment_prompt = f"""
    Perform comprehensive sentiment and risk analysis on this board presentation:
    
    TEXT: {board_text}
    
    ANALYSIS REQUIRED:
    
    1. OVERALL SENTIMENT ANALYSIS:
       - Primary sentiment (Positive/Negative/Mixed/Neutral)
       - Confidence score (1-10)
       - Key sentiment indicators and phrases
       - Tone evolution throughout the text
    
    2. RISK ASSESSMENT:
       - Identify all mentioned risks
       - Categorize risk levels (High/Medium/Low)
       - Assess potential business impact
       - Risk interconnections and compound effects
    
    3. LEADERSHIP CONFIDENCE:
       - Board confidence level in strategy
       - Areas of uncertainty or concern
       - Decision-making tone (decisive/hesitant/conflicted)
    
    4. FINANCIAL HEALTH INDICATORS:
       - Financial stability signals
       - Cash flow concerns
       - Investment capacity assessment
    
    Provide detailed, actionable insights that a board member would find valuable.
    """
    
    manager = LLMProviderManager()
    
    print("Generating sentiment and risk analysis...")
    start_time = time.time()
    
    response = manager.generate_response(
        sentiment_prompt,
        provider="ollama", 
        model="llama3.2:3b",
        temperature=0.1
    )
    
    if response.error:
        print(f"❌ Error: {response.error}")
        return
    
    print(f"✅ Analysis completed in {time.time() - start_time:.1f} seconds")
    print(f"📊 Sentiment & Risk Analysis ({len(response.content)} characters):")
    print("=" * 80)
    print(response.content)
    print("=" * 80)
    
    return response

def main():
    """Run enhanced analysis tests"""
    print("🚀 Enhanced BoD Analysis System - Ollama Integration Test")
    print("=" * 80)
    
    # Test 1: Enhanced Commitment Analysis
    commitment_response = test_enhanced_commitment_analysis()
    
    # Test 2: Sentiment and Risk Analysis
    sentiment_response = test_sentiment_and_risk_analysis()
    
    # Summary
    print("\n📈 TEST SUMMARY")
    print("=" * 40)
    if commitment_response and not commitment_response.error:
        print("✅ Enhanced Commitment Analysis: PASSED")
        print(f"   Response time: {commitment_response.response_time:.1f}s")
        print(f"   Content length: {len(commitment_response.content)} chars")
    else:
        print("❌ Enhanced Commitment Analysis: FAILED")
    
    if sentiment_response and not sentiment_response.error:
        print("✅ Sentiment & Risk Analysis: PASSED")
        print(f"   Response time: {sentiment_response.response_time:.1f}s")
        print(f"   Content length: {len(sentiment_response.content)} chars")
    else:
        print("❌ Sentiment & Risk Analysis: FAILED")
    
    # Usage statistics
    manager = LLMProviderManager()
    usage = manager.get_usage_summary()
    print(f"\n💰 Ollama Usage Statistics:")
    ollama_stats = usage.get("providers", {}).get("ollama", {})
    print(f"   Total requests: {ollama_stats.get('request_count', 0)}")
    print(f"   Total tokens: {ollama_stats.get('total_tokens', 0)}")
    print(f"   Error count: {ollama_stats.get('error_count', 0)}")
    print(f"   Cost: ${ollama_stats.get('total_cost', 0):.2f} (Free!)")

if __name__ == "__main__":
    main()
