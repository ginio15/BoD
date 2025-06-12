#!/usr/bin/env python3
"""
Test OpenAI API configuration and provider availability
"""

from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

print("🔑 Testing OpenAI API Key Configuration")
print("=" * 50)

# Test environment variable
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print(f"✅ OPENAI_API_KEY found: {api_key[:10]}...{api_key[-4:]}")
else:
    print("❌ OPENAI_API_KEY not found")
    exit(1)

# Test LLM Provider Manager
print("\n🔧 Testing LLM Provider Manager")
print("=" * 50)

try:
    from src.utils.llm_providers import LLMProviderManager
    
    manager = LLMProviderManager()
    available_providers = manager.get_available_providers()
    print(f"✅ Available providers: {available_providers}")
    
    if 'openai' in available_providers:
        print("✅ OpenAI provider is available")
        
        print("\n🧪 Testing simple OpenAI request")
        print("-" * 30)
        response = manager.generate_response(
            "Say hello in exactly 5 words.",
            provider='openai'
        )
        
        if response.error:
            print(f"❌ Error: {response.error}")
        else:
            print(f"✅ Success! Response: {response.content}")
            print(f"   Model: {response.model}")
            print(f"   Tokens used: {response.tokens_used}")
            print(f"   Cost: ${response.cost:.4f}")
            print(f"   Response time: {response.response_time:.2f}s")
    else:
        print("❌ OpenAI provider not available")
        
    # Check usage summary
    summary = manager.get_usage_summary()
    print(f"\n📊 Usage Summary")
    print("-" * 30)
    for provider, info in summary['providers'].items():
        status = "✅" if info["available"] else "❌"
        print(f"{status} {provider}: Available={info['available']}, Requests={info['request_count']}, Cost=${info['total_cost']:.4f}")
        
except Exception as e:
    import traceback
    print(f"❌ Error: {e}")
    print(traceback.format_exc())

print("\n🎯 Testing BoD Analysis")
print("=" * 50)

try:
    # Test with a simple board presentation text
    test_text = """
    Board Meeting Q1 2024
    
    Financial Performance:
    - Revenue increased by 15% to $2.5M
    - Operating margin improved to 18%
    
    Strategic Commitments:
    - We will launch the new product line by Q3 2024
    - Plan to reduce operational costs by 10% this year
    
    Risk Assessment:
    - Market competition increasing
    - Supply chain disruptions possible
    """
    
    print("Testing with sample board text...")
    from src.utils.enhanced_analysis_engine import EnhancedAnalysisEngine
    
    engine = EnhancedAnalysisEngine()
    results = engine.analyze_presentation(test_text, provider='openai')
    
    if results.get('error'):
        print(f"❌ Analysis Error: {results['error']}")
    else:
        print("✅ Analysis completed successfully!")
        print(f"   Commitments found: {len(results.get('commitments', []))}")
        print(f"   Risks found: {len(results.get('risks', []))}")
        print(f"   Financial metrics: {len(results.get('financial_metrics', []))}")
        
except Exception as e:
    print(f"❌ Analysis Error: {e}")
    import traceback
    print(traceback.format_exc())
