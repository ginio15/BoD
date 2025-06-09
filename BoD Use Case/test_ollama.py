#!/usr/bin/env python3
"""
Test script for Ollama integration in BoD Analysis System
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.utils.llm_providers import LLMProviderManager
import json

def test_ollama_basic():
    """Test basic Ollama functionality"""
    print("=== Testing Ollama Basic Functionality ===")
    
    # Initialize provider manager
    manager = LLMProviderManager()
    
    # Check available providers
    available = manager.get_available_providers()
    print(f"Available providers: {available}")
    
    if "ollama" not in available:
        print("❌ Ollama not available!")
        return False
    
    # Test simple prompt
    prompt = "What is the capital of France? Please respond in one sentence."
    print(f"\nTesting prompt: {prompt}")
    
    response = manager.generate_response(prompt, provider="ollama", model="llama3.2:3b")
    
    if response.error:
        print(f"❌ Error: {response.error}")
        return False
    
    print(f"✅ Response: {response.content}")
    print(f"   Model: {response.model}")
    print(f"   Tokens: {response.tokens_used}")
    print(f"   Response time: {response.response_time:.2f}s")
    
    return True

def test_ollama_board_analysis():
    """Test Ollama with board presentation analysis"""
    print("\n=== Testing Ollama Board Analysis ===")
    
    manager = LLMProviderManager()
    
    # Sample board presentation text
    board_text = """
    Q4 2023 Financial Results and Strategic Update
    
    Revenue Growth: We achieved 15% year-over-year revenue growth, reaching $2.5M in Q4.
    
    Key Commitments for 2024:
    - We will reduce operational costs by 10% by Q2 2024
    - Plan to launch new product line in Q3 2024
    - Target market expansion into European markets by December 2024
    - Committed to improving customer satisfaction scores to 85% by end of 2024
    
    Risk Factors:
    - Market volatility may impact Q1 performance
    - Supply chain constraints continue to pose challenges
    - Regulatory changes in target markets create uncertainty
    
    Overall sentiment: The board is optimistic about 2024 prospects but acknowledges significant challenges ahead.
    """
    
    # Commitment extraction prompt
    commitment_prompt = f"""
    Analyze the following board presentation excerpt and extract key commitments with their details:
    
    Text: {board_text}
    
    Please identify:
    1. All specific commitments made
    2. Target dates or deadlines
    3. Quantifiable metrics or goals
    4. Confidence level (high/medium/low) for each commitment
    
    Format as JSON with this structure:
    {{
        "commitments": [
            {{
                "commitment": "description",
                "deadline": "date",
                "metric": "quantifiable goal",
                "confidence": "high/medium/low",
                "category": "financial/operational/strategic"
            }}
        ]
    }}
    """
    
    print("Testing commitment extraction...")
    response = manager.generate_response(commitment_prompt, provider="ollama", model="llama3.2:3b")
    
    if response.error:
        print(f"❌ Error: {response.error}")
        return False
    
    print(f"✅ Commitment Analysis Response:")
    print(f"   Response time: {response.response_time:.2f}s")
    print(f"   Content length: {len(response.content)} chars")
    print(f"   Response: {response.content[:500]}...")
    
    # Test sentiment analysis
    sentiment_prompt = f"""
    Analyze the sentiment of this board presentation excerpt:
    
    Text: {board_text}
    
    Provide:
    1. Overall sentiment (positive/negative/neutral)
    2. Confidence level (1-10)
    3. Key sentiment indicators
    4. Risk assessment tone
    
    Keep response concise and structured.
    """
    
    print("\nTesting sentiment analysis...")
    response = manager.generate_response(sentiment_prompt, provider="ollama", model="llama3.2:3b")
    
    if response.error:
        print(f"❌ Error: {response.error}")
        return False
    
    print(f"✅ Sentiment Analysis Response:")
    print(f"   Response time: {response.response_time:.2f}s")
    print(f"   Response: {response.content[:400]}...")
    
    return True

def test_provider_comparison():
    """Test comparing Ollama with other providers if available"""
    print("\n=== Testing Provider Comparison ===")
    
    manager = LLMProviderManager()
    available = manager.get_available_providers()
    
    if len(available) < 2:
        print(f"Only {len(available)} provider(s) available: {available}")
        print("Skipping comparison test")
        return True
    
    simple_prompt = "Explain the importance of board governance in one paragraph."
    
    print(f"Comparing providers: {available}")
    results = manager.compare_providers(simple_prompt, available)
    
    for provider, response in results.items():
        if response.error:
            print(f"❌ {provider}: {response.error}")
        else:
            print(f"✅ {provider}: {len(response.content)} chars, {response.response_time:.2f}s")
            print(f"   First 100 chars: {response.content[:100]}...")
    
    return True

def main():
    """Run all Ollama tests"""
    print("🔧 Testing Ollama Integration for BoD Analysis System")
    print("=" * 60)
    
    tests = [
        test_ollama_basic,
        test_ollama_board_analysis,
        test_provider_comparison
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_func.__name__} PASSED")
            else:
                print(f"❌ {test_func.__name__} FAILED")
        except Exception as e:
            print(f"❌ {test_func.__name__} FAILED with exception: {str(e)}")
        
        print("-" * 40)
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    # Show usage summary
    manager = LLMProviderManager()
    usage = manager.get_usage_summary()
    print(f"\n💰 Usage Summary:")
    print(json.dumps(usage, indent=2))

if __name__ == "__main__":
    main()
