#!/usr/bin/env python3
"""
Live OpenAI vs Ollama Comparison Test
"""

from dotenv import load_dotenv
import os
import time
import json
from datetime import datetime

load_dotenv()

from src.utils.enhanced_analysis_engine import EnhancedAnalysisEngine
from src.utils.optimized_analysis_engine import OptimizedAnalysisEngine
from src.models.document import ProcessedDocument, DocumentMetadata, DocumentPage

def create_test_document():
    """Load our standardized test document"""
    with open('test_comparison_document.txt', 'r') as f:
        test_text = f.read()
    
    metadata = DocumentMetadata(
        filename='board_meeting_q2_2024.txt',
        file_type='txt',
        total_pages=1,
        word_count=len(test_text.split())
    )
    page = DocumentPage(page_number=1, text=test_text)
    return ProcessedDocument(pages=[page], metadata=metadata, full_text=test_text)

def analyze_with_provider(provider_name, document):
    """Analyze document with specific provider"""
    print(f"\n🔍 TESTING {provider_name.upper()}")
    print("=" * 50)
    
    start_time = time.time()
    
    try:
        if provider_name.lower() == "ollama":
            print("📡 Using OptimizedAnalysisEngine for Ollama...")
            engine = OptimizedAnalysisEngine()
            results = engine.analyze_document_optimized(document, provider_name)
        else:
            print("📡 Using EnhancedAnalysisEngine for OpenAI...")
            engine = EnhancedAnalysisEngine()
            results = engine.analyze_document_enhanced(document, provider_name)
        
        processing_time = time.time() - start_time
        
        # Extract results based on provider type
        if provider_name.lower() == "ollama":
            # OptimizedAnalysisEngine results format
            commitments = results.get('commitments', [])
            risks = results.get('risks', [])
            financial = results.get('financial_metrics', [])
            sentiment = results.get('sentiment', 'unknown')
            summary = results.get('summary', '')
        else:
            # EnhancedAnalysisEngine results format
            commitments = results.get('enhanced_commitments', [])
            risks = results.get('risk_assessment', [])
            financial = results.get('financial_insights', [])
            sentiment = results.get('enhanced_sentiment', {})
            summary = results.get('executive_summary', {})
        
        print(f"✅ Analysis completed in {processing_time:.2f} seconds")
        print(f"\n📊 RESULTS SUMMARY:")
        print(f"   📋 Commitments found: {len(commitments)}")
        print(f"   ⚠️  Risks identified: {len(risks)}")
        print(f"   💰 Financial metrics: {len(financial)}")
        print(f"   ⏱️  Processing time: {processing_time:.2f}s")
        
        # Display sentiment
        if isinstance(sentiment, dict):
            sentiment_value = sentiment.get('overall_sentiment', sentiment.get('sentiment', 'unknown'))
            confidence = sentiment.get('confidence', 'N/A')
            print(f"   😊 Sentiment: {sentiment_value} (confidence: {confidence})")
        else:
            print(f"   😊 Sentiment: {sentiment}")
        
        # Show detailed results
        print(f"\n📋 DETAILED COMMITMENTS:")
        for i, commitment in enumerate(commitments[:5], 1):
            if isinstance(commitment, dict):
                text = commitment.get('commitment', commitment.get('text', str(commitment)))
                conf = commitment.get('confidence', 'N/A')
                print(f"   {i}. {text[:80]}... (confidence: {conf})")
            else:
                print(f"   {i}. {str(commitment)[:80]}...")
        
        print(f"\n⚠️  DETAILED RISKS:")
        for i, risk in enumerate(risks[:5], 1):
            if isinstance(risk, dict):
                text = risk.get('risk', risk.get('description', str(risk)))
                impact = risk.get('impact', risk.get('severity', 'N/A'))
                print(f"   {i}. {text[:80]}... (impact: {impact})")
            else:
                print(f"   {i}. {str(risk)[:80]}...")
        
        print(f"\n💰 FINANCIAL INSIGHTS:")
        for i, insight in enumerate(financial[:3], 1):
            if isinstance(insight, dict):
                metric = insight.get('metric_type', insight.get('metric', str(insight)))
                value = insight.get('current_value', insight.get('value', 'N/A'))
                print(f"   {i}. {metric}: {value}")
            else:
                print(f"   {i}. {str(insight)[:60]}...")
        
        return {
            'provider': provider_name,
            'success': True,
            'processing_time': processing_time,
            'commitments_count': len(commitments),
            'risks_count': len(risks),
            'financial_count': len(financial),
            'sentiment': sentiment,
            'commitments': commitments[:5],
            'risks': risks[:5],
            'financial': financial[:3]
        }
        
    except Exception as e:
        processing_time = time.time() - start_time
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'provider': provider_name,
            'success': False,
            'processing_time': processing_time,
            'error': str(e)
        }

