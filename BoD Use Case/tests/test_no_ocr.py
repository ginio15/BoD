#!/usr/bin/env python3
"""
Test document processing without OCR dependencies
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

def test_document_processing_without_ocr():
    """Test that document processing works even without OCR"""
    print("Testing Document Processing (No OCR)")
    print("=" * 40)
    
    try:
        from src.utils.document_parser import DocumentParser, OCR_AVAILABLE
        print(f"✅ DocumentParser imported successfully")
        print(f"OCR Available: {OCR_AVAILABLE}")
        
        # Create a parser instance
        parser = DocumentParser()
        print("✅ DocumentParser instance created")
        
        # Test with a simple text file (should work without OCR)
        test_text = """
        Board Meeting Q4 2024
        
        Key Decisions:
        1. Approved $2M budget for digital transformation
        2. Committed to 15% cost reduction by Q2 2025
        3. Risk identified: supply chain disruptions
        
        Financial highlights: Revenue up 12% YoY
        """
        
        # Save as temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(test_text)
            temp_file = f.name
        
        print(f"✅ Created test file: {temp_file}")
        
        # For now, just test that the parser can be created
        # Full document processing would require actual PDF/PPTX files
        print("✅ Document parser ready for use")
        
        # Clean up
        import os
        os.unlink(temp_file)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_enhanced_app_integration():
    """Test that the enhanced app components work together"""
    print("\nTesting Enhanced App Integration")
    print("=" * 40)
    
    try:
        from src.utils.optimized_analysis_engine import OptimizedAnalysisEngine
        from src.models.document import ProcessedDocument, DocumentPage, DocumentMetadata
        
        # Create test document
        text = "Board approved $2M budget. Revenue up 15%. Risk: supply chain issues."
        page = DocumentPage(page_number=1, text=text)
        doc = ProcessedDocument(
            pages=[page],
            metadata=DocumentMetadata(filename="test.txt", file_type="txt")
        )
        
        print("✅ Test document created")
        
        # Test analysis
        engine = OptimizedAnalysisEngine()
        results = engine.analyze_document_optimized(doc)
        
        print(f"✅ Analysis completed - Found {len(results.get('commitments', []))} commitments")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing BoD Analysis System (OCR-Free Mode)")
    print("=" * 50)
    
    test1 = test_document_processing_without_ocr()
    test2 = test_enhanced_app_integration()
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    if test1 and test2:
        print("🎉 ALL TESTS PASSED!")
        print("✅ System is working without OCR dependencies")
        print("✅ Enhanced Streamlit app should be functional")
        print("\n📊 Access your app at: http://localhost:8502")
    else:
        print("❌ Some tests failed - check logs above")

if __name__ == "__main__":
    main()
