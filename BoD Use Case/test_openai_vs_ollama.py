#!/usr/bin/env python3
"""
Comprehensive comparison test: OpenAI vs Ollama
"""

from dotenv import load_dotenv
import os
import time
import json

load_dotenv()

from src.utils.enhanced_analysis_engine import EnhancedAnalysisEngine
from src.utils.optimized_analysis_engine import OptimizedAnalysisEngine
from src.models.document import ProcessedDocument, DocumentMetadata, DocumentPage

def create_test_document():
    """Create a comprehensive test document for comparison"""
    test_text = """
    Board of Directors Meeting - Q1 2024 Strategic Review
    
    FINANCIAL PERFORMANCE:
    • Revenue increased 18% year-over-year to $4.2M
    • Operating margin improved from 12% to 16%
    • Cash flow positive for the third consecutive quarter
    • R&D spending increased to $800K (19% of revenue)
    
    STRATEGIC COMMITMENTS:
    • We will launch the new AI-powered product suite by September 2024
    • Committed to achieving 25% cost reduction in operations by Q4 2024
    • Plan to expand into European markets within 12 months
    • Board approved $2.5M investment in digital transformation
    
    RISK ASSESSMENT:
    • High risk: Increased competition from Tech Giant Corp
    • Medium risk: Supply chain disruptions affecting delivery timelines
    • Low risk: Regulatory changes in data privacy laws
    • Critical risk: Key talent retention challenges in engineering
    
    SENTIMENT INDICATORS:
    • Board expressed strong confidence in leadership team
    • Concerns raised about market saturation in core segments
    • Optimistic outlook for international expansion
    • Cautious approach recommended for cryptocurrency investments
    
    STRATEGIC PRIORITIES:
    • Priority 1: Complete product development by August 2024
    • Priority 2: Establish partnerships with 3 major distributors
    • Priority 3: Achieve SOC 2 compliance certification
    • Priority 4: Build engineering team from 15 to 25 people
    """
    
    metadata = DocumentMetadata(
        filename='board_meeting_q1_2024.txt',
        file_type='txt',
        total_pages=1,
        word_count=len(test_text.split())
    )
    page = DocumentPage(page_number=1, text=test_text)
    return ProcessedDocument(pages=[page], metadata=metadata, full_text=test_text)

def test_provider(provider_name, document):
    """Test a specific provider and return results"""
    print(f"\n🔍 Testing {provider_name.upper()}")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        if provider_name.lower() == "ollama":
            engine = OptimizedAnalysisEngine()
            results = engine.analyze_document_optimized(document, provider_name)
        else:
            engine = EnhancedAnalysisEngine()
            results = engine.analyze_document_enhanced(document, provider_name)
        
        processing_time = time.time() - start_time
        
        print(f"✅ Analysis completed in {processing_time:.2f} seconds")
        
        # Extract and display results
        commitments = results.get('enhanced_commitments', results.get('commitments', []))
        risks = results.get('risk_assessment', results.get('risks', []))
        financial = results.get('financial_insights', results.get('financial_metrics', []))
        sentiment = results.get('enhanced_sentiment', results.get('sentiment', {}))
        priorities = results.get('strategic_priorities', [])
        
        print(f"📊 Results Summary:")
        print(f"   • Commitments found: {len(commitments)}")
        print(f"   • Risks identified: {len(risks)}")
        print(f"   • Financial insights: {len(financial)}")
        print(f"   • Strategic priorities: {len(priorities)}")
        print(f"   • Processing time: {processing_time:.2f}s")
        
        if isinstance(sentiment, dict):
            sentiment_score = sentiment.get('overall_sentiment', sentiment.get('sentiment', 'unknown'))
            confidence = sentiment.get('confidence', 'N/A')
            print(f"   • Sentiment: {sentiment_score} (confidence: {confidence})")
        else:
            print(f"   • Sentiment: {sentiment}")
        
        # Show sample results
        if commitments:
            print(f"\n📋 Sample Commitments:")
            for i, commitment in enumerate(commitments[:3], 1):
                if isinstance(commitment, dict):
                    text = commitment.get('commitment', commitment.get('text', str(commitment)))
                    confidence = commitment.get('confidence', 'N/A')
                    print(f"   {i}. {text} (confidence: {confidence})")
                else:
                    print(f"   {i}. {commitment}")
        
        if risks:
            print(f"\n⚠️ Sample Risks:")
            for i, risk in enumerate(risks[:3], 1):
                if isinstance(risk, dict):
                    text = risk.get('risk', risk.get('description', str(risk)))
                    impact = risk.get('impact', 'N/A')
                    print(f"   {i}. {text} (impact: {impact})")
                else:
                    print(f"   {i}. {risk}")
        
        if financial:
            print(f"\n💰 Sample Financial Insights:")
            for i, insight in enumerate(financial[:3], 1):
                if isinstance(insight, dict):
                    metric = insight.get('metric_type', insight.get('metric', str(insight)))
                    value = insight.get('current_value', insight.get('value', 'N/A'))
                    print(f"   {i}. {metric}: {value}")
                else:
                    print(f"   {i}. {insight}")
        
        return {
            'provider': provider_name,
            'processing_time': processing_time,
            'commitments_count': len(commitments),
            'risks_count': len(risks),
            'financial_count': len(financial),
            'priorities_count': len(priorities),
            'sentiment': sentiment,
            'success': True,
            'sample_commitments': commitments[:3] if commitments else [],
            'sample_risks': risks[:3] if risks else []
        }
        
    except Exception as e:
        processing_time = time.time() - start_time
        print(f"❌ Error: {str(e)}")
        return {
            'provider': provider_name,
            'processing_time': processing_time,
            'success': False,
            'error': str(e)
        }

