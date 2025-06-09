#!/usr/bin/env python3
"""
BoD Presentation Analysis System - Proof of Concept
Main Streamlit Application

This application provides automated analysis of Board of Directors presentations,
tracking commitments, sentiment shifts, and topic de-escalation across quarters.
"""

import streamlit as st
import os
import tempfile
from pathlib import Path
import pandas as pd
from datetime import datetime

# Import our custom modules
from src.utils.document_parser import DocumentParser
from src.utils.llm_providers import LLMProviderManager
from src.utils.analysis_engine import AnalysisEngine
from src.utils.optimized_analysis_engine import OptimizedAnalysisEngine
from src.models.document import ProcessedDocument
from config.settings import Config

# Page configuration
st.set_page_config(
    page_title="BoD Presentation Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application function"""
    
    # Title and description
    st.title("📊 BoD Presentation Analysis System")
    st.markdown("**Proof of Concept** - Automated quarterly presentation comparison and insights")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # LLM Provider selection
        provider = st.selectbox(
            "Select LLM Provider",
            ["mistral", "openai", "ollama", "compare_all"],
            help="Choose the AI provider for analysis"
        )
        
        # Analysis options
        st.subheader("Analysis Options")
        analyze_commitments = st.checkbox("Track Commitments", value=True)
        analyze_sentiment = st.checkbox("Detect Sentiment Shifts", value=True)
        analyze_deescalation = st.checkbox("Find Topic De-escalation", value=True)
        
        # Processing options
        st.subheader("Processing Options")
        use_ocr = st.checkbox("Enable OCR for Images", value=True)
        confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.7)
        
        # Budget tracking
        st.subheader("💰 Budget Tracking")
        if "total_cost" not in st.session_state:
            st.session_state.total_cost = 0.0
        st.metric("Total API Cost", f"${st.session_state.total_cost:.2f}")
        st.progress(min(st.session_state.total_cost / 20.0, 1.0))  # $20 budget
        
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Previous Quarter Presentation")
        previous_file = st.file_uploader(
            "Upload previous quarter presentation",
            type=["pdf", "pptx"],
            key="previous_file",
            help="Upload the previous quarter's BoD presentation"
        )
        
        if previous_file:
            st.success(f"✅ Loaded: {previous_file.name}")
            st.caption(f"Size: {previous_file.size / 1024:.1f} KB")
    
    with col2:
        st.subheader("📄 Current Quarter Presentation")
        current_file = st.file_uploader(
            "Upload current quarter presentation",
            type=["pdf", "pptx"],
            key="current_file",
            help="Upload the current quarter's BoD presentation"
        )
        
        if current_file:
            st.success(f"✅ Loaded: {current_file.name}")
            st.caption(f"Size: {current_file.size / 1024:.1f} KB")
    
    # Analysis button
    if previous_file and current_file:
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔍 Analyze Presentations", type="primary", use_container_width=True):
                run_analysis(previous_file, current_file, provider, {
                    'commitments': analyze_commitments,
                    'sentiment': analyze_sentiment,
                    'deescalation': analyze_deescalation,
                    'use_ocr': use_ocr,
                    'confidence_threshold': confidence_threshold
                })
    
    # Display results if available
    if "analysis_results" in st.session_state:
        display_results(st.session_state.analysis_results)

def run_analysis(previous_file, current_file, provider, options):
    """Run the analysis on uploaded presentations"""
    
    try:
        with st.spinner("🔄 Processing presentations..."):
            # Initialize components
            parser = DocumentParser()
            llm_manager = LLMProviderManager()
            
            # Use OptimizedAnalysisEngine for Ollama to prevent timeouts
            if provider.lower() == "ollama":
                analyzer = OptimizedAnalysisEngine(llm_manager)
            else:
                analyzer = AnalysisEngine(llm_manager)
            
            # Save uploaded files temporarily
            previous_path = save_uploaded_file(previous_file, "previous")
            current_path = save_uploaded_file(current_file, "current")
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Parse documents
            status_text.text("📄 Parsing documents...")
            progress_bar.progress(20)
            
            previous_doc = parser.process_document(previous_path, use_ocr=options['use_ocr'])
            current_doc = parser.process_document(current_path, use_ocr=options['use_ocr'])
            
            # Step 2: Run analysis
            status_text.text("🔍 Analyzing content...")
            progress_bar.progress(60)
            
            results = analyzer.compare_documents(
                previous_doc, 
                current_doc, 
                provider=provider,
                options=options
            )
            
            # Step 3: Finalize
            status_text.text("✅ Analysis complete!")
            progress_bar.progress(100)
            
            # Store results
            st.session_state.analysis_results = results
            
            # Update cost tracking
            if 'cost' in results:
                st.session_state.total_cost += results['cost']
            
            # Clean up temporary files
            os.unlink(previous_path)
            os.unlink(current_path)
            
            status_text.empty()
            progress_bar.empty()
            st.success("🎉 Analysis completed successfully!")
            
    except Exception as e:
        st.error(f"❌ Error during analysis: {str(e)}")
        st.exception(e)

