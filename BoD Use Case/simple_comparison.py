#!/usr/bin/env python3
"""Simple OpenAI vs Ollama test"""

from dotenv import load_dotenv
load_dotenv()

from src.utils.llm_providers import LLMProviderManager
import time

def test_simple_comparison():
    """Test both providers with a simple request"""
    
    test_prompt = """
    Analyze this board meeting text and extract commitments:
    
    "Board Meeting Q1 2024: We will launch the new product by September 2024. 
    Committed to reducing costs by 20% this year. Plan to hire 5 new engineers."
    
    Please list the commitments found.
    """
    
    manager = LLMProviderManager()
    
    print("🔍 SIMPLE COMPARISON TEST")
    print("=" * 50)
    
    # Test OpenAI
    print("\n🌐 Testing OpenAI...")
    start_time = time.time()
    openai_response = manager.generate_response(test_prompt, provider='openai')
    openai_time = time.time() - start_time
    
    if openai_response.error:
        print(f"❌ OpenAI Error: {openai_response.error}")
    else:
        print(f"✅ OpenAI Success!")
        print(f"   Response: {openai_response.content[:200]}...")
        print(f"   Cost: ${openai_response.cost:.4f}")
        print(f"   Time: {openai_time:.2f}s")
        print(f"   Tokens: {openai_response.tokens_used}")
    
    # Test Ollama
    print("\n🏠 Testing Ollama...")
    start_time = time.time()
    ollama_response = manager.generate_response(test_prompt, provider='ollama')
    ollama_time = time.time() - start_time
    
    if ollama_response.error:
        print(f"❌ Ollama Error: {ollama_response.error}")
    else:
        print(f"✅ Ollama Success!")
        print(f"   Response: {ollama_response.content[:200]}...")
        print(f"   Cost: ${ollama_response.cost:.4f}")
        print(f"   Time: {ollama_time:.2f}s")
        print(f"   Tokens: {ollama_response.tokens_used}")
    
    # Comparison
    print(f"\n📊 COMPARISON")
    print("-" * 30)
    if not openai_response.error and not ollama_response.error:
        print(f"Speed:  OpenAI {openai_time:.1f}s vs Ollama {ollama_time:.1f}s")
        print(f"Cost:   OpenAI ${openai_response.cost:.4f} vs Ollama ${ollama_response.cost:.4f}")
        faster = "OpenAI" if openai_time < ollama_time else "Ollama"
        print(f"Winner: {faster} (speed), Ollama (cost)")
    
    return openai_response, ollama_response

if __name__ == "__main__":
    test_simple_comparison()
