# BoD Presentation Analysis System - Proof of Concept Development Guide

## Executive Summary

This document provides a minimal-cost proof of concept (POC) development roadmap for Olympia Group's AI-powered BoD presentation analysis system. The POC focuses on processing 2+ sample presentations to demonstrate core functionality: commitment tracking, sentiment shift detection, and topic de-escalation identification. By leveraging free/low-cost tools and local development, we validate the approach before investing in enterprise-scale solutions.

## Problem Definition & Business Context

### Core Challenge
Olympia Group processes ~10 quarterly BoD presentations (80 pages each) from subsidiaries with 48-hour turnaround requirements. Current manual analysis fails to systematically track:
- **Commitment fulfillment vs. delays** (e.g., "100% completion" → "re-evaluate all contracts")
- **Subtle sentiment shifts** (e.g., "will complete" → "hope to complete")  
- **Topic de-escalation** (detailed coverage → minimal mention or omission)

### POC Success Criteria
- Process 2+ presentation pairs with variable structures (like Project Kalamaras examples)
- Automatically detect different metric types (targets, percentages, status indicators)
- Generate analysis quality matching Olympia's "good example" standard
- Total testing budget: ≤$20 across all LLM providers
- Processing time: ≤15 minutes per presentation pair for POC

## Technical Architecture - POC Version

