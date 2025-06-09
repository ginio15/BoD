#!/usr/bin/env python3
"""
Test script to process PPTX files and monitor system output
"""

import sys
import os
import time
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.document_parser import DocumentParser
from src.utils.enhanced_analysis_engine import EnhancedAnalysisEngine
from src.utils.llm_providers import LLMProviders

def test_pptx_processing():
    """Test PPTX file processing with detailed monitoring"""
    
    print("🔍 BoD Use Case - PPTX Testing System")
    print("=" * 50)
    
    # Initialize components
    print("\n📋 Initializing components...")
    parser = DocumentParser()
    llm_providers = LLMProviders()
    analysis_engine = EnhancedAnalysisEngine(llm_providers)
    
    # Test files
    upload_dir = Path("data/uploads")
    pptx_files = ["Presentation1.pptx", "Presentation2.pptx"]
    
    for filename in pptx_files:
        file_path = upload_dir / filename
        
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            continue
            
        print(f"\n🎯 Processing: {filename}")
        print("-" * 30)
        
        try:
            # Step 1: Document Parsing
            print("📄 Step 1: Parsing PPTX document...")
            start_time = time.time()
            
            doc = parser.parse_document(str(file_path))
            parse_time = time.time() - start_time
            
            print(f"✅ Parsing completed in {parse_time:.2f} seconds")
            print(f"📊 Extracted text length: {len(doc.content)} characters")
            print(f"📖 Number of pages/slides: {len(doc.pages) if hasattr(doc, 'pages') else 'N/A'}")
            
            # Show preview of extracted content
            content_preview = doc.content[:300] + "..." if len(doc.content) > 300 else doc.content
            print(f"📝 Content preview:\n{content_preview}")
            
            # Step 2: Analysis
            print(f"\n🔍 Step 2: Analyzing content for BoD insights...")
            analysis_start = time.time()
            
            # Configure analysis settings
            analysis_config = {
                'provider': 'ollama',  # Use free local Ollama
                'model': 'llama3.2',   # Default model
                'max_retries': 2,
                'timeout': 120
            }
            
            print(f"⚙️  Analysis configuration: {analysis_config}")
            
            # Perform analysis
            results = analysis_engine.analyze_document(doc, analysis_config)
            analysis_time = time.time() - analysis_start
            
            print(f"✅ Analysis completed in {analysis_time:.2f} seconds")
            
            # Step 3: Display Results
            print(f"\n📈 Step 3: Analysis Results for {filename}")
            print("=" * 40)
            
            if results:
                # Commitments
                commitments = results.get('commitments', [])
                print(f"🎯 Commitments found: {len(commitments)}")
                for i, commitment in enumerate(commitments[:3], 1):  # Show first 3
                    print(f"   {i}. {commitment.get('text', 'N/A')[:100]}...")
                
                # Sentiment
                sentiment = results.get('sentiment', {})
                print(f"💭 Overall sentiment: {sentiment.get('overall', 'N/A')}")
                print(f"📊 Confidence: {sentiment.get('confidence', 'N/A')}")
                
                # Risk assessment
                risks = results.get('risks', [])
                print(f"⚠️  Risk factors identified: {len(risks)}")
                for i, risk in enumerate(risks[:2], 1):  # Show first 2
                    print(f"   {i}. {risk.get('description', 'N/A')[:80]}...")
                
                # Financial insights
                financial = results.get('financial_insights', {})
                print(f"💰 Financial metrics found: {len(financial.get('metrics', []))}")
                
                # Executive summary
                summary = results.get('executive_summary', '')
                if summary:
                    summary_preview = summary[:200] + "..." if len(summary) > 200 else summary
                    print(f"📋 Executive summary preview:\n{summary_preview}")
                
            else:
                print("❌ No analysis results returned")
            
            print(f"\n⏱️  Total processing time: {parse_time + analysis_time:.2f} seconds")
            
        except Exception as e:
            print(f"❌ Error processing {filename}: {str(e)}")
            import traceback
            print(f"🔍 Traceback:\n{traceback.format_exc()}")
        
        print("\n" + "="*50)
    
    print("\n🎉 PPTX Testing Complete!")
    print("💡 If you see analysis results above, the system is working correctly!")

if __name__ == "__main__":
    test_pptx_processing()
