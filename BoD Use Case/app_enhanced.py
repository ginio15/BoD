#!/usr/bin/env python3
"""
Enhanced BoD Analysis Streamlit App with Ollama Integration

This enhanced version includes:
1. Advanced LLM-powered analysis using Ollama
2. Comprehensive commitment tracking
3. Risk assessment capabilities
4. Financial impact analysis
5. Real-time analysis dashboard
"""

import streamlit as st
import os
import tempfile
import json
import time
from pathlib import Path
from datetime import datetime

# Import our custom modules
from src.utils.document_parser import DocumentParser
from src.utils.llm_providers import LLMProviderManager
from src.utils.enhanced_analysis_engine import EnhancedAnalysisEngine
from src.utils.optimized_analysis_engine import OptimizedAnalysisEngine
from src.models.document import ProcessedDocument, DocumentMetadata, DocumentPage
from config.settings import Config

# Page configuration
st.set_page_config(
    page_title="Enhanced BoD Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables"""
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None
    if "processing_time" not in st.session_state:
        st.session_state.processing_time = 0
    if "total_cost" not in st.session_state:
        st.session_state.total_cost = 0.0

def create_sample_document():
    """Create a sample document for demo purposes"""
    sample_content = """
    BOARD MEETING MINUTES - Q4 2023 STRATEGIC REVIEW
    
    FINANCIAL PERFORMANCE:
    Q4 revenue reached $2.5M, representing 15% year-over-year growth and exceeding our 
    target of $2.3M. Net profit margin improved to 12% from 8% in Q4 2022. We maintained 
    positive cash flow for the third consecutive quarter at $400K.
    
    STRATEGIC COMMITMENTS FOR 2024:
    1. Cost Optimization: We will reduce operational expenses by 10% by Q2 2024
    2. Product Launch: Committed to launching new AI analytics platform in Q3 2024
    3. Market Expansion: Target European market entry by December 2024 with $500K investment
    4. Customer Success: Improve satisfaction scores from 75% to 85% by end of 2024
    
    RISK ASSESSMENT:
    High Priority: Supply chain disruptions may impact Q1 delivery schedules
    Medium Priority: Currency fluctuations could affect European expansion costs
    Low Priority: Regulatory changes in data privacy laws require monitoring
    
    FINANCIAL PROJECTIONS:
    Q1 2024 target revenue: $2.8M
    Full year 2024: Projecting 20% revenue growth to $12M
    R&D investment: Increase to 15% of revenue
    
    The board expressed cautious optimism about 2024 growth prospects while acknowledging 
    the need for careful risk management and operational excellence.
    """
    
    metadata = DocumentMetadata(
        filename="Sample_Q4_2023_Board_Minutes.txt",
        file_type="txt",
        total_pages=1
    )
    
    page = DocumentPage(page_number=1, text=sample_content)
    
    return ProcessedDocument(
        pages=[page],
        metadata=metadata,
        full_text=sample_content
    )

def analyze_document_enhanced(document, provider="ollama"):
    """Run enhanced analysis on a document"""
    # Use OptimizedAnalysisEngine for Ollama to prevent timeouts
    if provider.lower() == "ollama":
        engine = OptimizedAnalysisEngine()
    else:
        engine = EnhancedAnalysisEngine()
    
    with st.spinner(f"🔍 Running enhanced analysis with {provider}..."):
        start_time = time.time()
        if provider.lower() == "ollama":
            results = engine.analyze_document_optimized(document, provider)
        else:
            results = engine.analyze_document_enhanced(document, provider)
        processing_time = time.time() - start_time
    
    return results, processing_time

def display_analysis_results(results, processing_time):
    """Display comprehensive analysis results"""
    
    st.success(f"✅ Analysis completed in {processing_time:.1f} seconds")
    
    # Overview metrics
    st.subheader("📊 Analysis Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        commitments_count = len(results.get("enhanced_commitments", []))
        st.metric("Commitments Found", commitments_count)
    
    with col2:
        risks_count = len(results.get("risk_assessment", []))
        st.metric("Risks Identified", risks_count)
    
    with col3:
        financial_count = len(results.get("financial_insights", []))
        st.metric("Financial Insights", financial_count)
    
    with col4:
        priorities_count = len(results.get("strategic_priorities", []))
        st.metric("Strategic Priorities", priorities_count)
    
    # Detailed analysis tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🎯 Commitments", "⚠️ Risks", "💰 Financial", "📈 Sentiment", "🎯 Strategy", "📋 Summary"
    ])
    
    with tab1:
        display_commitments(results.get("enhanced_commitments", []))
    
    with tab2:
        display_risks(results.get("risk_assessment", []))
    
    with tab3:
        display_financial_insights(results.get("financial_insights", []))
    
    with tab4:
        display_sentiment_analysis(results.get("sentiment_analysis", {}))
    
    with tab5:
        display_strategic_priorities(results.get("strategic_priorities", []))
    
    with tab6:
        display_executive_summary(results.get("executive_summary", ""))