### Simplified Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Streamlit UI   │    │   Python Core    │    │   Document      │
│  (Local Web)    │◄──►│   Processing     │◄──►│   Pipeline      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
┌─────────────────┐    ┌──────────────────┐              │
│  Local ChromaDB │    │   LLM Services   │              │
│  (Vector Store) │◄──►│  (API Testing)   │◄─────────────┘
└─────────────────┘    └──────────────────┘
```

### Cost-Optimized Technology Stack

#### Document Processing
- **PDF Processing**: PyMuPDF (free, robust text extraction)
- **PPTX Processing**: python-pptx (free, comprehensive PowerPoint support)
- **OCR Engine**: Tesseract OCR (free, open-source) + pytesseract
- **Image Processing**: Pillow for image preprocessing before OCR

#### AI & Analysis - Multi-Provider Testing
- **LLM Option 1**: Mistral AI (free tier: 1M tokens/month)
- **LLM Option 2**: OpenAI GPT-3.5 Turbo (free credits + low cost: $0.0015/1K tokens)
- **LLM Option 3**: Local Ollama (Llama-2-13B, Mixtral-8x7B - free, runs locally)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2 (free, local)
- **Vector Database**: ChromaDB (free, local storage)

#### UI & Infrastructure  
- **Frontend**: Streamlit (free, rapid prototyping)
- **Backend**: Pure Python (no server costs)
- **Storage**: Local filesystem (no cloud costs)
- **Environment**: Local development (no hosting costs)

## Core POC Features & Implementation Priority

### Week 1: Foundation & Document Processing
**Priority 1: Document Ingestion Pipeline**
- Upload PDF/PPTX files (current + previous quarter)
- Automatic format detection and text extraction
- OCR integration for image-based slides using Tesseract
- Metadata extraction with slide/page numbering
- Basic document structure parsing

**Deliverable**: Successfully extract and structure content from Project Kalamaras-style presentations

### Week 2: LLM Integration & Testing Framework
**Priority 2: Multi-Provider LLM Setup**
- Integrate Mistral AI API (free tier testing)
- Integrate OpenAI GPT-3.5 Turbo API  
- Set up Ollama for local model testing
- Create unified LLM interface for A/B testing
- Implement cost tracking per provider

**Priority 3: Core Analysis Logic**
- Section alignment using semantic similarity (embeddings)
- Basic commitment extraction using patterns + LLM verification
- Metric type detection (targets, percentages, dates, status)

**Deliverable**: Process same presentation pair with all 3 LLM providers

### Week 3: Advanced Analysis & Comparison
**Priority 4: Commitment & Sentiment Tracking**
- Language confidence change detection ("will" → "hope to" → "considering")
- Target modification tracking ("100%" → "re-evaluate all")
- Status downgrade identification ("Done" → "Phase B" → "Not Started")
- Timeline shift detection (Sept 24 → Year End)

**Priority 5: Topic De-escalation Detection**
- Coverage depth analysis (slide count, word count per topic)
- Missing section identification
- Priority shift detection based on presentation structure

**Deliverable**: Generate analysis matching Olympia's "good example" quality

### Week 4: Dashboard & Comparative Testing
**Priority 6: Interactive Streamlit Dashboard**
- Side-by-side presentation viewer
- Tabbed analysis results (Commitments, Sentiment, De-escalation)
- Citation system with precise slide/page references
- LLM provider comparison interface
- Export functionality (PDF reports)

**Priority 7: Model Performance Comparison**
- Accuracy scoring across all providers
- Cost analysis per analysis run
- Processing time benchmarks
- Quality assessment framework

**Deliverable**: Complete POC with provider recommendations

## LLM Testing Methodology

### Testing Framework Design

#### 1. Standardized Test Cases
**Test Dataset:**
- Project Kalamaras presentation pair (slides 37 vs 61)
- 2 additional presentation pairs for validation
- Manual "ground truth" analysis for accuracy measurement

**Test Categories:**
- Commitment extraction accuracy
- Sentiment shift detection precision
- Target modification identification
- Topic de-escalation flagging
- Citation accuracy

#### 2. Provider Testing Sequence

**Phase 1: Mistral AI Testing (Week 2)**
```python
# Test configuration
MISTRAL_CONFIG = {
    "model": "mistral-small",  # Free tier
    "max_tokens": 4000,
    "temperature": 0.1,  # Low for consistent analysis
    "budget_limit": 5.00  # $5 testing budget
}
```

**Phase 2: OpenAI Testing (Week 2-3)**  
```python
# Test configuration
OPENAI_CONFIG = {
    "model": "gpt-3.5-turbo",
    "max_tokens": 4000, 
    "temperature": 0.1,
    "budget_limit": 10.00  # $10 testing budget
}
```

**Phase 3: Local Ollama Testing (Week 3-4)**
```python
# Test configuration  
OLLAMA_CONFIG = {
    "models": ["llama2:13b", "mixtral:8x7b"],
    "max_tokens": 4000,
    "temperature": 0.1,
    "cost": 0.00  # Free local processing
}
```

#### 3. Evaluation Metrics

**Accuracy Scoring:**
- **Commitment Detection Rate**: % of manually identified commitments found
- **False Positive Rate**: % of flagged items that aren't actual issues  
- **False Negative Rate**: % of issues that should have been flagged but weren't detected
- **Sentiment Accuracy**: % of correctly identified confidence changes
- **Citation Precision**: % of citations pointing to correct slide/page

**Performance Metrics:**
- Processing time per presentation pair
- Cost per analysis (API calls)
- Token usage optimization
- Error rate and reliability

**Quality Assessment:**
- Output resemblance to Olympia's "good example"
- Actionable insights generation
- Nuance detection capability
- Structured output consistency

#### 4. A/B Testing Implementation

**Comparative Analysis Setup:**
```python
def compare_llm_outputs(presentation_pair, providers=['mistral', 'openai', 'ollama']):
    results = {}
    for provider in providers:
        start_time = time.time()
        analysis = analyze_with_provider(presentation_pair, provider)
        processing_time = time.time() - start_time
        
        results[provider] = {
            'analysis': analysis,
            'processing_time': processing_time,
            'cost': calculate_cost(analysis, provider),
            'accuracy_score': evaluate_accuracy(analysis, ground_truth)
        }
    return results
