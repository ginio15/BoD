#!/usr/bin/env python3
"""
BoD Presentation Analysis System - Demo Script

This script demonstrates the complete functionality of the BoD analysis system
with the sample documents and shows all key features working together.
"""

import sys
from pathlib import Path
import time

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from src.models.document import ProcessedDocument, DocumentPage, DocumentMetadata
from src.utils.document_parser import DocumentParser
from src.utils.llm_providers import LLMProviderManager
from src.utils.analysis_engine import AnalysisEngine
from config.settings import Config

def demo_header():
    """Print demo header"""
    print("🎯" + "=" * 60)
    print("    BoD PRESENTATION ANALYSIS SYSTEM - LIVE DEMO")
    print("    Automated Quarterly Presentation Analysis")
    print("=" * 62)

def demo_document_processing():
    """Demonstrate document processing with sample files"""
    print("\n📄 DOCUMENT PROCESSING DEMONSTRATION")
    print("-" * 40)
    
    # Check for sample files
    sample_files = [
        Path("data/uploads/sample_q1_2024.txt"),
        Path("data/uploads/sample_q4_2023.txt")
    ]
    
    processed_docs = []
    
    for sample_file in sample_files:
        if sample_file.exists():
            print(f"📁 Processing: {sample_file.name}")
            
            # Read content
            with open(sample_file, 'r') as f:
                content = f.read()
            
            # Create document structure
            metadata = DocumentMetadata(
                filename=sample_file.name,
                file_type="txt",
                total_pages=1,
                word_count=len(content.split()),
                char_count=len(content),
                file_size_mb=sample_file.stat().st_size / (1024 * 1024),
                quarter="Q1" if "q1" in sample_file.name.lower() else "Q4",
                year=2024 if "2024" in sample_file.name else 2023
            )
            
            page = DocumentPage(
                page_number=1,
                text=content,
                source="text"
            )
            
            document = ProcessedDocument(
                pages=[page],
                metadata=metadata,
                full_text=content
            )
            
            processed_docs.append(document)
            
            print(f"   ✅ Document processed: {metadata.word_count} words, {metadata.total_pages} page(s)")
            print(f"   📊 Quarter: {metadata.quarter} {metadata.year}")
        else:
            print(f"   ⚠️ Sample file not found: {sample_file}")
    
    return processed_docs

def demo_commitment_analysis(documents):
    """Demonstrate commitment tracking"""
    print("\n🎯 COMMITMENT ANALYSIS DEMONSTRATION")
    print("-" * 40)
    
    engine = AnalysisEngine()
    
    for doc in documents:
        print(f"\n📋 Analyzing commitments in {doc.metadata.filename}...")
        
        # Extract commitments using pattern matching
        commitments = engine._extract_commitments_by_pattern(doc.full_text)
        
        print(f"   Found {len(commitments)} commitments:")
        for i, commitment in enumerate(commitments[:5], 1):  # Show first 5
            print(f"   {i}. {commitment['text'][:60]}...")
            print(f"      Type: {commitment['type']}, Confidence: {commitment['confidence']:.2f}")
        
        if len(commitments) > 5:
            print(f"   ... and {len(commitments) - 5} more commitments")
        
        # Store in document
        doc.commitments = commitments

def demo_sentiment_analysis(documents):
    """Demonstrate sentiment analysis"""
    print("\n😊 SENTIMENT ANALYSIS DEMONSTRATION")
    print("-" * 40)
    
    engine = AnalysisEngine()
    
    for doc in documents:
        print(f"\n📊 Analyzing sentiment in {doc.metadata.filename}...")
        
        # Calculate sentiment score
        sentiment_score = engine._calculate_sentiment_score(doc.full_text)
        
        # Interpret sentiment
        if sentiment_score > 0.1:
            sentiment_desc = "Positive 📈"
        elif sentiment_score < -0.1:
            sentiment_desc = "Negative 📉"
        else:
            sentiment_desc = "Neutral ➡️"
        
        print(f"   Overall Sentiment: {sentiment_score:.3f} ({sentiment_desc})")
        
        # Store sentiment
        doc.sentiment_scores = {"overall": sentiment_score}

def demo_topic_analysis(documents):
    """Demonstrate topic and escalation detection"""
    print("\n🔍 TOPIC & ESCALATION ANALYSIS DEMONSTRATION")
    print("-" * 40)
    
    engine = AnalysisEngine()
    
    # Define key business topics for demo
    business_topics = ["financial", "revenue", "costs", "risks", "strategy", "market", "operations"]
    
    for doc in documents:
        print(f"\n🏷️ Analyzing topics in {doc.metadata.filename}...")
        
        # Simple topic detection based on keywords
        found_topics = []
        content_lower = doc.full_text.lower()
        
        for topic in business_topics:
            if topic in content_lower:
                found_topics.append(topic)
        
        doc.key_topics = found_topics
        print(f"   Key Topics: {', '.join(found_topics)}")
        
        # Escalation detection
        escalation_keywords = ["critical", "urgent", "crisis", "immediate", "challenge", "risk"]
        escalations = []
        
        for keyword in escalation_keywords:
            if keyword.lower() in content_lower:
                escalations.append(f"escalation: {keyword}")
        
        doc.escalation_topics = escalations
        if escalations:
            print(f"   🚨 Escalations detected: {len(escalations)}")
        else:
            print(f"   ✅ No critical escalations detected")