def compare_results(ollama_result, openai_result):
    """Generate detailed comparison"""
    print(f"\n📊 COMPREHENSIVE COMPARISON")
    print("=" * 60)
    
    if not ollama_result['success'] or not openai_result['success']:
        print("⚠️ One or both tests failed - cannot compare")
        return
    
    # Performance comparison
    print(f"⚡ PERFORMANCE COMPARISON:")
    print(f"   Ollama:  {ollama_result['processing_time']:.1f}s (FREE)")
    print(f"   OpenAI:  {openai_result['processing_time']:.1f}s (~$0.001-0.01)")
    
    speed_winner = "OpenAI" if openai_result['processing_time'] < ollama_result['processing_time'] else "Ollama"
    print(f"   🏆 Speed Winner: {speed_winner}")
    
    # Content analysis comparison
    print(f"\n🎯 CONTENT ANALYSIS COMPARISON:")
    
    metrics = [
        ('Commitments', 'commitments_count'),
        ('Risks', 'risks_count'), 
        ('Financial Items', 'financial_count')
    ]
    
    for name, key in metrics:
        ollama_val = ollama_result.get(key, 0)
        openai_val = openai_result.get(key, 0)
        winner = "OpenAI" if openai_val > ollama_val else "Ollama" if ollama_val > openai_val else "Tie"
        print(f"   {name:<15}: Ollama={ollama_val:<3} OpenAI={openai_val:<3} Winner={winner}")
    
    # Quality assessment
    print(f"\n🏆 QUALITY ASSESSMENT:")
    print(f"   🏠 Ollama Strengths:")
    print(f"      • Completely FREE (no API costs)")
    print(f"      • Privacy-focused (local processing)")
    print(f"      • No rate limits or quotas")
    print(f"      • Offline capability")
    
    print(f"   🌐 OpenAI Strengths:")
    print(f"      • Faster processing ({openai_result['processing_time']:.1f}s vs {ollama_result['processing_time']:.1f}s)")
    print(f"      • Potentially more detailed analysis")
    print(f"      • Advanced reasoning capabilities")
    print(f"      • Consistent availability")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    print(f"   🎯 Choose Ollama when:")
    print(f"      • Cost is primary concern (FREE vs paid)")
    print(f"      • Privacy is critical (no external API calls)")
    print(f"      • Processing volume is high")
    print(f"      • Offline operation needed")
    
    print(f"   🎯 Choose OpenAI when:")
    print(f"      • Speed is critical (especially for real-time use)")
    print(f"      • Maximum analysis detail needed")
    print(f"      • Budget allows API costs")
    print(f"      • Integration with other OpenAI services")

def main():
    """Run live comparison test"""
    print(f"🎯 LIVE OPENAI vs OLLAMA COMPARISON")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Load test document
    document = create_test_document()
    print(f"📄 Test document loaded: {document.metadata.word_count} words")
    
    # Test both providers
    print(f"\n🚀 Starting dual analysis...")
    
    # Test Ollama first (it takes longer)
    ollama_result = analyze_with_provider("ollama", document)
    
    # Test OpenAI
    openai_result = analyze_with_provider("openai", document)
    
    # Compare results
    compare_results(ollama_result, openai_result)
    
    # Save results for reference
    comparison_results = {
        'timestamp': datetime.now().isoformat(),
        'ollama': ollama_result,
        'openai': openai_result
    }
    
    with open('comparison_results.json', 'w') as f:
        json.dump(comparison_results, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to comparison_results.json")
    print(f"🎉 Comparison complete!")

if __name__ == "__main__":
    main()