def display_commitments(commitments):
    """Display enhanced commitments analysis"""
    st.subheader("🎯 Enhanced Commitments Analysis")
    
    if not commitments:
        st.info("No commitments found in the document.")
        return
    
    # Commitment categories
    categories = {}
    for commitment in commitments:
        cat = commitment.get("category", "unknown")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(commitment)
    
    # Display by category
    for category, cat_commitments in categories.items():
        with st.expander(f"📌 {category.title()} Commitments ({len(cat_commitments)})"):
            for i, commitment in enumerate(cat_commitments, 1):
                st.markdown(f"**{i}. {commitment.get('exact_text', 'N/A')[:100]}...**")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.caption(f"🎯 **Deadline:** {commitment.get('deadline', 'Not specified')}")
                    st.caption(f"📊 **Metric:** {commitment.get('quantifiable_metric', 'Not specified')}")
                    st.caption(f"💪 **Confidence:** {commitment.get('confidence_level', 'medium')}")
                
                with col2:
                    st.caption(f"👤 **Stakeholder:** {commitment.get('stakeholder', 'Not specified')}")
                    risks = commitment.get('risk_factors', [])
                    if risks:
                        st.caption(f"⚠️ **Risks:** {', '.join(risks[:2])}...")
                
                st.markdown("---")

def display_risks(risks):
    """Display risk assessment"""
    st.subheader("⚠️ Risk Assessment")
    
    if not risks:
        st.info("No specific risks identified in the document.")
        return
    
    # Risk level distribution
    risk_levels = {"high": [], "medium": [], "low": []}
    for risk in risks:
        level = risk.get("risk_level", "medium").lower()
        if level in risk_levels:
            risk_levels[level].append(risk)
    
    # Display by risk level
    for level, level_risks in risk_levels.items():
        if level_risks:
            color = {"high": "🔴", "medium": "🟡", "low": "🟢"}[level]
            with st.expander(f"{color} {level.title()} Risk ({len(level_risks)} risks)"):
                for i, risk in enumerate(level_risks, 1):
                    st.markdown(f"**{i}. {risk.get('risk_description', 'N/A')[:80]}...**")
                    st.caption(f"📂 **Category:** {risk.get('category', 'N/A')}")
                    st.caption(f"💥 **Impact:** {risk.get('potential_impact', 'Not specified')[:100]}...")
                    
                    mitigation = risk.get('mitigation_mentioned', False)
                    st.caption(f"🛡️ **Mitigation:** {'Yes' if mitigation else 'No'}")
                    st.markdown("---")

