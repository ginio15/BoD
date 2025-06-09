#!/bin/bash
# Launch script for BoD Presentation Analysis System

echo "🚀 Starting BoD Presentation Analysis System..."
echo "📍 Current directory: $(pwd)"
echo "🌐 Streamlit will be available at: http://localhost:8501"
echo ""

# Start the enhanced Streamlit application
streamlit run app_enhanced.py

echo ""
echo "✅ Application stopped."
