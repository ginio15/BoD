"""
Sample Document Creator for BoD Analysis System
Creates test documents in various formats for testing the analysis pipeline.
"""

from pathlib import Path
import sys

# Add project root to path
sys.path.append(str(Path(__file__).parent))

def create_sample_content():
    """Create sample BoD presentation content"""
    return """
OLYMPIA GROUP
BOARD OF DIRECTORS QUARTERLY REVIEW
Q1 2024

EXECUTIVE SUMMARY
We are pleased to present our Q1 2024 results to the Board of Directors.
This quarter demonstrated strong performance across key business areas despite ongoing market challenges.

FINANCIAL PERFORMANCE
• Revenue: $125M (+15% YoY)
• EBITDA: $28M (+12% YoY) 
• Net Income: $18M (+8% YoY)
• Cash Position: $45M (stable)

We exceeded our revenue target of $120M and remain on track for our annual goal of $500M.

STRATEGIC INITIATIVES
1. CUSTOMER ACQUISITION
   - We will implement the new digital marketing strategy by Q2 2024
   - Target: Increase customer base by 25% over next 6 months
   - Investment: $2M approved for technology platform upgrade

2. OPERATIONAL EFFICIENCY  
   - We are committed to reducing operational costs by 10% through automation
   - Timeline: Full implementation by end of Q3 2024
   - Expected savings: $3M annually

3. MARKET EXPANSION
   - We plan to enter two new geographic markets in Q2
   - Investment required: $5M for market entry
   - Revenue target: $15M additional revenue by Q4

RISK MANAGEMENT
CRITICAL ISSUES REQUIRING ATTENTION:
• Supply chain disruption affecting 15% of operations
• Regulatory changes in European markets pose compliance challenges  
• Cybersecurity threats have increased 40% this quarter

MITIGATION STRATEGIES:
- We will diversify supplier base by Q2 2024
- Compliance team expansion approved (3 new hires)
- Enhanced cybersecurity protocols to be implemented immediately

HUMAN RESOURCES
• Headcount: 1,250 employees (+50 new hires in Q1)
• Retention rate: 92% (industry average: 88%)
• Training investment: $500K in skills development programs

COMMITMENTS FOR Q2 2024:
1. Complete digital transformation project (budget: $8M)
2. Achieve customer satisfaction score of 85% (current: 82%)
3. Launch sustainability initiative with 20% carbon reduction goal
4. Implement new performance management system for all employees

MARKET OUTLOOK
Despite economic uncertainty, we remain optimistic about growth prospects.
Market research indicates strong demand for our products through 2024.
Competition has intensified, but our market position remains strong.

BOARD ACTIONS REQUIRED:
• Approve additional $10M investment in R&D for Q2-Q3
• Review and approve updated compensation packages for senior leadership
• Authorize merger and acquisition exploration in adjacent markets

CONCLUSION
Q1 2024 exceeded expectations across most key metrics. We are confident in our ability to deliver on annual targets while managing identified risks effectively.

The executive team remains committed to transparent communication and delivering value to all stakeholders.

Next Board Meeting: June 15, 2024
Next Quarterly Review: July 30, 2024
"""

def create_pdf_sample():
    """Create a sample PDF document (text-based)"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        import io
        
        # Create PDF in memory
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Add content
        content = create_sample_content()
        lines = content.split('\n')
        
        y_position = 750
        for line in lines[:40]:  # First 40 lines to fit on page
            if y_position < 50:  # Start new page
                p.showPage()
                y_position = 750
            p.drawString(50, y_position, line[:80])  # Limit line length
            y_position -= 15
        
        p.save()
        buffer.seek(0)
        
        # Save to file
        pdf_path = Path("data/uploads/sample_board_presentation_q1_2024.pdf")
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(pdf_path, 'wb') as f:
            f.write(buffer.getvalue())
        
        print(f"✅ Created sample PDF: {pdf_path}")
        return pdf_path
        
    except ImportError:
        print("⚠️ reportlab not installed, creating text file instead")
        return create_text_sample()

def create_text_sample():
    """Create a sample text file as fallback"""
    content = create_sample_content()
    
    text_path = Path("data/uploads/sample_board_presentation_q1_2024.txt")
    text_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(text_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Created sample text file: {text_path}")
    return text_path

def create_comparison_sample():
    """Create a second sample for comparison testing"""
    content = """
