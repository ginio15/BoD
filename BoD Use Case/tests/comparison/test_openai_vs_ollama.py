#!/usr/bin/env python3
"""
Comprehensive comparison between OpenAI and Ollama providers
"""

import sys
import time
import json
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Load .env file from project root
from dotenv import load_dotenv
load_dotenv(project_root / '.env')

from src.utils.optimized_analysis_engine import OptimizedAnalysisEngine
from src.utils.enhanced_analysis_engine import EnhancedAnalysisEngine
from src.models.document import ProcessedDocument, DocumentMetadata, DocumentPage
from src.utils.llm_providers import LLMProviderManager

def create_comprehensive_test_document():
    """Create a comprehensive test document"""
    # Read actual test document if available
    test_doc_path = project_root / 'data' / 'test_documents' / 'comprehensive_test_document.txt'
    
    if test_doc_path.exists():
        with open(test_doc_path, 'r', encoding='utf-8') as f:
            sample_text = f.read()
        print(f"📄 Using test document: {test_doc_path.name}")
    else:
        # Fallback to sample text
        sample_text = """
        BOARD OF DIRECTORS QUARTERLY MEETING - Q1 2024 STRATEGIC REVIEW
        
        EXECUTIVE SUMMARY:
        The first quarter of 2024 has demonstrated remarkable progress across all strategic initiatives. 
        Our revenue growth of 28% year-over-year has exceeded projections, while operational efficiency 
        improvements have contributed to a 15% reduction in costs.
        
        FINANCIAL PERFORMANCE:
        - Total revenue: $158M (up 28% YoY)
        - EBITDA: $42M (margin of 26.5%, up from 23.1%)
        - Net income: $28M (up 35% YoY)
        - Cash position: $78M (improved liquidity)
        - R&D investment: $15M (9.5% of revenue)
        
        STRATEGIC COMMITMENTS FOR 2024:
        1. Market Expansion: We commit to entering three new international markets by Q4 2024, with an initial investment of $12M
        2. Product Innovation: Launch of our AI-powered analytics platform by September 2024, targeting 20% market share within 18 months
        3. Operational Excellence: Achieve additional 10% cost reduction through process optimization by end of 2024
        4. Sustainability Goals: Reduce carbon footprint by 25% and achieve carbon-neutral operations by Q2 2025
        5. Team Development: Hire 150 additional employees across technical and commercial functions by December 2024
        6. Customer Experience: Improve Net Promoter Score from 67 to 80+ through enhanced service delivery
        
        RISK ASSESSMENT & MITIGATION:
        HIGH PRIORITY RISKS:
        - Supply chain disruptions in APAC region could impact Q3 delivery schedules (Mitigation: Diversified supplier base)
        - Regulatory changes in European markets may affect product compliance (Mitigation: Early engagement with regulators)
        - Cybersecurity threats requiring enhanced protection measures (Mitigation: $2M security infrastructure investment)
        
        MEDIUM PRIORITY RISKS:
        - Currency fluctuations affecting international revenue (Mitigation: Hedging strategies)
        - Competition from new market entrants (Mitigation: Accelerated innovation pipeline)
        - Talent acquisition challenges in key technical roles (Mitigation: Enhanced compensation packages)
        
        STRATEGIC PRIORITIES Q2-Q4 2024:
        1. Technology Leadership: Complete AI platform development and market launch
        2. Global Expansion: Establish operations in target international markets
        3. Operational Scaling: Build infrastructure to support 40% growth trajectory
        4. Partnership Development: Strategic alliances with key industry players
        5. Sustainability Implementation: Execute comprehensive ESG strategy
        
        BOARD SENTIMENT & OUTLOOK:
        The board expresses strong confidence in management's execution capabilities and the company's 
        strategic direction. While acknowledging market uncertainties, the focus remains on sustainable 
        growth, operational excellence, and stakeholder value creation. The unanimous decision to 
        accelerate international expansion reflects our commitment to market leadership.
        """
        print("📄 Using fallback sample document")
    
    metadata = DocumentMetadata(
        filename="comprehensive_test.txt",
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

def comprehensive_analysis_comparison():
    """Run comprehensive comparison between OpenAI and Ollama"""
    print("🧪 Comprehensive OpenAI vs Ollama Comparison")
    print("=" * 60)
    
    # Check available providers
    manager = LLMProviderManager()
    available_providers = manager.get_available_providers()
    
    print(f"Available providers: {available_providers}")
    
    # Create test document
    test_doc = create_comprehensive_test_document()
    print(f"Document length: {len(test_doc.full_text):,} characters")
    print(f"Word count: {test_doc.metadata.word_count:,} words")
    
    # Test configurations
    test_configs = []
    
    if "openai" in available_providers:
        test_configs.append({
            "name": "OpenAI (Enhanced)",
            "provider": "openai",
            "engine_class": EnhancedAnalysisEngine,
            "method": "analyze_document_enhanced"
        })
        test_configs.append({
            "name": "OpenAI (Optimized)",
            "provider": "openai", 
            "engine_class": OptimizedAnalysisEngine,
            "method": "analyze_document_optimized"
        })
    
    if "ollama" in available_providers:
        test_configs.append({
            "name": "Ollama (Optimized)",
            "provider": "ollama",
            "engine_class": OptimizedAnalysisEngine,
            "method": "analyze_document_optimized"
        })
    
    if not test_configs:
        print("❌ No providers available for testing")
        return False
    
    results = {}
    
    # Run tests
    for config in test_configs:
        print(f"\n🔍 Testing {config['name']}...")
        print("-" * 40)
        
        try:
            engine = config['engine_class']()
            method = getattr(engine, config['method'])
            
            start_time = time.time()
            analysis_results = method(test_doc, provider=config['provider'])
            end_time = time.time()
            
            duration = end_time - start_time
            
            # Extract metrics
            commitments = analysis_results.get('enhanced_commitments', analysis_results.get('commitments', []))
            risks = analysis_results.get('risk_assessment', analysis_results.get('risks', []))
            financial = analysis_results.get('financial_insights', [])
            sentiment = analysis_results.get('sentiment_analysis', analysis_results.get('sentiment', {}))
            priorities = analysis_results.get('strategic_priorities', [])
            
            results[config['name']] = {
                "duration": duration,
                "success": True,
                "metrics": {
                    "commitments": len(commitments),
                    "risks": len(risks),
                    "financial": len(financial),
                    "strategic_priorities": len(priorities),
                    "has_sentiment": bool(sentiment),
                    "has_executive_summary": bool(analysis_results.get('executive_summary'))
                },
                "sample_data": {
                    "first_commitment": commitments[0] if commitments else None,
                    "first_risk": risks[0] if risks else None,
                    "sentiment_overall": sentiment.get('overall', 'N/A') if sentiment else 'N/A'
                }
            }
            
            print(f"✅ Completed in {duration:.1f} seconds")
            print(f"   Commitments: {results[config['name']]['metrics']['commitments']}")
            print(f"   Risks: {results[config['name']]['metrics']['risks']}")
            print(f"   Financial insights: {results[config['name']]['metrics']['financial']}")
            print(f"   Strategic priorities: {results[config['name']]['metrics']['strategic_priorities']}")
            print(f"   Sentiment: {results[config['name']]['sample_data']['sentiment_overall']}")
            
        except Exception as e:
            print(f"❌ Failed: {e}")
            results[config['name']] = {
                "duration": 0,
                "success": False,
                "error": str(e)
            }
    
    # Display detailed comparison
    print(f"\n📊 DETAILED COMPARISON RESULTS")
    print("=" * 60)
    
    successful_tests = [name for name, result in results.items() if result['success']]
    
    if len(successful_tests) >= 2:
        print("⚡ Performance Comparison:")
        for name in successful_tests:
            result = results[name]
            print(f"   {name:20}: {result['duration']:6.1f}s")
        
        print("\n🎯 Quality Metrics Comparison:")
        print(f"{'Provider':20} {'Commits':8} {'Risks':6} {'Financial':9} {'Strategic':9} {'Sentiment':9}")
        print("-" * 70)
        for name in successful_tests:
            metrics = results[name]['metrics']
            sentiment_status = "✅" if metrics['has_sentiment'] else "❌"
            print(f"{name:20} {metrics['commitments']:7} {metrics['risks']:5} {metrics['financial']:8} {metrics['strategic_priorities']:8} {sentiment_status:8}")
        
        # Detailed analysis samples
        print("\n📋 Sample Analysis Quality:")
        for name in successful_tests:
            result = results[name]
            sample = result['sample_data']
            print(f"\n{name}:")
            if sample['first_commitment']:
                commitment_text = sample['first_commitment'].get('text', sample['first_commitment'].get('exact_text', 'N/A'))
                print(f"   First commitment: {commitment_text[:80]}...")
            if sample['first_risk']:
                risk_text = sample['first_risk'].get('description', sample['first_risk'].get('text', 'N/A'))
                print(f"   First risk: {risk_text[:80]}...")
        
        # Recommendations
        print(f"\n🏆 RECOMMENDATIONS:")
        fastest = min(successful_tests, key=lambda p: results[p]['duration'])
        most_comprehensive = max(successful_tests, 
                               key=lambda p: sum(results[p]['metrics'][k] for k in ['commitments', 'risks', 'financial']))
        
        print(f"   Fastest: {fastest} ({results[fastest]['duration']:.1f}s)")
        print(f"   Most comprehensive: {most_comprehensive}")
        
        if "Ollama (Optimized)" in successful_tests:
            print(f"   💰 Cost-effective: Ollama (Optimized) - Free local processing")
        
    elif len(successful_tests) == 1:
        provider = successful_tests[0]
        print(f"✅ Only {provider} available and working")
        print(f"   Duration: {results[provider]['duration']:.1f}s")
        print(f"   Quality metrics: {results[provider]['metrics']}")
    else:
        print("❌ No successful analyses")
        return False
    
    # Save results to file
    results_file = project_root / 'comparison_results.json'
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n💾 Results saved to: {results_file}")
    
    return True

def main():
    """Main comparison function"""
    print("🚀 OpenAI vs Ollama Comprehensive Comparison")
    print("=" * 60)
    
    success = comprehensive_analysis_comparison()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Comprehensive comparison completed successfully!")
        print("   Review the detailed results above to choose the best provider for your needs")
    else:
        print("❌ Comprehensive comparison failed")
    print("=" * 60)

if __name__ == "__main__":
    main()