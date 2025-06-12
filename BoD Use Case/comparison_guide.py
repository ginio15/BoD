#!/usr/bin/env python3
"""
OpenAI vs Ollama Results Comparison
Run this after testing both providers in the Streamlit UI
"""

print("🎯 OPENAI vs OLLAMA COMPARISON GUIDE")
print("=" * 60)

print("""
🌐 TESTING INSTRUCTIONS:

1. Open the Enhanced BoD Analyzer: http://localhost:8502

2. Test with OLLAMA first:
   • Select "ollama" in the sidebar
   • Choose "Use Sample Document" or paste this test text:
   
   "Board Meeting Q1 2024: Revenue increased 18% to $4.2M. 
    We will launch new AI product by September 2024. 
    Committed to 25% cost reduction by Q4 2024.
    Risk: High competition from Tech Giant Corp.
    Board expressed strong confidence in leadership."
   
   • Click "Run Enhanced Analysis"
   • Note the results and timing

3. Test with OPENAI:
   • Change provider to "openai" in sidebar
   • Use the SAME text/document
   • Click "Run Enhanced Analysis"  
   • Compare results with Ollama

📊 COMPARISON CHECKLIST:
""")

comparison_metrics = [
    "⏱️  Processing Time",
    "💼 Number of Commitments Found", 
    "⚠️  Number of Risks Identified",
    "💰 Financial Metrics Extracted",
    "🎯 Strategic Priorities Listed",
    "😊 Sentiment Analysis Quality",
    "📋 Executive Summary Detail",
    "💵 Cost per Analysis"
]

for metric in comparison_metrics:
    print(f"   [ ] {metric}")

print(f"""

🏆 EXPECTED RESULTS:

🌐 OpenAI (GPT-3.5-turbo):
   • Speed: ~1-3 seconds
   • Cost: ~$0.001-0.01 per analysis  
   • Strengths: Detailed analysis, nuanced understanding
   • Commitments: Typically finds 3-5 with high confidence
   • Risks: Detailed risk categorization and impact assessment
   • Sentiment: Sophisticated reasoning and context understanding

🏠 Ollama (llama3.2:3b):
   • Speed: ~25-30 seconds
   • Cost: $0.00 (completely free)
   • Strengths: Privacy, offline capability, no API limits
   • Commitments: Typically finds 2-4 with good accuracy
   • Risks: Solid risk identification with basic categorization
   • Sentiment: Good general sentiment detection

💡 RECOMMENDATION MATRIX:

Choose OPENAI when:
   ✅ Maximum accuracy is critical
   ✅ Processing speed is important (1-3s vs 25-30s)
   ✅ Detailed financial analysis needed
   ✅ Complex document structure
   ✅ Budget allows API costs

Choose OLLAMA when:
   ✅ Privacy is paramount (no data sent to external APIs)
   ✅ Cost is a primary concern (completely free)
   ✅ Offline capability needed
   ✅ High-volume batch processing
   ✅ Good enough accuracy for regular use

🎯 BOTTOM LINE:
Both providers deliver excellent results for board presentation analysis.
OpenAI excels in speed and detail, Ollama excels in cost and privacy.
""")

def show_manual_test_results():
    """Interactive results collection"""
    print(f"\n📋 MANUAL TEST RESULTS COLLECTION")
    print("-" * 40)
    
    providers = ["Ollama", "OpenAI"]
    results = {}
    
    for provider in providers:
        print(f"\n🔍 {provider} Results:")
        print("After testing in the UI, enter your observations:")
        
        try:
            processing_time = input(f"   Processing time (seconds): ")
            commitments = input(f"   Commitments found: ")
            risks = input(f"   Risks identified: ")
            financial = input(f"   Financial metrics: ")
            sentiment = input(f"   Sentiment quality (1-5): ")
            
            results[provider] = {
                'time': processing_time,
                'commitments': commitments,
                'risks': risks,
                'financial': financial,
                'sentiment': sentiment
            }
        except KeyboardInterrupt:
            print(f"\nSkipping manual input...")
            break
    
    if len(results) == 2:
        print(f"\n📊 YOUR COMPARISON RESULTS:")
        print(f"{'Metric':<20} {'Ollama':<15} {'OpenAI':<15}")
        print("-" * 50)
        print(f"{'Processing Time':<20} {results['Ollama']['time']:<15} {results['OpenAI']['time']:<15}")
        print(f"{'Commitments':<20} {results['Ollama']['commitments']:<15} {results['OpenAI']['commitments']:<15}")
        print(f"{'Risks':<20} {results['Ollama']['risks']:<15} {results['OpenAI']['risks']:<15}")
        print(f"{'Financial':<20} {results['Ollama']['financial']:<15} {results['OpenAI']['financial']:<15}")
        print(f"{'Sentiment (1-5)':<20} {results['Ollama']['sentiment']:<15} {results['OpenAI']['sentiment']:<15}")

if __name__ == "__main__":
    print(f"\n" + "="*60)
    print("Ready to collect your test results? (y/n)")
    response = input().lower()
    if response.startswith('y'):
        show_manual_test_results()
    else:
        print("Test both providers in the UI, then run this script again!")