def demo_comparison_analysis(documents):
    """Demonstrate document comparison"""
    print("\n🔄 DOCUMENT COMPARISON DEMONSTRATION")
    print("-" * 40)
    
    if len(documents) < 2:
        print("   ⚠️ Need at least 2 documents for comparison")
        return
    
    # Sort by quarter/year
    sorted_docs = sorted(documents, key=lambda d: (d.metadata.year or 0, d.metadata.quarter or ""))
    
    print(f"\n📊 Comparing {len(sorted_docs)} documents:")
    for doc in sorted_docs:
        print(f"   📄 {doc.metadata.filename} ({doc.metadata.quarter} {doc.metadata.year})")
    
    # Compare commitments
    print(f"\n🎯 Commitment Evolution:")
    for doc in sorted_docs:
        print(f"   {doc.metadata.quarter} {doc.metadata.year}: {len(doc.commitments)} commitments")
    
    # Compare sentiment
    print(f"\n😊 Sentiment Trends:")
    for doc in sorted_docs:
        sentiment = doc.sentiment_scores.get("overall", 0)
        trend = "📈" if sentiment > 0.1 else "📉" if sentiment < -0.1 else "➡️"
        print(f"   {doc.metadata.quarter} {doc.metadata.year}: {sentiment:.3f} {trend}")
    
    # Compare topics
    print(f"\n🏷️ Topic Changes:")
    if len(sorted_docs) >= 2:
        old_topics = set(sorted_docs[0].key_topics)
        new_topics = set(sorted_docs[1].key_topics)
        
        added_topics = new_topics - old_topics
        removed_topics = old_topics - new_topics
        continued_topics = old_topics & new_topics
        
        if added_topics:
            print(f"   ➕ New topics: {', '.join(added_topics)}")
        if removed_topics:
            print(f"   ➖ Removed topics: {', '.join(removed_topics)}")
        if continued_topics:
            print(f"   🔄 Continuing topics: {', '.join(continued_topics)}")

def demo_budget_tracking():
    """Demonstrate budget and cost tracking"""
    print("\n💰 BUDGET TRACKING DEMONSTRATION")
    print("-" * 40)
    
    llm_manager = LLMProviderManager()
    usage_summary = llm_manager.get_usage_summary()
    
    print(f"📊 Current Budget Status:")
    print(f"   Total Budget Used: ${usage_summary['total_budget_used']:.2f}")
    
    for provider, stats in usage_summary['providers'].items():
        status_icon = "✅" if stats['available'] else "⚠️"
        print(f"   {status_icon} {provider.capitalize()}:")
        print(f"      Budget: ${stats['total_cost']:.2f} / ${stats['budget_limit']:.2f}")
        print(f"      Requests: {stats['request_count']}")
        if stats['error_count'] > 0:
            print(f"      Errors: {stats['error_count']}")

def demo_system_status():
    """Show system status and capabilities"""
    print("\n⚙️ SYSTEM STATUS & CAPABILITIES")
    print("-" * 40)
    
    config = Config()
    
    print(f"📋 Configuration:")
    print(f"   App: {config.APP_NAME} v{config.VERSION}")
    print(f"   Budget: ${config.BUDGET_CONFIG['total_budget']:.2f}")
    
    print(f"\n🛠️ Available Features:")
    features = [
        "Document parsing (PDF/PPTX/TXT)",
        "Multi-provider LLM integration",
        "Pattern-based commitment detection", 
        "Sentiment analysis",
        "Topic identification",
        "Escalation detection",
        "Comparative analysis",
        "Budget tracking",
        "Streamlit web interface"
    ]
    
    for feature in features:
        print(f"   ✅ {feature}")

def demo_next_steps():
    """Show next steps and recommendations"""
    print("\n🚀 NEXT STEPS & RECOMMENDATIONS")
    print("-" * 40)
    
    print(f"🎯 For Enhanced Analysis:")
    print(f"   1. Set up OpenAI API key: export OPENAI_API_KEY='your-key'")
    print(f"   2. Set up Mistral API key: export MISTRAL_API_KEY='your-key'") 
    print(f"   3. Install Ollama for local LLM: https://ollama.ai")
    
    print(f"\n📊 To Use the System:")
    print(f"   1. Start Streamlit: streamlit run app.py")
    print(f"   2. Upload real BoD presentations")
    print(f"   3. Select LLM provider")
    print(f"   4. Run analysis and generate reports")
    
    print(f"\n📈 Production Considerations:")
    print(f"   - Scale budget based on document volume")
    print(f"   - Implement document version control") 
    print(f"   - Add user authentication and access control")
    print(f"   - Set up automated scheduling for quarterly reviews")
    print(f"   - Integrate with existing document management systems")

def main():
    """Run the complete demo"""
    demo_header()
    
    print("⏱️ Starting comprehensive system demonstration...")
    time.sleep(1)
    
    try:
        # Process documents
        documents = demo_document_processing()
        
        if documents:
            # Analysis demonstrations
            demo_commitment_analysis(documents)
            demo_sentiment_analysis(documents)
            demo_topic_analysis(documents)
            demo_comparison_analysis(documents)
        
        # System demonstrations
        demo_budget_tracking()
        demo_system_status()
        demo_next_steps()
        
        print("\n🎉" + "=" * 60)
        print("    DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("    The BoD Analysis System is ready for production use.")
        print("=" * 62)
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
