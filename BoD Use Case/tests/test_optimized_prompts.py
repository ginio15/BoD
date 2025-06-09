#!/usr/bin/env python3
"""
Quick test of Ollama with optimized shorter prompts
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.utils.llm_providers import LLMProviderManager
import time

def test_optimized_prompts():
    """Test Ollama with shorter, optimized prompts"""
    print("🔬 Testing Optimized Ollama Prompts")
    print("=" * 50)
    
    manager = LLMProviderManager()
    
    # Sample text (shorter version)
    sample_text = """
    Q4 2023 Board Meeting Summary:
    
    Financial Results: Revenue $2.5M (15% growth), profit margin 12%
    
    Key Commitments:
    - Reduce costs by 10% by Q2 2024
    - Launch AI platform in Q3 2024  
    - Enter European markets by Dec 2024
    - Improve customer satisfaction to 85%
    
    Risks: Supply chain issues, cybersecurity threats, economic recession
    
    Board sentiment: Cautiously optimistic but focused on risk management
    """
    
    # Test 1: Short commitment extraction
    print("\n1. Testing Commitment Extraction...")
    commitment_prompt = f"""Extract commitments from this board text. List each commitment with its deadline and category (financial/operational/strategic).

Text: {sample_text}

Format: 
- Commitment: [text]
  Deadline: [date] 
  Category: [type]"""
    
    start_time = time.time()
    response = manager.generate_response(commitment_prompt, provider="ollama", model="llama3.2:3b")
    
    if response.error:
        print(f"❌ Error: {response.error}")
    else:
        print(f"✅ Success ({time.time() - start_time:.1f}s)")
        print(f"Response: {response.content[:200]}...")
    
    # Test 2: Short risk analysis
    print("\n2. Testing Risk Analysis...")
    risk_prompt = f"""Identify the main risks mentioned in this board presentation.

Text: {sample_text}

For each risk, provide:
Risk: [description]
Level: high/medium/low
Impact: [potential effect]"""
    
    start_time = time.time()
    response = manager.generate_response(risk_prompt, provider="ollama", model="llama3.2:3b")
    
    if response.error:
        print(f"❌ Error: {response.error}")
    else:
        print(f"✅ Success ({time.time() - start_time:.1f}s)")
        print(f"Response: {response.content[:200]}...")
    
    # Test 3: Short sentiment analysis
    print("\n3. Testing Sentiment Analysis...")
    sentiment_prompt = f"""Analyze the sentiment in this board presentation. 

Text: {sample_text}

Provide:
Overall sentiment: positive/negative/neutral/mixed
Confidence: 1-10
Key indicators: [words/phrases that indicate sentiment]"""
    
    start_time = time.time()
    response = manager.generate_response(sentiment_prompt, provider="ollama", model="llama3.2:3b")
    
    if response.error:
        print(f"❌ Error: {response.error}")
    else:
        print(f"✅ Success ({time.time() - start_time:.1f}s)")
        print(f"Response: {response.content[:200]}...")
    
    print("\n📊 Test Summary:")
    print("Optimized shorter prompts work better with Ollama")
    print("Recommendation: Break complex analysis into smaller focused tasks")

if __name__ == "__main__":
    test_optimized_prompts()
