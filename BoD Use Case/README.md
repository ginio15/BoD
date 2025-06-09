# BoD Presentation Analysis System - Proof of Concept

An automated Board of Directors presentation analysis system that tracks commitments, analyzes sentiment shifts, and detects topic de-escalation across quarterly presentations.

## 🚀 Quick Start

### 1. Launch the Application
```bash
cd "/Users/ginio/projects/BoD Use Case"
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### 2. Test the System
Run the comprehensive test suite to verify all components:
```bash
python test_system.py
```

## 📋 Current Status

### ✅ Completed Features
- **Document Processing**: PDF and PPTX parsing with OCR support
- **Multi-LLM Integration**: OpenAI, Mistral, and Ollama providers
- **Commitment Tracking**: Pattern-based detection with LLM verification
- **Sentiment Analysis**: Keyword-based and LLM-enhanced analysis
- **Budget Management**: Cost tracking across providers ($20 PoC budget)
- **Streamlit UI**: File upload, provider selection, analysis results
- **Test Framework**: Comprehensive testing and validation

### 🔄 Core Capabilities Ready
1. **Document Upload & Processing**
   - Support for PDF and PowerPoint presentations
   - **Enhanced OCR for screenshot-based PPTX files** ✨
   - Image extraction and processing from presentation slides
   - Metadata extraction and validation

2. **Commitment Analysis**
   - Pattern-based commitment detection (7 different patterns)
   - Confidence scoring and categorization
   - Time-bound commitment tracking

3. **Sentiment Analysis**
   - Page-by-page sentiment scoring
   - Topic-specific sentiment tracking
   - Trend analysis across documents

4. **Multi-Provider LLM Support**
   - OpenAI GPT integration
   - Mistral AI integration  
   - Local Ollama support
   - Cost tracking and budget limits

5. **Enhanced OCR Capabilities** ✨
   - **Screenshot-based presentation processing**
   - Optimized for image-heavy PPTX files
   - Presentation-specific text cleaning and corrections
   - High-accuracy extraction from Project Kalamaras-style content

## 🔧 Setup Instructions

### Environment Variables (Optional)
For full LLM functionality, set up API keys:
```bash
export OPENAI_API_KEY="your-openai-key"
export MISTRAL_API_KEY="your-mistral-key"
```

### Local LLM (Optional)
Install Ollama for free local processing:
```bash
# Install Ollama from https://ollama.ai
ollama pull llama2:13b
ollama pull mixtral:8x7b
```

## 📊 Usage Workflow

1. **Upload Presentations**: Use the Streamlit interface to upload PDF/PPTX files
2. **Select Provider**: Choose between OpenAI, Mistral, or Ollama for analysis
3. **Configure Analysis**: Set analysis options (commitments, sentiment, topics)
4. **Run Analysis**: Process documents with real-time progress tracking
5. **Review Results**: View structured analysis results with export options
6. **Compare Documents**: Upload multiple presentations for comparative analysis

## 🎯 Analysis Features

### Commitment Tracking
- **Future Commitments**: "We will", "We plan to", "We commit to"
- **Time-bound Goals**: Commitments with specific deadlines
- **Action Items**: Deliverables and implementation tasks
- **Target Metrics**: Specific percentage or numerical goals

### Sentiment Analysis
- **Overall Document Sentiment**: Aggregate sentiment scoring
- **Page-by-Page Analysis**: Detailed sentiment progression  
- **Topic-Specific Sentiment**: Sentiment by business area
- **Escalation Detection**: Identification of urgent/critical issues

### Document Comparison
- **Commitment Fulfillment**: Track promise completion across quarters
- **Sentiment Trends**: Monitor sentiment changes over time
- **Topic Evolution**: Analyze how topics develop and change
- **De-escalation Tracking**: Identify resolved or improving issues

## 💰 Budget Management

The PoC operates with a $20 budget allocated across providers:
- **Mistral**: $5 budget (cost-effective for most tasks)
- **OpenAI**: $10 budget (high-quality analysis)
- **Ollama**: Free (local processing, no API costs)

Real-time budget tracking prevents overspend and suggests provider optimization.

## 🔍 Testing Results

Latest test results show:
- ✅ All core modules importing successfully
- ✅ Document models and parsing functional
- ✅ Pattern-based commitment detection working (7 commitments found in sample)
- ✅ Sentiment analysis operational
- ✅ Budget tracking active
- ✅ Directory structure created
- ⚠️ API keys not configured (optional for basic functionality)

## 📁 Project Structure

```
BoD Use Case/
├── app.py                    # Main Streamlit application
├── test_system.py           # Comprehensive test suite
├── requirements.txt         # Python dependencies
├── config/
│   └── settings.py         # Configuration management
├── src/
│   ├── models/
│   │   └── document.py     # Document data structures
│   └── utils/
│       ├── document_parser.py    # PDF/PPTX processing
│       ├── llm_providers.py     # Multi-LLM integration
│       └── analysis_engine.py   # Core analysis logic
└── data/
    ├── uploads/            # Input files
    ├── processed/          # Processed documents
    └── outputs/           # Analysis results
```

## 🚀 Next Steps

1. **Upload Test Documents**: Try the system with real BoD presentations
2. **API Integration**: Set up OpenAI or Mistral keys for enhanced analysis
3. **Ollama Setup**: Install local LLM for cost-free processing
4. **Comparative Analysis**: Upload multiple quarters for trend analysis
5. **Export & Reporting**: Generate analysis reports for stakeholders

## 🛠️ Development Status

**Current Phase**: Proof of Concept ✅ Complete
**Next Phase**: Production scaling and refinement
**Timeline**: Ready for immediate testing and evaluation

The system successfully demonstrates all core capabilities for automated BoD presentation analysis, with a robust foundation for scaling to full production use.