def compare_results(results):
    """Compare and display results from different providers"""
    print(f"\n📊 COMPREHENSIVE COMPARISON")
    print("=" * 60)
    
    successful_results = [r for r in results if r['success']]
    
    if len(successful_results) < 2:
        print("⚠️ Need at least 2 successful results for comparison")
        return
    
    print(f"{'Metric':<25} {'OpenAI':<15} {'Ollama':<15} {'Winner':<10}")
    print("-" * 65)
    
    openai_result = next((r for r in successful_results if r['provider'] == 'openai'), None)
    ollama_result = next((r for r in successful_results if r['provider'] == 'ollama'), None)
    
    if openai_result and ollama_result:
        # Processing time comparison
        faster = "OpenAI" if openai_result['processing_time'] < ollama_result['processing_time'] else "Ollama"
        print(f"{'Processing Time (s)':<25} {openai_result['processing_time']:<15.2f} {ollama_result['processing_time']:<15.2f} {faster:<10}")
        
        # Content detection comparison
        metrics = ['commitments_count', 'risks_count', 'financial_count', 'priorities_count']
        metric_names = ['Commitments', 'Risks', 'Financial Items', 'Priorities']
        
        for metric, name in zip(metrics, metric_names):
            openai_val = openai_result.get(metric, 0)
            ollama_val = ollama_result.get(metric, 0)
            winner = "OpenAI" if openai_val > ollama_val else "Ollama" if ollama_val > openai_val else "Tie"
            print(f"{name:<25} {openai_val:<15} {ollama_val:<15} {winner:<10}")
    
    print(f"\n🏆 ANALYSIS QUALITY COMPARISON:")
    
    if openai_result:
        print(f"\n🌐 OpenAI (GPT-3.5-turbo):")
        print(f"   • Cost: ~$0.001-0.01 per analysis")
        print(f"   • Speed: {openai_result['processing_time']:.1f}s")
        print(f"   • Strengths: Advanced reasoning, detailed analysis")
        
    if ollama_result:
        print(f"\n🏠 Ollama (llama3.2:3b):")
        print(f"   • Cost: Free")
        print(f"   • Speed: {ollama_result['processing_time']:.1f}s") 
        print(f"   • Strengths: Privacy, no API limits, offline capable")

def main():
    """Main comparison test"""
    print("🎯 OPENAI vs OLLAMA COMPREHENSIVE COMPARISON")
    print("=" * 60)
    print("Testing both providers with identical board presentation content...")
    
    # Create test document
    document = create_test_document()
    print(f"📄 Test document: {document.metadata.word_count} words")
    
    # Test both providers
    results = []
    
    # Test OpenAI
    results.append(test_provider("openai", document))
    
    # Test Ollama
    results.append(test_provider("ollama", document))
    
    # Compare results
    compare_results(results)
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    print(f"   🎯 For Production Use:")
    print(f"      • Ollama: Best for cost-conscious deployments")
    print(f"      • OpenAI: Best for maximum accuracy and detail")
    print(f"   📊 For Board Analysis:")
    print(f"      • Both providers deliver excellent results")
    print(f"      • Ollama recommended for regular/batch processing")
    print(f"      • OpenAI recommended for critical/complex documents")

if __name__ == "__main__":
    main()
