#!/usr/bin/env python3
"""
Final System Test - BoD Analysis System
Tests all components working together after import fixes
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append('..')

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing Critical Imports...")
    
    try:
        from src.utils.document_parser import DocumentParser
        print("  ✅ DocumentParser")
    except Exception as e:
        print(f"  ❌ DocumentParser: {e}")
        return False
    
    try:
        from src.utils.optimized_analysis_engine import OptimizedAnalysisEngine
        print("  ✅ OptimizedAnalysisEngine")
    except Exception as e:
        print(f"  ❌ OptimizedAnalysisEngine: {e}")
        return False
    
    try:
        from src.utils.llm_providers import LLMProviderManager
        print("  ✅ LLMProviderManager")
    except Exception as e:
        print(f"  ❌ LLMProviderManager: {e}")
        return False
    
    try:
        from src.models.document import ProcessedDocument
        print("  ✅ Document Models")
    except Exception as e:
        print(f"  ❌ Document Models: {e}")
        return False
    
    try:
        from config.settings import Config
        print("  ✅ Configuration")
    except Exception as e:
        print(f"  ❌ Configuration: {e}")
        return False
    
    return True

def test_document_parsing():
    """Test document parsing functionality"""
    print("\n📄 Testing Document Parsing...")
    
    try:
        from src.utils.document_parser import DocumentParser
        
        parser = DocumentParser()
        
        # Test with sample text file
        sample_file = Path("data/uploads/sample_board_presentation_q1_2024.txt")
        if sample_file.exists():
            doc = parser.process_document(str(sample_file))
            print(f"  ✅ Parsed text document: {len(doc.full_text)} characters")
        else:
            print("  ❌ Sample text file not found")
            return False
        
        return True
    except Exception as e:
        print(f"  ❌ Document parsing failed: {e}")
        return False

def test_analysis_engine():
    """Test the optimized analysis engine"""
    print("\n🧠 Testing Analysis Engine...")
    
    try:
        from src.utils.optimized_analysis_engine import OptimizedAnalysisEngine
        
        engine = OptimizedAnalysisEngine()
        
        # Test with simple text
        test_text = """
        BOARD MEETING MINUTES - Q1 2024
        
        We commit to achieving 20% revenue growth this year.
        The board approved a $5M investment in new technology.
        Risk: Market volatility may impact our projections.
        """
        
        result = engine.analyze_document(test_text)
        
        print(f"  ✅ Analysis completed")
        print(f"  📊 Commitments: {len(result.get('commitments', []))}")
        print(f"  ⚠️  Risks: {len(result.get('risks', []))}")
        print(f"  💰 Financial: {len(result.get('financial_insights', []))}")
        print(f"  😊 Sentiment: {result.get('sentiment', 'unknown')}")
        
        return True
    except Exception as e:
        print(f"  ❌ Analysis engine failed: {e}")
        return False

def test_streamlit_app():
    """Test Streamlit app imports"""
    print("\n🌐 Testing Streamlit App...")
    
    try:
        # Read the app file and test imports
        with open('app_enhanced.py', 'r') as f:
            app_content = f.read()
        
        # Extract import section (everything before main streamlit code)
        import_section = app_content.split('st.set_page_config')[0]
        
        # Execute the import section
        exec(import_section)
        print("  ✅ All app imports successful")
        print("  ✅ Enhanced app ready to run")
        
        return True
    except Exception as e:
        print(f"  ❌ Streamlit app test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 BoD Analysis System - Final Import Test")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Document Parsing", test_document_parsing),
        ("Analysis Engine", test_analysis_engine),
        ("Streamlit App", test_streamlit_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"\n❌ {test_name} failed")
        except Exception as e:
            print(f"\n❌ {test_name} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! System is ready to use.")
        print("\n📋 Next Steps:")
        print("1. Run: streamlit run app_enhanced.py --server.port 8502")
        print("2. Open: http://localhost:8502")
        print("3. Upload sample files from data/uploads/")
        print("4. Test document analysis features")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