```

**Scoring Matrix:**
| Provider | Accuracy | Speed | Cost | Overall Score |
|----------|----------|-------|------|---------------|
| Mistral  | TBD      | TBD   | TBD  | TBD           |
| OpenAI   | TBD      | TBD   | TBD  | TBD           |  
| Ollama   | TBD      | TBD   | $0   | TBD           |

## Implementation Details

### Document Processing Pipeline
```python
def process_presentation(file_path: str) -> ProcessedDocument:
    """
    Extract and structure content from PDF/PPTX with OCR fallback
    """
    file_type = detect_file_type(file_path)
    
    if file_type == 'pdf':
        pages = extract_pdf_content(file_path)
    elif file_type == 'pptx':
        pages = extract_pptx_content(file_path)
    
    # Apply OCR to image-heavy slides
    for page in pages:
        if page['text_density'] < 0.1:  # Mostly images
            page['text'] = apply_ocr(page['image'])
            page['source'] = 'ocr'
    
    return structure_document(pages)
```

### Commitment Extraction Logic
```python
def extract_commitments(text: str, llm_provider: str) -> List[Commitment]:
    """
    Multi-stage commitment extraction: patterns + LLM verification
    """
    # Stage 1: Pattern-based candidate identification
    patterns = [
        r"(?:will|committed to|plan to|target|goal)\s+(.{10,100}?)\s+(?:by|in|before)\s+(\w+\s+\d{4}|\d{1,2}/\d{4})",
        r"(\d{1,3}%)\s+(?:completion|target|goal)",
        r"reduce|increase|improve\s+(.{10,50}?)\s+(?:by|to)\s+(\d{1,3}%|\d+)"
    ]
    
    candidates = extract_with_patterns(text, patterns)
    
    # Stage 2: LLM verification and enhancement
    verified = verify_commitments_with_llm(candidates, text, llm_provider)
    
    return structure_commitments(verified)
```

### Sentiment Analysis Implementation
```python
def analyze_sentiment_shifts(current_text: str, previous_text: str, llm_provider: str) -> List[SentimentShift]:
    """
    Detect confidence level changes in commitment language
    """
    confidence_indicators = {
        'high': ['will', 'committed', 'ensure', 'guarantee'],
        'medium': ['plan to', 'aim to', 'target', 'expect'],
        'low': ['hope to', 'considering', 'exploring', 'may']
    }
    
    current_confidence = assess_confidence(current_text, confidence_indicators)
    previous_confidence = assess_confidence(previous_text, confidence_indicators)
    
    # Use LLM for nuanced analysis
    llm_analysis = analyze_with_llm(current_text, previous_text, 'sentiment_shift', llm_provider)
    
    return combine_analyses(current_confidence, previous_confidence, llm_analysis)
```

## Streamlit Dashboard Implementation

### Main Interface Structure
```python
import streamlit as st

def main():
    st.title("BoD Presentation Analyzer - POC")
    st.sidebar.title("Configuration")
    
    # LLM Provider Selection
    provider = st.sidebar.selectbox(
        "Select LLM Provider",
        ["mistral", "openai", "ollama", "compare_all"]
    )
    
    # Document Upload
    col1, col2 = st.columns(2)
    with col1:
        current_doc = st.file_uploader("Current Quarter", type=["pdf", "pptx"])
    with col2:
        previous_doc = st.file_uploader("Previous Quarter", type=["pdf", "pptx"])
    
    if st.button("Analyze Presentations") and current_doc and previous_doc:
        with st.spinner("Processing..."):
            results = analyze_presentations(current_doc, previous_doc, provider)
            display_results(results)

def display_results(results):
    """Display analysis results in tabbed interface"""
    
    # Executive Summary
    st.header("Executive Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Commitments Tracked", len(results['commitments']))
    col2.metric("Sentiment Shifts", len(results['sentiment_shifts']))  
    col3.metric("De-escalations", len(results['de_escalations']))
    
    # Detailed Analysis Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Commitments", "Sentiment Shifts", "Topic Changes", "Side-by-Side"])
    
    with tab1:
        display_commitment_analysis(results['commitments'])
    with tab2:
        display_sentiment_analysis(results['sentiment_shifts'])
    with tab3:
        display_topic_analysis(results['de_escalations'])
    with tab4:
        display_side_by_side_comparison(results['comparison'])
