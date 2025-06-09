"""
Enhanced Analysis Engine for BoD Presentation Analysis with Advanced LLM Integration

This enhanced version provides:
1. Improved prompt engineering for better LLM responses
2. Structured analysis workflows
3. Advanced commitment categorization
4. Risk assessment capabilities
5. Financial impact analysis
"""

import logging
import json
import re
import sys
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.analysis_engine import AnalysisEngine
from src.models.document import ProcessedDocument
from config.settings import Config

logger = logging.getLogger(__name__)

@dataclass
class EnhancedCommitment:
    """Enhanced commitment structure with detailed attributes"""
    text: str
    category: str  # financial, operational, strategic, hr, compliance
    deadline: Optional[str] = None
    quantifiable_metric: Optional[str] = None
    confidence_level: str = "medium"  # high, medium, low
    risk_factors: List[str] = None
    financial_impact: Optional[Dict[str, Any]] = None
    stakeholder: Optional[str] = None
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.risk_factors is None:
            self.risk_factors = []
        if self.dependencies is None:
            self.dependencies = []

@dataclass
class RiskAssessment:
    """Risk assessment structure"""
    risk_description: str
    risk_level: str  # high, medium, low
    category: str  # financial, operational, strategic, regulatory, market
    potential_impact: str
    mitigation_mentioned: bool = False
    affects_commitments: List[str] = None
    
    def __post_init__(self):
        if self.affects_commitments is None:
            self.affects_commitments = []

@dataclass
class FinancialInsight:
    """Financial insights structure"""
    metric_type: str  # revenue, cost, profit, etc.
    current_value: Optional[str] = None
    target_value: Optional[str] = None
    trend: str = "stable"  # increasing, decreasing, stable
    significance: str = "medium"  # high, medium, low