def save_uploaded_file(uploaded_file, prefix):
    """Save uploaded file to temporary location"""
    suffix = Path(uploaded_file.name).suffix
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix, prefix=f"{prefix}_")
    temp_file.write(uploaded_file.getvalue())
    temp_file.close()
    return temp_file.name

def display_results(results):
    """Display analysis results in tabbed interface"""
    
    st.markdown("---")
    st.header("📊 Analysis Results")
    
    # Executive Summary
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        commitments_count = len(results.get('commitments', []))
        st.metric("Commitments Tracked", commitments_count)
    
    with col2:
        sentiment_shifts = len(results.get('sentiment_shifts', []))
        st.metric("Sentiment Shifts", sentiment_shifts)
    
    with col3:
        deescalations = len(results.get('deescalations', []))
        st.metric("Topic De-escalations", deescalations)
    
    with col4:
        processing_time = results.get('processing_time', 0)
        st.metric("Processing Time", f"{processing_time:.1f}s")
    
    # Detailed analysis tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Executive Summary", 
        "🎯 Commitments", 
        "💭 Sentiment Shifts", 
        "📉 Topic Changes",
        "🔄 Side-by-Side"
    ])
    
    with tab1:
        display_executive_summary(results)
    
    with tab2:
        display_commitments_analysis(results.get('commitments', []))
    
    with tab3:
        display_sentiment_analysis(results.get('sentiment_shifts', []))
    
    with tab4:
        display_topic_analysis(results.get('deescalations', []))
    
    with tab5:
        display_side_by_side_comparison(results)

def display_executive_summary(results):
    """Display executive summary of findings"""
    
    st.subheader("🎯 Key Findings")
    
    # High-level insights
    insights = results.get('executive_summary', {})
    
    if insights.get('critical_issues'):
        st.error("🚨 **Critical Issues Identified**")
        for issue in insights['critical_issues']:
            st.markdown(f"- {issue}")
    
    if insights.get('important_changes'):
        st.warning("⚠️ **Important Changes**")
        for change in insights['important_changes']:
            st.markdown(f"- {change}")
    
    if insights.get('positive_developments'):
        st.success("✅ **Positive Developments**")
        for development in insights['positive_developments']:
            st.markdown(f"- {development}")
    
    # Provider comparison if available
    if results.get('provider_comparison'):
        st.subheader("🔧 LLM Provider Performance")
        comparison_df = pd.DataFrame(results['provider_comparison'])
        st.dataframe(comparison_df)

def display_commitments_analysis(commitments):
    """Display commitment tracking results"""
    
    if not commitments:
        st.info("No commitments were identified in the analysis.")
        return
    
    st.subheader("🎯 Commitment Tracking Results")
    
    for i, commitment in enumerate(commitments):
        status_color = {
            'fulfilled': '🟢',
            'delayed': '🟡', 
            'modified': '🟠',
            'abandoned': '🔴'
        }.get(commitment.get('status', 'unknown'), '⚪')
        
        with st.expander(f"{status_color} **{commitment.get('status', 'Unknown').title()}**: {commitment.get('text', '')[:80]}..."):
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Previous Quarter:**")
                st.markdown(commitment.get('previous_text', 'N/A'))
                
            with col2:
                st.markdown("**Current Quarter:**")
                st.markdown(commitment.get('current_text', 'N/A'))
            
            st.markdown(f"**Analysis:** {commitment.get('analysis', 'No analysis available')}")
            st.markdown(f"**Citation:** {commitment.get('citation', 'No citation available')}")
            
            # Confidence scoring
            confidence = commitment.get('confidence', 0)
            st.progress(confidence)
            st.caption(f"Confidence: {confidence:.1%}")