```

## Budget Breakdown & Cost Control

### POC Development Costs
- **Development Time**: Internal resource (4 weeks)
- **Software/Tools**: $0 (all open-source)

### API Testing Budget ($20 total)
- **Mistral AI**: $5 (free tier + minimal paid usage)
- **OpenAI GPT-3.5**: $10 (efficient token usage)
- **Ollama Local**: $0 (free local processing)
- **Buffer**: $5 (unexpected usage/testing)

### Cost Monitoring Implementation
```python
class CostTracker:
    def __init__(self):
        self.costs = {'mistral': 0, 'openai': 0, 'ollama': 0}
        self.limits = {'mistral': 5.00, 'openai': 10.00, 'ollama': 0}
    
    def track_usage(self, provider: str, tokens: int):
        cost = calculate_provider_cost(provider, tokens)
        self.costs[provider] += cost
        
        if self.costs[provider] > self.limits[provider]:
            raise BudgetExceededException(f"{provider} budget exceeded")
        
        return cost
```

## Success Metrics & Quality Gates

### POC Acceptance Criteria
- **Processing Success**: Successfully process Project Kalamaras-style presentations  
- **Analysis Quality**: Generate insights matching Olympia's "good example" standard
- **Provider Comparison**: Clear recommendation based on accuracy/cost/speed analysis
- **Generalization**: Handle variable presentation structures automatically
- **Citation Accuracy**: Precise slide/page references for all findings

### Quality Gates by Week
- **Week 1**: Document processing pipeline functional
- **Week 2**: All 3 LLM providers integrated and testable  
- **Week 3**: Analysis quality matches manual expectations
- **Week 4**: Complete dashboard with provider comparison

## Risk Mitigation

### Technical Risks
- **OCR Accuracy**: Test with multiple image qualities, implement preprocessing
- **LLM API Limits**: Implement rate limiting and retry logic
- **Variable Structures**: Design flexible parsing algorithms
- **Budget Overrun**: Strict cost monitoring and automatic cutoffs

### Quality Risks  
- **False Positives**: Manual validation of test cases
- **Missed Insights**: Comprehensive pattern coverage
- **Inconsistent Results**: Multiple test runs per provider
- **Poor Generalization**: Test with diverse presentation styles


## Next Steps After POC

### Decision Framework
Based on POC results, determine:
1. **Optimal LLM Provider**: Best accuracy/cost ratio
2. **Architecture Scaling**: Which components need cloud services
3. **Feature Prioritization**: Most impactful capabilities for full MVP
4. **Investment Areas**: Where additional budget yields best improvements

### Scaling Considerations
- **Multi-document Processing**: Batch processing capabilities
- **Advanced Analytics**: Historical trending, predictive insights  
- **Enterprise Integration**: Security, compliance, user management
- **Performance Optimization**: Caching, parallel processing

## Getting Started

### Environment Setup
```bash
# Create project directory
mkdir bod-analyzer-poc
cd bod-analyzer-poc

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR
# macOS: brew install tesseract
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
# Linux: sudo apt-get install tesseract-ocr

# Install Ollama (for local LLM testing)
# Visit: https://ollama.ai/download
ollama pull llama2:13b
ollama pull mixtral:8x7b

# Run the application  
streamlit run app.py
```

### API Keys Setup
```bash
# Create .env file
echo "MISTRAL_API_KEY=your_mistral_key" >> .env
echo "OPENAI_API_KEY=your_openai_key" >> .env
echo "BUDGET_LIMIT_MISTRAL=5.00" >> .env
echo "BUDGET_LIMIT_OPENAI=10.00" >> .env
```

This comprehensive POC guide provides a clear, cost-effective path to validate the core concept with minimal investment while preserving options to scale to the full enterprise solution.