class EnhancedAnalysisEngine(AnalysisEngine):
    """Enhanced analysis engine with advanced LLM capabilities"""
    
    def __init__(self):
        super().__init__()
        self.default_provider = "ollama"  # Use Ollama as default for cost-free analysis
    
    def analyze_document_enhanced(self, document: ProcessedDocument, provider: str = None) -> Dict[str, Any]:
        """Perform comprehensive enhanced analysis"""
        if provider is None:
            provider = self.default_provider
            
        logger.info(f"Starting enhanced analysis with {provider}")
        
        analysis_results = {
            "enhanced_commitments": self._extract_enhanced_commitments(document.full_text, provider),
            "risk_assessment": self._analyze_risks(document.full_text, provider),
            "financial_insights": self._extract_financial_insights(document.full_text, provider),
            "sentiment_analysis": self._enhanced_sentiment_analysis(document.full_text, provider),
            "strategic_priorities": self._identify_strategic_priorities(document.full_text, provider),
            "stakeholder_analysis": self._analyze_stakeholder_mentions(document.full_text, provider)
        }
        
        # Generate executive summary
        analysis_results["executive_summary"] = self._generate_executive_summary(
            document.full_text, analysis_results, provider
        )
        
        return analysis_results
    
    def _extract_enhanced_commitments(self, text: str, provider: str) -> List[Dict[str, Any]]:
        """Extract commitments with enhanced categorization and analysis"""
        prompt = f"""
        You are an expert board analyst. Analyze this board presentation text and extract ALL commitments, promises, and future actions with detailed categorization.

        TEXT TO ANALYZE:
        {text[:4000]}

        EXTRACT each commitment with these details:
        1. exact_text: The precise commitment statement
        2. category: financial/operational/strategic/hr/compliance/regulatory
        3. deadline: Any specific timeframe mentioned (Q1 2024, December, etc.)
        4. quantifiable_metric: Specific numbers, percentages, or measurable goals
        5. confidence_level: high/medium/low (based on language certainty)
        6. stakeholder: Who is responsible (board, management, specific department)
        7. risk_factors: Any risks that could impact this commitment
        8. dependencies: Prerequisites or dependencies mentioned

        IMPORTANT: 
        - Look for subtle commitments, not just obvious "we will" statements
        - Include targets, goals, and expectations
        - Note conditional commitments ("if market conditions...")
        - Identify both explicit and implicit commitments

        FORMAT as JSON array of commitment objects.
        """
        
        try:
            response = self.llm_manager.generate_response(prompt, provider)
            if response.error:
                logger.error(f"Enhanced commitment extraction failed: {response.error}")
                return []
            
            # Try to parse JSON response
            try:
                commitments = json.loads(response.content)
                if isinstance(commitments, list):
                    logger.info(f"Extracted {len(commitments)} enhanced commitments")
                    return commitments
                else:
                    logger.warning("LLM response was not a list")
                    return []
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse commitment JSON: {e}")
                # Try to extract JSON from response text
                return self._extract_json_from_text(response.content, "commitments")
                
        except Exception as e:
            logger.error(f"Error in enhanced commitment extraction: {e}")
            return []
    
    def _analyze_risks(self, text: str, provider: str) -> List[Dict[str, Any]]:
        """Comprehensive risk analysis"""
        prompt = f"""
        Conduct a comprehensive risk analysis of this board presentation.

        TEXT TO ANALYZE:
        {text[:4000]}

        IDENTIFY all risks mentioned or implied, including:
        1. risk_description: Clear description of the risk
        2. risk_level: high/medium/low based on language and context
        3. category: financial/operational/strategic/regulatory/market/technical
        4. potential_impact: Specific impact if risk materializes
        5. mitigation_mentioned: true/false if mitigation strategies are discussed
        6. affects_commitments: List of commitments this risk could impact
        7. time_horizon: immediate/short-term/medium-term/long-term

        LOOK FOR:
        - Explicit risk statements
        - Implied concerns or challenges
        - Market conditions and external factors
        - Operational vulnerabilities
        - Financial exposures
        - Regulatory or compliance risks

        FORMAT as JSON array of risk objects.
        """
        
        try:
            response = self.llm_manager.generate_response(prompt, provider)
            if response.error:
                logger.error(f"Risk analysis failed: {response.error}")
                return []
            
            try:
                risks = json.loads(response.content)
                if isinstance(risks, list):
                    logger.info(f"Identified {len(risks)} risks")
                    return risks
                else:
                    return []
            except json.JSONDecodeError:
                return self._extract_json_from_text(response.content, "risks")
                
        except Exception as e:
            logger.error(f"Error in risk analysis: {e}")
            return []
    
    def _extract_financial_insights(self, text: str, provider: str) -> List[Dict[str, Any]]:
        """Extract financial metrics, targets, and insights"""
        prompt = f"""
        Extract all financial information, metrics, and insights from this board presentation.

        TEXT TO ANALYZE:
        {text[:4000]}

        IDENTIFY:
        1. metric_type: revenue/costs/profit/margin/cash_flow/growth/etc.
        2. current_value: Current reported value with units
        3. target_value: Target or projected value if mentioned
        4. time_period: Q1/Q2/2024/monthly/etc.
        5. trend: increasing/decreasing/stable/volatile
        6. significance: high/medium/low importance to business
        7. comparison: vs previous period, vs target, vs competition
        8. context: Additional context about the metric

        LOOK FOR:
        - Revenue and growth figures
        - Cost reduction targets
        - Profit margins and targets
        - Cash flow statements
        - Budget allocations
        - Investment amounts
        - Financial projections
        - ROI metrics

        FORMAT as JSON array of financial insight objects.
        """
        
        try:
            response = self.llm_manager.generate_response(prompt, provider)
            if response.error:
                logger.error(f"Financial analysis failed: {response.error}")
                return []
            
            try:
                insights = json.loads(response.content)
                if isinstance(insights, list):
                    logger.info(f"Extracted {len(insights)} financial insights")
                    return insights
                else:
                    return []
            except json.JSONDecodeError:
                return self._extract_json_from_text(response.content, "financial_insights")
                
        except Exception as e:
            logger.error(f"Error in financial analysis: {e}")
            return []
    
    def _enhanced_sentiment_analysis(self, text: str, provider: str) -> Dict[str, Any]:
        """Advanced sentiment analysis with topic-specific insights"""
        prompt = f"""
        Perform comprehensive sentiment analysis on this board presentation.

        TEXT TO ANALYZE:
        {text[:4000]}

        PROVIDE:
        1. overall_sentiment: positive/negative/neutral/mixed
        2. overall_confidence: 1-10 scale
        3. topic_sentiments: Sentiment for each major topic discussed
        4. sentiment_evolution: How sentiment changes throughout the document
        5. confidence_indicators: Words/phrases indicating confidence levels
        6. concern_indicators: Words/phrases indicating concerns
        7. leadership_tone: confident/cautious/optimistic/pessimistic/realistic
        8. board_alignment: high/medium/low based on language consistency

        ANALYZE sentiment for specific areas:
        - Financial performance
        - Market conditions  
        - Operational efficiency
        - Strategic initiatives
        - Risk management
        - Future outlook

        FORMAT as structured JSON object with detailed analysis.
        """
        
        try:
            response = self.llm_manager.generate_response(prompt, provider)
            if response.error:
                logger.error(f"Enhanced sentiment analysis failed: {response.error}")
                return {}
            
            try:
                sentiment = json.loads(response.content)
                if isinstance(sentiment, dict):
                    logger.info("Completed enhanced sentiment analysis")
                    return sentiment
                else:
                    return {}
            except json.JSONDecodeError:
                return {}
                
        except Exception as e:
            logger.error(f"Error in enhanced sentiment analysis: {e}")
            return {}
    
    def _identify_strategic_priorities(self, text: str, provider: str) -> List[Dict[str, Any]]:
        """Identify strategic priorities and initiatives"""
        prompt = f"""
        Identify strategic priorities, initiatives, and focus areas from this board presentation.

        TEXT TO ANALYZE:
        {text[:4000]}

        EXTRACT:
        1. priority_name: Clear name of the strategic priority
        2. category: growth/cost_reduction/market_expansion/innovation/operational_excellence/etc.
        3. importance_level: high/medium/low based on emphasis and context
        4. timeline: When this priority should be addressed
        5. resources_mentioned: Budget, personnel, or other resources allocated
        6. success_metrics: How success will be measured
        7. challenges: Obstacles or challenges mentioned
        8. stakeholders: Who is responsible or involved

        LOOK FOR:
        - Strategic initiatives and programs
        - Business transformation efforts
        - Market expansion plans
        - Innovation projects
        - Operational improvements
        - Competitive responses

        FORMAT as JSON array of strategic priority objects.
        """
        
        try:
            response = self.llm_manager.generate_response(prompt, provider)
            if response.error:
                logger.error(f"Strategic priority analysis failed: {response.error}")
                return []
            
            try:
                priorities = json.loads(response.content)
                if isinstance(priorities, list):
                    logger.info(f"Identified {len(priorities)} strategic priorities")
                    return priorities
                else:
                    return []
            except json.JSONDecodeError:
                return self._extract_json_from_text(response.content, "priorities")
                
        except Exception as e:
            logger.error(f"Error in strategic priority analysis: {e}")
            return []
    
    def _analyze_stakeholder_mentions(self, text: str, provider: str) -> Dict[str, Any]:
        """Analyze stakeholder mentions and relationships"""
        prompt = f"""
        Analyze stakeholder mentions and relationships in this board presentation.

        TEXT TO ANALYZE:
        {text[:4000]}

        IDENTIFY:
        1. stakeholder_groups: customers/employees/shareholders/partners/regulators/etc.
        2. sentiment_toward_stakeholder: positive/negative/neutral for each group
        3. commitments_to_stakeholders: Specific promises or commitments made
        4. stakeholder_concerns: Issues or concerns raised about stakeholders
        5. engagement_plans: Plans for stakeholder interaction or communication

        ANALYZE mentions of:
        - Customers and customer satisfaction
        - Employees and workforce
        - Shareholders and investors
        - Business partners
        - Regulatory bodies
        - Communities
        - Suppliers

        FORMAT as structured JSON with stakeholder analysis.
        """
        
        try:
            response = self.llm_manager.generate_response(prompt, provider)
            if response.error:
                logger.error(f"Stakeholder analysis failed: {response.error}")
                return {}
            
            try:
                stakeholders = json.loads(response.content)
                if isinstance(stakeholders, dict):
                    logger.info("Completed stakeholder analysis")
                    return stakeholders
                else:
                    return {}
            except json.JSONDecodeError:
                return {}
                
        except Exception as e:
            logger.error(f"Error in stakeholder analysis: {e}")
            return {}
    
    def _generate_executive_summary(self, text: str, analysis_results: Dict[str, Any], provider: str) -> str:
        """Generate executive summary of the analysis"""
        prompt = f"""
        Based on this board presentation and the analysis results, generate a concise executive summary.

        ORIGINAL TEXT (first 2000 chars):
        {text[:2000]}

        ANALYSIS RESULTS:
        - Commitments found: {len(analysis_results.get('enhanced_commitments', []))}
        - Risks identified: {len(analysis_results.get('risk_assessment', []))}
        - Financial insights: {len(analysis_results.get('financial_insights', []))}
        - Strategic priorities: {len(analysis_results.get('strategic_priorities', []))}

        GENERATE a 3-4 paragraph executive summary covering:
        1. Key themes and overall tone of the presentation
        2. Major commitments and strategic priorities
        3. Primary risks and financial insights
        4. Overall assessment and recommendations for board attention

        Write in professional, board-level language. Be concise but comprehensive.
        """
        
        try:
            response = self.llm_manager.generate_response(prompt, provider)
            if response.error:
                logger.error(f"Executive summary generation failed: {response.error}")
                return "Executive summary generation failed."
            
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating executive summary: {e}")
            return "Error generating executive summary."
    
    def _extract_json_from_text(self, text: str, key: str) -> List[Dict[str, Any]]:
        """Attempt to extract JSON from mixed text response"""
        try:
            # Look for JSON-like structures in the text
            import re
            json_pattern = r'\[.*\]|\{.*\}'
            matches = re.findall(json_pattern, text, re.DOTALL)
            
            for match in matches:
                try:
                    parsed = json.loads(match)
                    if isinstance(parsed, list):
                        return parsed
                    elif isinstance(parsed, dict) and key in parsed:
                        return parsed[key]
                except json.JSONDecodeError:
                    continue
            
            return []
        except Exception:
            return []