def display_sentiment_analysis(sentiment_shifts):
    """Display sentiment shift analysis"""
    
    if not sentiment_shifts:
        st.info("No significant sentiment shifts were detected.")
        return
    
    st.subheader("💭 Sentiment Shift Analysis")
    
    for shift in sentiment_shifts:
        direction = shift.get('direction', 'neutral')
        direction_icon = {
            'positive': '📈',
            'negative': '📉',
            'neutral': '➡️'
        }.get(direction, '➡️')
        
        with st.expander(f"{direction_icon} **{direction.title()} Shift**: {shift.get('topic', '')[:60]}..."):
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Before:**")
                st.markdown(f"*Confidence: {shift.get('previous_confidence', 'Unknown')}*")
                st.markdown(shift.get('previous_text', 'N/A'))
                
            with col2:
                st.markdown("**After:**")
                st.markdown(f"*Confidence: {shift.get('current_confidence', 'Unknown')}*")
                st.markdown(shift.get('current_text', 'N/A'))
            
            st.markdown(f"**Impact:** {shift.get('impact_analysis', 'No analysis available')}")
            st.markdown(f"**Citation:** {shift.get('citation', 'No citation available')}")

def display_topic_analysis(deescalations):
    """Display topic de-escalation analysis"""
    
    if not deescalations:
        st.info("No topic de-escalations were detected.")
        return
    
    st.subheader("📉 Topic De-escalation Analysis")
    
    for deesc in deescalations:
        severity = deesc.get('severity', 'medium')
        severity_icon = {
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢'
        }.get(severity, '🟡')
        
        with st.expander(f"{severity_icon} **{severity.title()} Priority**: {deesc.get('topic', '')[:60]}..."):
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Previous Coverage:**")
                st.markdown(f"Pages/Slides: {deesc.get('previous_coverage', 'N/A')}")
                st.markdown(f"Word Count: {deesc.get('previous_word_count', 'N/A')}")
                
            with col2:
                st.markdown("**Current Coverage:**")
                st.markdown(f"Pages/Slides: {deesc.get('current_coverage', 'N/A')}")
                st.markdown(f"Word Count: {deesc.get('current_word_count', 'N/A')}")
            
            st.markdown(f"**Possible Reasons:** {deesc.get('analysis', 'No analysis available')}")
            st.markdown(f"**Recommendation:** {deesc.get('recommendation', 'No recommendation available')}")

def display_side_by_side_comparison(results):
    """Display side-by-side document comparison"""
    
    st.subheader("🔄 Side-by-Side Comparison")
    
    # Document metadata
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Previous Quarter")
        prev_meta = results.get('previous_metadata', {})
        st.write(f"**Slides/Pages:** {prev_meta.get('total_pages', 'N/A')}")
        st.write(f"**Word Count:** {prev_meta.get('word_count', 'N/A')}")
        
    with col2:
        st.markdown("### Current Quarter")
        curr_meta = results.get('current_metadata', {})
        st.write(f"**Slides/Pages:** {curr_meta.get('total_pages', 'N/A')}")
        st.write(f"**Word Count:** {curr_meta.get('word_count', 'N/A')}")
    
    # Export functionality
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("📥 Export to CSV"):
            csv_data = generate_csv_export(results)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"bod_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📄 Export Report"):
            # TODO: Implement PDF report generation
            st.info("PDF export feature coming soon!")
    
    with col3:
        if st.button("🔄 Restart Analysis"):
            # Clear session state
            for key in list(st.session_state.keys()):
                if key.startswith(('analysis_', 'total_cost')):
                    del st.session_state[key]
            st.rerun()

def generate_csv_export(results):
    """Generate CSV export of analysis results"""
    
    export_data = []
    
    # Add commitments
    for commitment in results.get('commitments', []):
        export_data.append({
            'Type': 'Commitment',
            'Status': commitment.get('status', ''),
            'Description': commitment.get('text', ''),
            'Previous': commitment.get('previous_text', ''),
            'Current': commitment.get('current_text', ''),
            'Citation': commitment.get('citation', ''),
            'Confidence': commitment.get('confidence', 0)
        })
    
    # Add sentiment shifts
    for shift in results.get('sentiment_shifts', []):
        export_data.append({
            'Type': 'Sentiment Shift',
            'Status': shift.get('direction', ''),
            'Description': shift.get('topic', ''),
            'Previous': shift.get('previous_text', ''),
            'Current': shift.get('current_text', ''),
            'Citation': shift.get('citation', ''),
            'Confidence': shift.get('confidence', 0)
        })
    
    # Convert to CSV
    df = pd.DataFrame(export_data)
    return df.to_csv(index=False)

if __name__ == "__main__":
    main()
