#!/usr/bin/env python3
"""
OCR Consistency Test for PPTX Files
Tests for consistent OCR results across multiple runs
"""

import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from utils.document_parser import DocumentParser
except ImportError:
    # Alternative import path
    sys.path.insert(0, '.')
    try:
        from src.utils.document_parser import DocumentParser
    except ImportError:
        # Final fallback
        import src.utils.document_parser as dp
        DocumentParser = dp.DocumentParser

def test_ocr_consistency(file_path: str, iterations: int = 3) -> Dict:
    """Test OCR consistency across multiple runs"""
    print(f"🔄 Testing OCR consistency for: {Path(file_path).name}")
    print(f"📊 Running {iterations} iterations...")
    
    parser = DocumentParser()
    results = []
    
    for i in range(iterations):
        print(f"   Run {i+1}/{iterations}...", end=" ")
        
        try:
            start_time = time.time()
            processed_doc = parser.process_document(file_path)
            parse_time = time.time() - start_time
            
            result = {
                "run": i + 1,
                "success": True,
                "parse_time": parse_time,
                "char_count": len(processed_doc.full_text),
                "word_count": len(processed_doc.full_text.split()),
                "content_preview": processed_doc.full_text[:100].replace('\n', ' '),
                "full_text": processed_doc.full_text
            }
            results.append(result)
            print(f"✅ {result['word_count']} words, {result['char_count']} chars")
            
        except Exception as e:
            result = {
                "run": i + 1,
                "success": False,
                "error": str(e)
            }
            results.append(result)
            print(f"❌ Error: {str(e)[:50]}...")
    
    return analyze_consistency(results)

def analyze_consistency(results: List[Dict]) -> Dict:
    """Analyze consistency of OCR results"""
    successful_runs = [r for r in results if r.get("success", False)]
    
    if not successful_runs:
        return {
            "status": "all_failed",
            "total_runs": len(results),
            "successful_runs": 0
        }
    
    # Extract key metrics
    word_counts = [r["word_count"] for r in successful_runs]
    char_counts = [r["char_count"] for r in successful_runs]
    parse_times = [r["parse_time"] for r in successful_runs]
    
    # Check for exact text matches
    unique_texts = set(r["full_text"] for r in successful_runs)
    text_variations = len(unique_texts)
    
    analysis = {
        "status": "consistent" if text_variations == 1 else "inconsistent",
        "total_runs": len(results),
        "successful_runs": len(successful_runs),
        "text_variations": text_variations,
        "word_count_range": (min(word_counts), max(word_counts)),
        "word_count_variation": max(word_counts) - min(word_counts),
        "char_count_range": (min(char_counts), max(char_counts)),
        "char_count_variation": max(char_counts) - min(char_counts),
        "avg_parse_time": sum(parse_times) / len(parse_times),
        "parse_time_range": (min(parse_times), max(parse_times))
    }
    
    # Show detailed results  
    print(f"\n📊 CONSISTENCY ANALYSIS")
    print(f"   Status: {'✅ CONSISTENT' if analysis['status'] == 'consistent' else '⚠️  INCONSISTENT'}")
    print(f"   Successful runs: {analysis['successful_runs']}/{analysis['total_runs']}")
    print(f"   Text variations: {analysis['text_variations']}")
    print(f"   Word count range: {analysis['word_count_range'][0]}-{analysis['word_count_range'][1]} (variation: {analysis['word_count_variation']})")
    print(f"   Char count range: {analysis['char_count_range'][0]}-{analysis['char_count_range'][1]} (variation: {analysis['char_count_variation']})")
    print(f"   Parse time: {analysis['avg_parse_time']:.2f}s avg ({analysis['parse_time_range'][0]:.2f}-{analysis['parse_time_range'][1]:.2f}s)")
    
    if analysis['status'] == 'inconsistent':
        print(f"\n⚠️  INCONSISTENCY DETAILS:")
        for i, result in enumerate(successful_runs):
            print(f"   Run {result['run']}: {result['word_count']} words - {result['content_preview'][:60]}...")
    
    return analysis

def main():
    """Main test function"""
    print("🚀 OCR Consistency Test Suite")
    print("=" * 50)
    
    test_files = [
        "/Users/ginio/projects/Olympia/BoD Use Case/data/uploads/Presentation1.pptx",
        "/Users/ginio/projects/Olympia/BoD Use Case/data/uploads/Presentation2.pptx"
    ]
    
    all_results = {}
    
    for file_path in test_files:
        if Path(file_path).exists():
            results = test_ocr_consistency(file_path, iterations=3)
            all_results[Path(file_path).name] = results
            print()
        else:
            print(f"❌ File not found: {file_path}")
    
    # Summary
    print("🎯 OVERALL SUMMARY")
    print("=" * 50)
    
    for filename, results in all_results.items():
        status_icon = "✅" if results["status"] == "consistent" else "⚠️"
        print(f"{status_icon} {filename}: {results['status'].upper()}")
        if results.get("status") == "inconsistent":
            print(f"   Word count variation: {results['word_count_variation']}")
            print(f"   Text variations: {results['text_variations']}")
    
    # Overall status
    inconsistent_files = [f for f, r in all_results.items() if r.get("status") == "inconsistent"]
    if inconsistent_files:
        print(f"\n⚠️  INCONSISTENT FILES: {len(inconsistent_files)}")
        print("   Investigation required to identify root cause")
    else:
        print(f"\n✅ ALL FILES CONSISTENT")
        print("   OCR pipeline is working reliably")

if __name__ == "__main__":
    main()
