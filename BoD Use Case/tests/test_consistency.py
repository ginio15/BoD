#!/usr/bin/env python3
"""
Test script to investigate inconsistent analysis results for PPTX files
"""

import os
import sys
import json
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.utils.document_parser import DocumentParser
from src.utils.optimized_analysis_engine import OptimizedAnalysisEngine

def test_consistency():
    """Test the same PPTX file multiple times to check for consistency"""
    
    # Initialize components
    parser = DocumentParser()
    analyzer = OptimizedAnalysisEngine()
    
    # Test files
    test_files = [
        "data/uploads/Presentation1.pptx",
        "data/uploads/Presentation2.pptx"
    ]
    
    results = {}
    
    for file_path in test_files:
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            continue
            
        print(f"\n🔍 Testing consistency for: {file_path}")
        print("=" * 60)
        
        file_results = []
        
        # Run the same file 3 times
        for run in range(1, 4):
            print(f"\n--- Run {run} ---")
            
            try:
                # Parse document
                print("📄 Parsing document...")
                start_time = time.time()
                parsed_result = parser.process_document(file_path)
                parse_time = time.time() - start_time
                
                print(f"✅ Parsed in {parse_time:.2f}s")
                print(f"📝 Extracted text length: {len(parsed_result.full_text)}")
                
                # Analyze document
                print("🔍 Analyzing document...")
                start_time = time.time()
                analysis_result = analyzer.analyze_document_optimized(parsed_result)
                analysis_time = time.time() - start_time
                
                print(f"✅ Analyzed in {analysis_time:.2f}s")
                
                # Store results
                run_result = {
                    'run': run,
                    'parsed_text_length': len(parsed_result.full_text),
                    'parsed_text_preview': parsed_result.full_text[:200],
                    'analysis_time': analysis_time,
                    'commitments_count': len(analysis_result.get('commitments', [])),
                    'commitments': analysis_result.get('commitments', []),
                    'risks_count': len(analysis_result.get('risks', [])),
                    'risks': analysis_result.get('risks', []),
                    'financial_insights_count': len(analysis_result.get('financial_insights', [])),
                    'financial_insights': analysis_result.get('financial_insights', []),
                    'sentiment': analysis_result.get('sentiment', {}),
                    'summary': analysis_result.get('summary', ''),
                    'full_analysis': analysis_result
                }
                
                file_results.append(run_result)
                
                # Print summary
                print(f"📊 Commitments: {run_result['commitments_count']}")
                print(f"⚠️  Risks: {run_result['risks_count']}")
                print(f"💰 Financial insights: {run_result['financial_insights_count']}")
                print(f"😊 Sentiment: {run_result['sentiment'].get('overall', 'unknown')}")
                print(f"📝 Summary preview: {run_result['summary'][:100]}...")
                
            except Exception as e:
                print(f"❌ Error in run {run}: {str(e)}")
                file_results.append({
                    'run': run,
                    'error': str(e)
                })
        
        results[file_path] = file_results
        
        # Analyze consistency for this file
        print(f"\n📈 CONSISTENCY ANALYSIS for {file_path}")
        print("-" * 40)
        
        if len(file_results) >= 2:
            # Check OCR consistency
            text_lengths = [r.get('parsed_text_length', 0) for r in file_results if 'parsed_text_length' in r]
            if text_lengths:
                print(f"📝 Text lengths: {text_lengths}")
                print(f"📝 Text length variance: {max(text_lengths) - min(text_lengths)}")
            
            # Check analysis consistency
            commitment_counts = [r.get('commitments_count', 0) for r in file_results if 'commitments_count' in r]
            risk_counts = [r.get('risks_count', 0) for r in file_results if 'risks_count' in r]
            financial_counts = [r.get('financial_insights_count', 0) for r in file_results if 'financial_insights_count' in r]
            
            print(f"📊 Commitment counts: {commitment_counts}")
            print(f"⚠️  Risk counts: {risk_counts}")
            print(f"💰 Financial insight counts: {financial_counts}")
            
            # Check if results are identical
            if len(set(commitment_counts)) == 1 and len(set(risk_counts)) == 1 and len(set(financial_counts)) == 1:
                print("✅ Results are CONSISTENT")
            else:
                print("❌ Results are INCONSISTENT")
                
            # Compare actual commitments
            if len(file_results) >= 2:
                print("\n🔍 Detailed comparison:")
                for i in range(len(file_results) - 1):
                    run1 = file_results[i]
                    run2 = file_results[i + 1]
                    
                    if 'commitments' in run1 and 'commitments' in run2:
                        commitments1 = set(run1['commitments'])
                        commitments2 = set(run2['commitments'])
                        
                        if commitments1 == commitments2:
                            print(f"✅ Commitments identical between run {run1['run']} and {run2['run']}")
                        else:
                            print(f"❌ Commitments differ between run {run1['run']} and {run2['run']}")
                            print(f"   Run {run1['run']}: {commitments1}")
                            print(f"   Run {run2['run']}: {commitments2}")
    
    # Save detailed results
    output_file = "consistency_test_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Detailed results saved to: {output_file}")
    return results

if __name__ == "__main__":
    print("🔍 Testing PPTX Analysis Consistency")
    print("=" * 50)
    
    results = test_consistency()
    
    print("\n🎯 OVERALL CONCLUSION:")
    print("=" * 30)
    
    inconsistent_files = []
    for file_path, file_results in results.items():
        if len(file_results) >= 2:
            # Check for inconsistencies
            commitment_counts = [r.get('commitments_count', 0) for r in file_results if 'commitments_count' in r]
            if len(set(commitment_counts)) > 1:
                inconsistent_files.append(file_path)
    
    if inconsistent_files:
        print("❌ INCONSISTENCY DETECTED in:")
        for file in inconsistent_files:
            print(f"   - {file}")
        print("\nPossible causes:")
        print("   1. LLM non-determinism (temperature > 0)")
        print("   2. Model state variations")
        print("   3. Prompt processing differences")
        print("   4. OCR processing variations")
    else:
        print("✅ Results appear CONSISTENT across runs")
