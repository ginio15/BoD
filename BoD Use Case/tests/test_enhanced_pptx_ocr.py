#!/usr/bin/env python3
"""
Enhanced PPTX OCR Test - Validate improved screenshot processing

Tests the enhanced OCR functionality specifically designed for 
presentation files containing screenshot images.
"""

import time
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.document_parser import DocumentParser
from src.utils.optimized_analysis_engine import OptimizedAnalysisEngine
from src.utils.llm_providers import LLMProviderManager

def test_enhanced_pptx_processing():
    """Test enhanced PPTX processing with OCR improvements"""
    print("🎯 Enhanced PPTX OCR Processing Test")
    print("=" * 50)
    
    parser = DocumentParser()
    analysis_engine = OptimizedAnalysisEngine()
    
    # Test files - screenshot-based presentations
    test_files = [
        {
            "path": "data/uploads/Presentation1.pptx",
            "name": "Presentation 1 (Kalamaras Update)",
            "expected_keywords": ["Kalamaras", "vendors", "strategy", "negotiations", "sourcing"]
        },
        {
            "path": "data/uploads/Presentation2.pptx", 
            "name": "Presentation 2 (Overview)",
            "expected_keywords": ["Overview", "vendors", "strategy", "hybrid", "contracts"]
        }
    ]
    
    results = {}
    
    for test_file in test_files:
        file_path = Path(test_file["path"])
        
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            continue
            
        print(f"\n📄 Testing: {test_file['name']}")
        print(f"📁 File: {file_path.name}")
        print("-" * 40)
        
        try:
            # Parse document with enhanced OCR
            start_time = time.time()
            doc = parser.process_document(str(file_path), use_ocr=True)
            parse_time = time.time() - start_time
            
            # Validate OCR results
            content_length = len(doc.full_text.strip())
            word_count = doc.metadata.word_count
            ocr_pages = doc.ocr_pages
            
            print(f"✅ Parsing completed in {parse_time:.2f}s")
            print(f"📊 Extracted: {content_length} characters, {word_count} words")
            print(f"🔍 OCR pages: {ocr_pages}/{doc.metadata.total_pages}")
            
            # Check for expected keywords
            text_lower = doc.full_text.lower()
            found_keywords = [kw for kw in test_file["expected_keywords"] if kw.lower() in text_lower]
            
            print(f"🎯 Keywords found: {len(found_keywords)}/{len(test_file['expected_keywords'])}")
            print(f"   Found: {', '.join(found_keywords)}")
            
            if len(found_keywords) >= len(test_file["expected_keywords"]) * 0.6:  # 60% success rate
                print("✅ Keyword detection: PASSED")
            else:
                print("⚠️  Keyword detection: NEEDS IMPROVEMENT")
            
            # Preview extracted content
            if content_length > 0:
                preview = doc.full_text[:300].replace('\n', ' ').strip()
                print(f"📋 Content preview: {preview}...")
                
                # Test analysis pipeline
                if content_length > 100:
                    print(f"\n🔍 Running analysis...")
                    try:
                        analysis_start = time.time()
                        analysis_results = analysis_engine.analyze_document_optimized(doc, "ollama")
                        analysis_time = time.time() - analysis_start
                        
                        commitments = analysis_results.get('commitments', [])
                        financial = analysis_results.get('financial_insights', [])
                        risks = analysis_results.get('risks', [])
                        sentiment = analysis_results.get('sentiment', {})
                        
                        print(f"✅ Analysis completed in {analysis_time:.1f}s")
                        print(f"🎯 Commitments detected: {len(commitments)}")
                        print(f"💰 Financial insights: {len(financial)}")
                        print(f"⚠️  Risks identified: {len(risks)}")
                        print(f"😊 Sentiment: {sentiment.get('overall', 'unknown')}")
                        
                        # Sample results
                        if commitments:
                            print(f"\n📋 Sample commitments:")
                            for i, commitment in enumerate(commitments[:3]):
                                text = commitment.get('text', 'N/A')[:80]
                                confidence = commitment.get('confidence', 0)
                                try:
                                    conf_str = f"{float(confidence):.2f}" if confidence else "N/A"
                                except (ValueError, TypeError):
                                    conf_str = str(confidence)
                                print(f"   {i+1}. {text}... (confidence: {conf_str})")
                                
                        if financial:
                            print(f"\n💰 Sample financial insights:")
                            for i, insight in enumerate(financial[:2]):
                                text = insight.get('text', 'N/A')[:80]
                                print(f"   {i+1}. {text}...")
                        
                        results[test_file["name"]] = {
                            "parsing_success": True,
                            "parse_time": parse_time,
                            "content_length": content_length,
                            "word_count": word_count,
                            "keywords_found": len(found_keywords),
                            "keywords_expected": len(test_file["expected_keywords"]),
                            "analysis_success": True,
                            "analysis_time": analysis_time,
                            "commitments": len(commitments),
                            "financial": len(financial),
                            "risks": len(risks)
                        }
                        
                    except Exception as e:
                        print(f"⚠️  Analysis failed: {str(e)[:100]}")
                        results[test_file["name"]] = {
                            "parsing_success": True,
                            "analysis_success": False,
                            "error": str(e)
                        }
                else:
                    print("⚠️  Content too short for analysis")
                    
            else:
                print("❌ No content extracted")
                results[test_file["name"]] = {
                    "parsing_success": False,
                    "content_length": 0
                }
                
        except Exception as e:
            print(f"❌ Processing failed: {e}")
            results[test_file["name"]] = {
                "parsing_success": False,
                "error": str(e)
            }
    
    return results

def print_summary(results):
    """Print test summary"""
    print(f"\n🎯 ENHANCED PPTX OCR TEST SUMMARY")
    print("=" * 50)
    
    total_tests = len(results)
    successful_parsing = sum(1 for r in results.values() if r.get("parsing_success", False))
    successful_analysis = sum(1 for r in results.values() if r.get("analysis_success", False))
    
    print(f"📊 Total files tested: {total_tests}")
    print(f"✅ Successful parsing: {successful_parsing}/{total_tests}")
    print(f"🔍 Successful analysis: {successful_analysis}/{total_tests}")
    
    if successful_parsing > 0:
        avg_parse_time = sum(r.get("parse_time", 0) for r in results.values() if "parse_time" in r) / successful_parsing
        total_words = sum(r.get("word_count", 0) for r in results.values())
        total_commitments = sum(r.get("commitments", 0) for r in results.values())
        total_financial = sum(r.get("financial", 0) for r in results.values())
        
        print(f"⏱️  Average parse time: {avg_parse_time:.2f}s")
        print(f"📝 Total words extracted: {total_words}")
        print(f"🎯 Total commitments found: {total_commitments}")
        print(f"💰 Total financial insights: {total_financial}")
    
    print(f"\n🎉 Enhanced PPTX OCR functionality: {'✅ WORKING' if successful_parsing == total_tests else '⚠️ NEEDS ATTENTION'}")

def main():
    """Main test function"""
    print("🚀 Starting Enhanced PPTX OCR Test Suite")
    print("Testing screenshot-based presentation processing")
    print()
    
    # Run tests
    results = test_enhanced_pptx_processing()
    
    # Print summary
    print_summary(results)
    
    return results

if __name__ == "__main__":
    main()