def display_financial_insights(insights):
    """Display financial insights"""
    st.subheader("💰 Financial Insights")
    
    if not insights:
        st.info("No financial insights extracted.")
        return
    
    # Create HTML table for better display
    if insights:
        # Display summary metrics in columns
        st.subheader("📊 Financial Metrics Overview")
        
        for i, insight in enumerate(insights, 1):
            with st.container():
                st.markdown(f"**{i}. {insight.get('metric_type', 'Unknown Metric')}**")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Current Value", insight.get("current_value", "N/A"))
                with col2:
                    st.metric("Target Value", insight.get("target_value", "N/A"))
                with col3:
                    trend = insight.get("trend", "N/A")
                    st.metric("Trend", trend)
                with col4:
                    significance = insight.get("significance", "N/A")
                    st.metric("Significance", significance)
                
                st.markdown("---")
    
    # Detailed view
    with st.expander("📊 Detailed Financial Analysis"):
        for i, insight in enumerate(insights, 1):
            st.markdown(f"**{i}. {insight.get('metric_type', 'Unknown Metric')}**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.caption(f"📈 **Current:** {insight.get('current_value', 'N/A')}")
            with col2:
                st.caption(f"🎯 **Target:** {insight.get('target_value', 'N/A')}")
            with col3:
                st.caption(f"📊 **Trend:** {insight.get('trend', 'N/A')}")
            
            context = insight.get('context', '')
            if context:
                st.caption(f"📝 **Context:** {context[:100]}...")
            st.markdown("---")

def display_sentiment_analysis(sentiment):
    """Display sentiment analysis results"""
    st.subheader("😊 Sentiment Analysis")
    
    if not sentiment:
        st.info("No sentiment analysis results available.")
        return
    
    # Overall sentiment
    overall = sentiment.get("overall_sentiment", "unknown")
    confidence = sentiment.get("overall_confidence", "N/A")
    
    col1, col2 = st.columns(2)
    with col1:
        sentiment_emoji = {
            "positive": "😊", "negative": "😟", 
            "neutral": "😐", "mixed": "😕"
        }.get(overall, "❓")
        st.metric("Overall Sentiment", f"{sentiment_emoji} {overall.title()}")
    
    with col2:
        st.metric("Confidence Level", f"{confidence}/10" if confidence != "N/A" else "N/A")
    
    # Topic sentiments
    topic_sentiments = sentiment.get("topic_sentiments", {})
    if topic_sentiments:
        st.subheader("📊 Topic-Specific Sentiment")
        for topic, score in topic_sentiments.items():
            if isinstance(score, (int, float)):
                sentiment_bar = "🟢" if score > 0.3 else "🟡" if score > -0.3 else "🔴"
                st.write(f"{sentiment_bar} **{topic}:** {score:.2f}")
    
    # Leadership tone
    leadership_tone = sentiment.get("leadership_tone", "")
    if leadership_tone:
        st.subheader("👔 Leadership Tone")
        st.write(f"**Tone:** {leadership_tone}")

def display_strategic_priorities(priorities):
    """Display strategic priorities"""
    st.subheader("🎯 Strategic Priorities")
    
    if not priorities:
        st.info("No strategic priorities identified.")
        return
    
    for i, priority in enumerate(priorities, 1):
        with st.expander(f"🎯 Priority {i}: {priority.get('priority_name', 'Unnamed Priority')}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.caption(f"📂 **Category:** {priority.get('category', 'N/A')}")
                st.caption(f"⭐ **Importance:** {priority.get('importance_level', 'N/A')}")
                st.caption(f"⏰ **Timeline:** {priority.get('timeline', 'N/A')}")
            
            with col2:
                resources = priority.get('resources_mentioned', 'N/A')
                st.caption(f"💰 **Resources:** {resources}")
                metrics = priority.get('success_metrics', 'N/A')
                st.caption(f"📊 **Success Metrics:** {metrics}")
            
            challenges = priority.get('challenges', '')
            if challenges:
                st.caption(f"⚠️ **Challenges:** {challenges}")

def display_executive_summary(summary):
    """Display executive summary"""
    st.subheader("📋 Executive Summary")
    
    if not summary:
        st.info("No executive summary generated.")
        return
    
    st.markdown(summary)

def main():
    """Main enhanced application function"""
    initialize_session_state()
    
    # Title and description
    st.title("🚀 Enhanced BoD Presentation Analyzer")
    st.markdown("**AI-Powered Analysis** with Ollama Integration - Advanced insights for board presentations")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # LLM Provider selection
        provider = st.selectbox(
            "Select AI Provider",
            ["ollama", "openai", "mistral"],
            index=0,
            help="Ollama is free and runs locally!"
        )
        
        # Model selection for Ollama
        if provider == "ollama":
            model = st.selectbox(
                "Ollama Model",
                ["llama3.2:3b", "llama2:13b"],
                help="Choose the local AI model"
            )
        
        # Analysis options
        st.subheader("🔍 Analysis Options")
        enhance_analysis = st.checkbox("Enhanced Analysis", value=True, help="Use advanced AI-powered analysis")
        
        # Processing options
        st.subheader("⚙️ Processing Options")
        confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.7)
        
        # System status
        st.subheader("🖥️ System Status")
        llm_manager = LLMProviderManager()
        available_providers = llm_manager.get_available_providers()
        
        for prov in ["ollama", "openai", "mistral"]:
            status = "🟢" if prov in available_providers else "🔴"
            st.caption(f"{status} {prov.title()}")
    
    # Main content
    st.subheader("📄 Document Analysis")
    
    # Input options
    input_method = st.radio(
        "Choose input method:",
        ["Upload Document", "Use Sample Document", "Paste Text"],
        horizontal=True
    )
    
    document = None
    
    if input_method == "Upload Document":
        uploaded_file = st.file_uploader(
            "Upload board presentation",
            type=["pdf", "pptx", "txt"],
            help="Upload your board presentation for analysis"
        )
        
        if uploaded_file:
            st.success(f"✅ Loaded: {uploaded_file.name}")
            
            # Process the uploaded file
            try:
                with st.spinner("📄 Processing uploaded document..."):
                    # Save uploaded file temporarily
                    import tempfile
                    from pathlib import Path
                    
                    suffix = Path(uploaded_file.name).suffix
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix, prefix="uploaded_")
                    temp_file.write(uploaded_file.getvalue())
                    temp_file.close()
                    
                    # Parse the document
                    parser = DocumentParser()
                    document = parser.process_document(temp_file.name, use_ocr=True)
                    
                    # Clean up temporary file
                    import os
                    os.unlink(temp_file.name)
                    
                    st.success(f"✅ Document processed: {document.metadata.word_count} words extracted")
                    
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
                document = None
    
    elif input_method == "Use Sample Document":
        if st.button("📋 Load Sample Document"):
            document = create_sample_document()
            st.success("✅ Sample document loaded")
    
    elif input_method == "Paste Text":
        text_input = st.text_area(
            "Paste board presentation text:",
            height=200,
            placeholder="Paste your board presentation content here..."
        )
        
        if text_input and st.button("📝 Analyze Text"):
            metadata = DocumentMetadata(
                filename="Pasted_Text.txt",
                file_type="txt",
                total_pages=1
            )
            page = DocumentPage(page_number=1, text=text_input)
            document = ProcessedDocument(pages=[page], metadata=metadata, full_text=text_input)
    
    # Analysis button and results
    if document:
        st.markdown("---")
        
        if st.button("🚀 Run Enhanced Analysis", type="primary"):
            try:
                results, processing_time = analyze_document_enhanced(document, provider)
                st.session_state.analysis_results = results
                st.session_state.processing_time = processing_time
                
                display_analysis_results(results, processing_time)
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                st.exception(e)
    
    # Display cached results if available
    elif st.session_state.analysis_results:
        st.markdown("---")
        st.info("📊 Showing previous analysis results")
        display_analysis_results(
            st.session_state.analysis_results, 
            st.session_state.processing_time
        )
    
    # Footer
    st.markdown("---")
    st.caption("🔬 Enhanced BoD Analysis System - Powered by Ollama & Streamlit")

if __name__ == "__main__":
    main()
