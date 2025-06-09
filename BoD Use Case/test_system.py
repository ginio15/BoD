"""
Test Script for BoD Presentation Analysis System

This script tests the core functionality of the document processing pipeline.
"""

import sys
from pathlib import Path
import tempfile
import os

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Test imports
try:
    from src.models.document import ProcessedDocument, DocumentPage, DocumentMetadata
    from src.utils.document_parser import DocumentParser, DocumentValidator
    from src.utils.llm_providers import LLMProviderManager
    from src.utils.analysis_engine import AnalysisEngine
    from config.settings import Config
    print("✅ All imports successful!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_configuration():
    """Test configuration and environment validation"""
    print("\n📋 Testing Configuration...")
    
    config = Config()
    print(f"✅ Config loaded: {config.APP_NAME} v{config.VERSION}")
    
    # Test environment validation
    env_validation = config.validate_environment()
    print("Environment validation results:")
    for key, status in env_validation.items():
        status_icon = "✅" if status else "⚠️"
        print(f"  {status_icon} {key}: {status}")

def test_llm_providers():
    """Test LLM provider initialization and availability"""
    print("\n🤖 Testing LLM Providers...")
    
    llm_manager = LLMProviderManager()
    available_providers = llm_manager.get_available_providers()
    
    print(f"Available providers: {available_providers}")
    
    # Test provider availability
    for provider_name in ["openai", "mistral", "ollama"]:
        if provider_name in llm_manager.providers:
            is_available = llm_manager.providers[provider_name].is_available()
            status_icon = "✅" if is_available else "⚠️"
            print(f"  {status_icon} {provider_name}: {is_available}")
        else:
            print(f"  ❌ {provider_name}: Not initialized")
    
    # Test usage summary
    usage_summary = llm_manager.get_usage_summary()
    print(f"Total budget used: ${usage_summary['total_budget_used']:.2f}")

def test_document_models():
    """Test document model creation and functionality"""
    print("\n📄 Testing Document Models...")
    
    # Test DocumentMetadata
    metadata = DocumentMetadata(
        filename="test_presentation.pdf",
        file_type="pdf",
        total_pages=10,
        word_count=1000,
        char_count=5000,
        file_size_mb=2.5
    )
    print(f"✅ DocumentMetadata created: {metadata.filename}")
    
    # Test DocumentPage
    page = DocumentPage(
        page_number=1,
        text="This is a test page with sample content for analysis.",
        source="text"
    )
    print(f"✅ DocumentPage created: Page {page.page_number}, {page.word_count} words")
    
    # Test ProcessedDocument
    document = ProcessedDocument(
        pages=[page],
        metadata=metadata,
        full_text=page.text
    )
    print(f"✅ ProcessedDocument created: {document.metadata.filename}")
    print(f"   - Total pages: {len(document.pages)}")
    print(f"   - Word count: {document.get_total_word_count()}")

def test_document_parser():
    """Test document parser initialization"""
    print("\n🔍 Testing Document Parser...")
    
    parser = DocumentParser()
    print("✅ DocumentParser initialized")
    
    # Test file validation
    validator = DocumentValidator()
    
    # Create a dummy test file
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
        tmp_file.write(b"dummy pdf content")
        tmp_path = tmp_file.name
    
    try:
        validation_result = validator.validate_file(tmp_path)
        print(f"✅ File validation tested: {validation_result['valid']}")
        if validation_result['errors']:
            for error in validation_result['errors']:
                print(f"   ⚠️ Error: {error}")
    finally:
        os.unlink(tmp_path)

def test_analysis_engine():
    """Test analysis engine initialization"""
    print("\n🔬 Testing Analysis Engine...")
    
    engine = AnalysisEngine()
    print("✅ AnalysisEngine initialized")
    print(f"   - Commitment patterns loaded: {len(engine.commitment_patterns)}")
    print(f"   - Sentiment keywords loaded: {len(engine.sentiment_keywords)} categories")

def test_sample_analysis():
    """Test a sample analysis workflow"""
    print("\n🧪 Testing Sample Analysis Workflow...")
    
    # Create a sample document with business content
    sample_text = """
    Board of Directors Quarterly Review - Q1 2024
    
    Financial Performance:
    We are pleased to report strong financial results for Q1 2024.
    Revenue increased by 15% compared to the same period last year.
    
    Strategic Initiatives:
    We will implement the new customer acquisition strategy by Q2 2024.
    The team is committed to achieving a 20% improvement in customer satisfaction scores.
    Our goal is to reduce operational costs by 10% over the next six months.
    
    Risk Management:
    We have identified several critical issues that require immediate attention.
    The supply chain disruption poses a significant challenge to our operations.
    We plan to diversify our supplier base to mitigate these risks.
    
    Outlook:
    We remain optimistic about our growth prospects despite current market challenges.
    The board has approved additional investment in technology infrastructure.
    """
    
    # Create sample document structure
    metadata = DocumentMetadata(
        filename="q1_2024_board_review.pdf",
        file_type="pdf",
        total_pages=1,
        word_count=len(sample_text.split()),
        char_count=len(sample_text),
        file_size_mb=0.1,
        quarter="Q1",
        year=2024
    )
    
    page = DocumentPage(
        page_number=1,
        text=sample_text,
        source="text"
    )
    
    document = ProcessedDocument(
        pages=[page],
        metadata=metadata,
        full_text=sample_text
    )
    
    print(f"✅ Sample document created: {metadata.filename}")
    print(f"   - Content: {len(sample_text)} characters, {len(sample_text.split())} words")
    
    # Test analysis engine with sample
    engine = AnalysisEngine()
    
    # Test commitment extraction (pattern-based only, no LLM)
    pattern_commitments = engine._extract_commitments_by_pattern(sample_text)
    print(f"✅ Pattern-based commitment extraction: {len(pattern_commitments)} commitments found")
    
    # Test sentiment analysis (keyword-based only)
    sentiment_score = engine._calculate_sentiment_score(sample_text)
    print(f"✅ Sentiment analysis: {sentiment_score:.3f} (range: -1 to +1)")
    
    return document

def main():
    """Run all tests"""
    print("🚀 BoD Presentation Analysis System - Test Suite")
    print("=" * 50)
    
    try:
        test_configuration()
        test_llm_providers()
        test_document_models()
        test_document_parser()
        test_analysis_engine()
        sample_doc = test_sample_analysis()
        
        print("\n" + "=" * 50)
        print("✅ All tests completed successfully!")
        print("\nSystem is ready for use. Key capabilities:")
        print("  📄 Document parsing (PDF/PPTX)")
        print("  🤖 Multi-provider LLM integration")
        print("  🔍 Commitment tracking")
        print("  📊 Sentiment analysis")
        print("  💰 Budget tracking")
        print("\nNext steps:")
        print("  1. Set up API keys for OpenAI/Mistral (optional)")
        print("  2. Install Ollama for local LLM (optional)")
        print("  3. Upload presentations via Streamlit UI")
        print("  4. Run analysis and comparison workflows")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
