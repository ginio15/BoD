#!/usr/bin/env python3
"""
Simple test of comprehensive analysis
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

try:
    print("Starting test...")
    
    from src.utils.optimized_analysis_engine import OptimizedAnalysisEngine
    from src.models.document import ProcessedDocument, DocumentPage, DocumentMetadata
    
    print("Imports successful")
    
    # Create simple test
    text = """Board Meeting Q4 2024. Approved $2M budget for digital transformation by Q2 2025. 
    Risk: supply chain disruption. Revenue up 15%. Board optimistic about growth."""
    
    page = DocumentPage(page_number=1, text=text)
    doc = ProcessedDocument(
        pages=[page],
        metadata=DocumentMetadata(filename="test.txt", file_type="txt")
    )
    
    print("Document created")
    
    engine = OptimizedAnalysisEngine()
    print("Engine created")
    
    results = engine.analyze_document_optimized(doc)
    print(f"Analysis complete! Found {len(results.get('commitments', []))} commitments")
    
    print("✅ SUCCESS!")

except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