OLYMPIA GROUP
BOARD OF DIRECTORS QUARTERLY REVIEW
Q4 2023

EXECUTIVE SUMMARY
Q4 2023 concluded a challenging but successful year for Olympia Group.
We achieved most of our annual objectives despite market headwinds.

FINANCIAL PERFORMANCE
• Revenue: $118M (+8% YoY)
• EBITDA: $25M (+5% YoY)
• Net Income: $15M (+3% YoY)
• Cash Position: $42M (-$3M from Q3)

Revenue growth slowed compared to earlier quarters due to market conditions.

STRATEGIC INITIATIVES STATUS
1. CUSTOMER ACQUISITION - COMPLETED
   - Digital marketing strategy fully implemented
   - Customer base increased by 22% (target was 25%)
   - Platform upgrade completed under budget

2. OPERATIONAL EFFICIENCY - IN PROGRESS
   - Achieved 8% cost reduction (target: 10%)
   - Automation project 75% complete
   - Some delays due to technical challenges

3. MARKET EXPANSION - DELAYED
   - Entry into new markets postponed to Q1 2024
   - Regulatory approval process took longer than expected
   - Budget reallocated to strengthen existing markets

RISK MANAGEMENT UPDATE
RESOLVED ISSUES:
• Supply chain disruption largely resolved through new partnerships
• Compliance team successfully hired and trained
• Cybersecurity incidents reduced by 60% after protocol implementation

NEW CHALLENGES:
• Economic uncertainty affecting customer spending patterns
• Increased competition from new market entrants
• Rising material costs impacting margins

HUMAN RESOURCES
• Headcount: 1,200 employees (-25 due to optimization)
• Retention rate: 89% (slight decline from 92%)
• Training completion: 95% of employees completed development programs

ACHIEVEMENTS vs COMMITMENTS:
✅ Customer satisfaction improved to 84% (target: 85%)
✅ Sustainability initiative launched successfully
⚠️ Performance management system delayed to Q1 2024
❌ Carbon reduction goal achieved only 15% (target: 20%)

MARKET OUTLOOK
Market conditions remain challenging with increased volatility.
However, strong fundamentals support cautious optimism for 2024.
Focus shifting to defensive strategies and market share protection.

LESSONS LEARNED:
- More conservative timeline planning needed for complex initiatives
- Supply chain diversification proved critical for resilience
- Technology investments delivered measurable ROI

Q1 2024 PRIORITIES:
1. Complete remaining operational efficiency projects
2. Execute delayed market expansion plans
3. Strengthen balance sheet and cash position
4. Enhance risk management capabilities

CONCLUSION
While Q4 presented challenges, the organization demonstrated resilience and adaptability.
Strong foundation established for growth in 2024.
"""
    
    text_path = Path("data/uploads/sample_board_presentation_q4_2023.txt")
    text_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(text_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Created comparison sample: {text_path}")
    return text_path

def main():
    """Create sample documents for testing"""
    print("📄 Creating Sample Documents for BoD Analysis System")
    print("=" * 50)
    
    # Create upload directory
    Path("data/uploads").mkdir(parents=True, exist_ok=True)
    
    # Create samples in different formats
    print("\n📝 Creating text samples...")
    sample1_txt = create_text_sample()  # Current quarter
    sample2_txt = create_comparison_sample()  # Previous quarter
    
    print("\n📄 Creating PDF samples...")
    try:
        sample1_pdf = create_pdf_sample()  # Try to create PDF version
        print(f"✅ Created PDF version: {sample1_pdf}")
    except Exception as e:
        print(f"⚠️  PDF creation failed: {e}")
        print("   Text samples available for testing")
    
    print("\n" + "=" * 50)
    print("✅ Sample documents created successfully!")
    print("\nUsage:")
    print("1. Start the enhanced Streamlit app: streamlit run app_enhanced.py --server.port 8502")
    print("2. Upload the sample files through the web interface")
    print("3. Test document analysis and comparison features")
    print("\nSample files:")
    print(f"  📄 {sample1_txt}")
    print(f"  📄 {sample2_txt}")
    
    # Check if PDF was created
    pdf_path = Path("data/uploads/sample_board_presentation_q1_2024.pdf")
    if pdf_path.exists():
        print(f"  📄 {pdf_path}")
    
    print(f"\n🌐 Access your enhanced BoD analyzer at: http://localhost:8502")

if __name__ == "__main__":
    main()
