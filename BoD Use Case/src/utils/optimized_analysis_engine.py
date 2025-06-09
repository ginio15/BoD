"""
Optimized Enhanced Analysis Engine for Ollama Integration

This version uses shorter, focused prompts that work better with local LLMs:
1. Shorter text chunks (under 2000 chars)
2. Simpler prompt structures
3. Step-by-step analysis approach
4. Better error handling for timeouts
"""

import logging
import json
import re
import sys
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.analysis_engine import AnalysisEngine
from src.models.document import ProcessedDocument
from config.settings import Config

logger = logging.getLogger(__name__)

class OptimizedAnalysisEngine(AnalysisEngine):
    """Optimized analysis engine for local LLM integration"""
    
    def __init__(self, provider: str = "ollama", model: str = "llama3.2:3b"):
        super().__init__()
        self.default_provider = provider
        self.default_model = model
        self.max_text_length = 2000  # Reduced for better performance
        self.timeout_seconds = 60     # Shorter timeout
        
        # Test LLM connection
        try:
            logger.info("Testing LLM connection...")
            test_response = self.llm_manager.generate_response(
                "Hello", self.default_provider, model=self.default_model
            )
            if test_response.error:
                logger.error(f"LLM connection test failed: {test_response.error}")
            else:
                logger.info("LLM connection successful")
        except Exception as e:
            logger.error(f"LLM initialization error: {e}")
    
    def analyze_document_optimized(self, document: ProcessedDocument, provider: str = None) -> Dict[str, Any]:
        """Perform optimized analysis with shorter prompts"""
        if provider is None:
            provider = self.default_provider
            
        logger.info(f"Starting optimized analysis with {provider}")
        
        # Chunk text if too long
        text_chunks = self._chunk_text(document.full_text, self.max_text_length)
        
        results = {
            "commitments": [],  # For regular app.py
            "enhanced_commitments": [],  # For app_enhanced.py
            "risks": [],  # For regular app.py
            "risk_assessment": [],  # For app_enhanced.py
            "financial_insights": [],
            "sentiment": {},  # For regular app.py
            "sentiment_analysis": {},  # For app_enhanced.py
            "strategic_priorities": [],  # For app_enhanced.py
            "executive_summary": "",  # For app_enhanced.py
            "summary": ""
        }
        
        # Analyze each chunk
        for i, chunk in enumerate(text_chunks):
            logger.info(f"Analyzing chunk {i+1}/{len(text_chunks)}")
            
            try:
                # Extract commitments
                chunk_commitments = self._extract_commitments_simple(chunk, provider)
                results["commitments"].extend(chunk_commitments)
                results["enhanced_commitments"].extend(chunk_commitments)  # Same data for both apps
                
                # Extract risks
                chunk_risks = self._extract_risks_simple(chunk, provider)
                results["risks"].extend(chunk_risks)
                results["risk_assessment"].extend(chunk_risks)  # Same data for both apps
                
                # Extract financial info
                chunk_financial = self._extract_financial_simple(chunk, provider)
                results["financial_insights"].extend(chunk_financial)
                
            except Exception as e:
                logger.error(f"Error analyzing chunk {i+1}: {e}")
                continue
        
        # Overall sentiment analysis
        try:
            sentiment_data = self._analyze_sentiment_simple(document.full_text[:1500], provider)
            results["sentiment"] = sentiment_data
            results["sentiment_analysis"] = sentiment_data  # Same data for both apps
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            results["sentiment"] = {"overall": "unknown", "confidence": 0}
            results["sentiment_analysis"] = {"overall": "unknown", "confidence": 0}
        
        # Generate strategic priorities (simple extraction for app_enhanced.py)
        try:
            results["strategic_priorities"] = self._extract_strategic_priorities_simple(document.full_text[:1500], provider)
        except Exception as e:
            logger.error(f"Strategic priorities extraction failed: {e}")
            results["strategic_priorities"] = []
        
        # Generate summary
        try:
            summary_text = self._generate_summary_simple(document.full_text[:1000], results, provider)
            results["summary"] = summary_text
            results["executive_summary"] = summary_text  # Same summary for both apps
        except Exception as e:
            logger.error(f"Summary generation failed: {e}")
            results["summary"] = "Summary generation failed."
            results["executive_summary"] = "Summary generation failed."
        
        return results
    
    def analyze_document(self, document_input, provider: str = None) -> Dict[str, Any]:
        """Convenience method that accepts either a string or ProcessedDocument"""
        if isinstance(document_input, str):
            # Create a ProcessedDocument from string
            from src.models.document import DocumentMetadata, DocumentPage
            
            metadata = DocumentMetadata(
                filename="Text_Input.txt",
                file_type="txt",
                total_pages=1,
                word_count=len(document_input.split())
            )
            page = DocumentPage(page_number=1, text=document_input)
            document = ProcessedDocument(pages=[page], metadata=metadata, full_text=document_input)
            
        elif hasattr(document_input, 'full_text'):
            # It's already a ProcessedDocument
            document = document_input
        else:
            raise ValueError("document_input must be either a string or ProcessedDocument")
        
        return self.analyze_document_optimized(document, provider)

    def _chunk_text(self, text: str, max_length: int) -> List[str]:
        """Split text into smaller chunks"""
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        words = text.split()
        current_chunk = []
        current_length = 0
        
        for word in words:
            word_length = len(word) + 1  # +1 for space
            if current_length + word_length > max_length and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = word_length
            else:
                current_chunk.append(word)
                current_length += word_length
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    
    def _extract_commitments_simple(self, text: str, provider: str) -> List[Dict[str, Any]]:
        """Extract commitments with a simple, focused prompt"""
        prompt = f"""Find commitments in this board text. Look for specific promises, targets, or planned actions.

Text: {text}

List each commitment in this format:
1. [commitment text] - Deadline: [when it will be done] - Metric: [any numbers or measurable targets]
2. [commitment text] - Deadline: [when it will be done] - Metric: [any numbers or measurable targets]

Focus on specific commitments with clear actions or targets."""
        
        try:
            response = self.llm_manager.generate_response(
                prompt, provider, model=self.default_model
            )
            
            if response.error:
                logger.error(f"Commitment extraction failed: {response.error}")
                return self._extract_commitments_fallback(text)
            
            if not response.content or response.content.strip() == "":
                logger.warning("Empty response for commitment extraction, using fallback")
                return self._extract_commitments_fallback(text)
            
            # Parse simple response format
            commitments = []
            lines = response.content.split('\n')
            
            for line in lines:
                line = line.strip()
                if line and (line.startswith('1.') or line.startswith('2.') or 
                           line.startswith('3.') or line.startswith('4.') or
                           line.startswith('5.') or line.startswith('-')):
                    
                    # More flexible parsing
                    # Handle different formats the LLM might return
                    if ' - ' in line:
                        # Format: "1. text - deadline - category"
                        parts = line.split(' - ')
                        commitment_text = parts[0]
                        
                        # Remove number prefix (1., 2., etc.)
                        if '. ' in commitment_text:
                            commitment_text = commitment_text.split('. ', 1)[1]
                        
                        # Try to parse deadline, metric, and category from remaining parts
                        deadline = "Not specified"
                        metric = "Not specified"
                        category = "general"
                        
                        # Look for different patterns in the parts
                        for part in parts[1:]:
                            part_lower = part.lower().strip()
                            
                            # Check for deadline patterns
                            if ('deadline:' in part_lower or 
                                any(word in part_lower for word in ['q1', 'q2', 'q3', 'q4', 'quarter', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', '2024', '2025', 'by'])):
                                deadline = part.replace('Deadline:', '').replace('deadline:', '').strip()
                            
                            # Check for metric patterns
                            elif ('metric:' in part_lower or 
                                  any(char in part for char in ['$', '%', '#']) or
                                  any(word in part_lower for word in ['million', 'thousand', 'percent', 'increase', 'decrease', 'target', 'goal'])):
                                metric = part.replace('Metric:', '').replace('metric:', '').strip()
                            
                            # Check for category patterns
                            elif any(word in part_lower for word in ['financial', 'operational', 'strategic', 'cost', 'product', 'market']):
                                category = part.strip().lower()
                        
                        # Try to extract quantifiable metric from the commitment text itself if not found in parts
                        if metric == "Not specified":
                            # Look for numbers, percentages, dollars in the commitment text
                            import re
                            metric_patterns = [
                                r'\$[\d,]+[KMB]?',  # Dollar amounts
                                r'\d+%',            # Percentages
                                r'\d+\s*(million|thousand|billion)',  # Large numbers
                                r'(increase|decrease|improve|reduce).*?(\d+%?)',  # Improvement metrics
                            ]
                            
                            for pattern in metric_patterns:
                                match = re.search(pattern, commitment_text, re.IGNORECASE)
                                if match:
                                    metric = match.group(0)
                                    break
                        
                        commitments.append({
                            "text": commitment_text.strip(),
                            "exact_text": commitment_text.strip(),
                            "deadline": deadline,
                            "category": category,
                            "confidence": "medium",
                            "confidence_level": "medium",
                            "quantifiable_metric": "Not specified",
                            "stakeholder": "Not specified",
                            "risk_factors": [],
                            "source": "llm_simple"
                        })
                    else:
                        # If no dashes, just take the text after the number
                        if '. ' in line:
                            commitment_text = line.split('. ', 1)[1]
                            
                            # Try to extract deadline from the text itself
                            deadline = "Not specified"
                            if any(word in commitment_text.lower() for word in ['q1', 'q2', 'q3', 'q4', 'by']):
                                # Simple deadline extraction
                                import re
                                deadline_match = re.search(r'by\s+(Q[1-4]\s+202[4-9]|[A-Z][a-z]+\s+202[4-9])', commitment_text, re.IGNORECASE)
                                if deadline_match:
                                    deadline = deadline_match.group(1)
                            
                            commitments.append({
                                "text": commitment_text.strip(),
                                "exact_text": commitment_text.strip(),
                                "deadline": deadline,
                                "category": "general",
                                "confidence": "medium",
                                "confidence_level": "medium",
                                "quantifiable_metric": "Not specified",
                                "stakeholder": "Not specified", 
                                "risk_factors": [],
                                "source": "llm_simple"
                            })
            
            return commitments
            
        except Exception as e:
            logger.error(f"Error in simple commitment extraction: {e}")
            return self._extract_commitments_fallback(text)
    
    def _extract_commitments_fallback(self, text: str) -> List[Dict[str, Any]]:
        """Fallback commitment extraction using keyword search"""
        try:
            commitments = []
            
            # Keywords that often indicate commitments
            commitment_keywords = [
                'will', 'plan to', 'commit to', 'intend to', 'expect to',
                'target', 'goal', 'objective', 'by the end of', 'next quarter',
                'implement', 'launch', 'deliver', 'achieve', 'complete'
            ]
            
            sentences = text.split('.')
            for sentence in sentences:
                sentence = sentence.strip()
                if any(keyword in sentence.lower() for keyword in commitment_keywords):
                    if len(sentence) > 20 and len(sentence) < 200:  # Reasonable length
                        commitments.append({
                            'text': sentence,
                            'exact_text': sentence,
                            'confidence': 0.3,  # Lower confidence for fallback
                            'confidence_level': 'low',
                            'category': 'unknown',
                            'deadline': 'not specified',
                            'quantifiable_metric': 'Not specified',
                            'stakeholder': 'Not specified',
                            'risk_factors': [],
                            'source': 'fallback_extraction'
                        })
            
            return commitments[:5]  # Limit to top 5 to avoid noise
            
        except Exception as e:
            logger.error(f"Error in fallback commitment extraction: {e}")
            return []
    
    def _extract_risks_simple(self, text: str, provider: str) -> List[Dict[str, Any]]:
        """Extract risks with a simple prompt"""
        prompt = f"""Find risks mentioned in this board text. For each risk, identify the description, level, and impact.

Text: {text}

List each risk in this format:
1. [risk description] - Level: [high/medium/low] - Impact: [describe the potential impact]
2. [risk description] - Level: [high/medium/low] - Impact: [describe the potential impact]

Be specific and concise."""
        
        try:
            response = self.llm_manager.generate_response(
                prompt, provider, model=self.default_model
            )
            
            if response.error:
                logger.error(f"Risk extraction failed: {response.error}")
                return self._extract_risks_fallback(text)
            
            if not response.content or response.content.strip() == "":
                logger.warning("Empty response for risk extraction, using fallback")
                return self._extract_risks_fallback(text)
            
            risks = []
            lines = response.content.split('\n')
            
            for line in lines:
                line = line.strip()
                # Look for numbered lists or bullet points
                if (line.startswith('-') or line.startswith('1.') or line.startswith('2.') or 
                    line.startswith('3.') or line.startswith('4.') or line.startswith('5.')):
                    
                    # Remove prefix (-, 1., 2., etc.)
                    if line.startswith('-'):
                        risk_text = line[1:].strip()
                    elif '. ' in line:
                        risk_text = line.split('. ', 1)[1]
                    else:
                        risk_text = line
                    
                    # Extract level - look for various patterns
                    level = "medium"  # default
                    level_patterns = [
                        r'\(([Hh]igh|[Mm]edium|[Ll]ow)[^)]*\)',
                        r'([Hh]igh|[Mm]edium|[Ll]ow)\s+[Pp]riority',
                        r'Level:\s*([Hh]igh|[Mm]edium|[Ll]ow)',
                        r'\(Level:\s*([Hh]igh|[Mm]edium|[Ll]ow)\)'
                    ]
                    
                    for pattern in level_patterns:
                        level_match = re.search(pattern, risk_text, re.IGNORECASE)
                        if level_match:
                            level = level_match.group(1).lower()
                            break
                    
                    # Extract impact
                    impact = "Not specified"
                    impact_patterns = [
                        r'Impact:\s*([^)]+)\)',
                        r'\(Impact:\s*([^)]+)\)',
                        r'impact[:\s]+([^)]+)\)',
                        r'Impact:\s*([^,]+)'
                    ]
                    
                    for pattern in impact_patterns:
                        impact_match = re.search(pattern, risk_text, re.IGNORECASE)
                        if impact_match:
                            impact = impact_match.group(1).strip()
                            break
                    
                    # Clean risk description by removing the level and impact parts
                    risk_desc = risk_text
                    # Remove common patterns
                    risk_desc = re.sub(r'\s*\([^)]*[Pp]riority[^)]*\)', '', risk_desc)
                    risk_desc = re.sub(r'\s*\(Level:[^)]*\)', '', risk_desc)
                    risk_desc = re.sub(r'\s*\(Impact:[^)]*\)', '', risk_desc)
                    risk_desc = re.sub(r'\s*\([^)]*[Ii]mpact[^)]*\)', '', risk_desc)
                    
                    if risk_desc.strip():
                        risks.append({
                            "description": risk_desc.strip(),
                            "risk_description": risk_desc.strip(),
                            "level": level,
                            "risk_level": level,
                            "impact": impact,
                            "potential_impact": impact,
                            "category": "general",
                            "mitigation_mentioned": False,
                            "source": "llm_simple"
                        })
            
            return risks
            
        except Exception as e:
            logger.error(f"Error in simple risk extraction: {e}")
            return self._extract_risks_fallback(text)
    
    def _extract_risks_fallback(self, text: str) -> List[Dict[str, Any]]:
        """Fallback risk extraction using keyword search"""
        try:
            risks = []
            
            # Keywords that often indicate risks
            risk_keywords = [
                'risk', 'threat', 'challenge', 'concern', 'issue', 'problem',
                'uncertainty', 'volatility', 'exposure', 'vulnerability',
                'decline', 'decrease', 'shortfall', 'delay', 'obstacle'
            ]
            
            sentences = text.split('.')
            for sentence in sentences:
                sentence = sentence.strip()
                if any(keyword in sentence.lower() for keyword in risk_keywords):
                    if len(sentence) > 15 and len(sentence) < 200:  # Reasonable length
                        risks.append({
                            'description': sentence,
                            'risk_description': sentence,
                            'level': 'medium',  # Default level
                            'risk_level': 'medium',
                            'impact': 'not specified',
                            'potential_impact': 'not specified',
                            'category': 'general',
                            'mitigation_mentioned': False,
                            'confidence': 0.3,  # Lower confidence for fallback
                            'source': 'fallback_extraction'
                        })
            
            return risks[:5]  # Limit to top 5 to avoid noise
            
        except Exception as e:
            logger.error(f"Error in fallback risk extraction: {e}")
            return []
    
    def _extract_financial_simple(self, text: str, provider: str) -> List[Dict[str, Any]]:
        """Extract financial information with a simple prompt"""
        prompt = f"""Find financial numbers and metrics in this text.

Text: {text}

List financial information:
- [metric name]: [value] ([trend: up/down/stable])

Example: Revenue: $2.5M (up)"""
        
        try:
            response = self.llm_manager.generate_response(
                prompt, provider, model=self.default_model
            )
            
            if response.error:
                return []
            
            financial = []
            lines = response.content.split('\n')
            
            for line in lines:
                if ':' in line and line.strip().startswith('-'):
                    # Parse: - Metric: Value (trend)
                    content = line.strip()[1:].strip()
                    parts = content.split(':', 1)
                    
                    if len(parts) == 2:
                        metric = parts[0].strip()
                        value_part = parts[1].strip()
                        
                        # Extract trend
                        trend = "stable"
                        if '(' in value_part and ')' in value_part:
                            trend_match = re.search(r'\(([^)]+)\)', value_part)
                            if trend_match:
                                trend_text = trend_match.group(1).lower()
                                if 'up' in trend_text or 'increase' in trend_text:
                                    trend = "increasing"
                                elif 'down' in trend_text or 'decrease' in trend_text:
                                    trend = "decreasing"
                        
                        # Clean value
                        value = re.sub(r'\s*\([^)]+\)', '', value_part).strip()
                        
                        financial.append({
                            "metric": metric,
                            "value": value,
                            "trend": trend,
                            "source": "llm_simple"
                        })
            
            return financial
            
        except Exception as e:
            logger.error(f"Error in simple financial extraction: {e}")
            return []
    
    def _analyze_sentiment_simple(self, text: str, provider: str) -> Dict[str, Any]:
        """Simple sentiment analysis"""
        prompt = f"""What is the overall sentiment of this board presentation?

Text: {text}

Answer:
Sentiment: positive/negative/neutral/mixed
Confidence: 1-10
Reason: [brief explanation]"""
        
        try:
            response = self.llm_manager.generate_response(
                prompt, provider, model=self.default_model
            )
            
            if response.error:
                return {"overall": "unknown", "confidence": 0}
            
            # Parse response
            sentiment_data = {"overall": "neutral", "confidence": 5, "reason": ""}
            
            lines = response.content.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith("Sentiment:"):
                    sentiment = line.split(':', 1)[1].strip().lower()
                    sentiment_data["overall"] = sentiment
                elif line.startswith("Confidence:"):
                    conf_text = line.split(':', 1)[1].strip()
                    try:
                        confidence = int(conf_text.split()[0])
                        sentiment_data["confidence"] = confidence
                    except:
                        pass
                elif line.startswith("Reason:"):
                    reason = line.split(':', 1)[1].strip()
                    sentiment_data["reason"] = reason
            
            return sentiment_data
            
        except Exception as e:
            logger.error(f"Error in simple sentiment analysis: {e}")
            return {"overall": "unknown", "confidence": 0}
    
    def _generate_summary_simple(self, text: str, analysis_results: Dict[str, Any], provider: str) -> str:
        """Generate a simple summary"""
        commitment_count = len(analysis_results.get("commitments", []))
        risk_count = len(analysis_results.get("risks", []))
        
        prompt = f"""Summarize this board presentation in 2-3 sentences.

Text: {text}

Analysis found: {commitment_count} commitments, {risk_count} risks

Summary:"""
        
        try:
            response = self.llm_manager.generate_response(
                prompt, provider, model=self.default_model
            )
            
            if response.error:
                return f"Board presentation analyzed: {commitment_count} commitments and {risk_count} risks identified."
            
            return response.content.strip()
            
        except Exception as e:
            logger.error(f"Error in simple summary generation: {e}")
            return f"Analysis completed: {commitment_count} commitments, {risk_count} risks found."

    def _extract_strategic_priorities_simple(self, text: str, provider: str) -> List[Dict[str, Any]]:
        """Extract strategic priorities with a simple prompt"""
        prompt = f"""Find strategic priorities or key initiatives in this board text.

Text: {text}

List each priority:
- [priority name] (Category: [category]) (Timeline: [timeline])

Be concise."""
        
        try:
            response = self.llm_manager.generate_response(
                prompt, provider, model=self.default_model
            )
            
            if response.error or not response.content or response.content.strip() == "":
                return self._extract_strategic_priorities_fallback(text)
            
            priorities = []
            lines = response.content.split('\n')
            
            for line in lines:
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('1.') or line.startswith('2.') or 
                           line.startswith('3.') or line.startswith('4.') or line.startswith('5.')):
                    
                    # Remove prefix
                    if line.startswith('-'):
                        priority_text = line[1:].strip()
                    elif '. ' in line:
                        priority_text = line.split('. ', 1)[1]
                    else:
                        priority_text = line
                    
                    # Extract category and timeline
                    category = "general"
                    timeline = "not specified"
                    
                    if "(Category:" in priority_text:
                        cat_match = re.search(r'\(Category:\s*([^)]+)\)', priority_text)
                        if cat_match:
                            category = cat_match.group(1).strip()
                    
                    if "(Timeline:" in priority_text:
                        timeline_match = re.search(r'\(Timeline:\s*([^)]+)\)', priority_text)
                        if timeline_match:
                            timeline = timeline_match.group(1).strip()
                    
                    # Clean priority name
                    priority_name = re.sub(r'\s*\(Category:[^)]*\)', '', priority_text)
                    priority_name = re.sub(r'\s*\(Timeline:[^)]*\)', '', priority_name)
                    
                    if priority_name.strip():
                        priorities.append({
                            "priority_name": priority_name.strip(),
                            "category": category,
                            "timeline": timeline,
                            "importance_level": "medium",
                            "resources_mentioned": "not specified",
                            "success_metrics": "not specified",
                            "challenges": "",
                            "source": "llm_simple"
                        })
            
            return priorities[:5]  # Limit to top 5
            
        except Exception as e:
            logger.error(f"Error in strategic priorities extraction: {e}")
            return self._extract_strategic_priorities_fallback(text)
    
    def _extract_strategic_priorities_fallback(self, text: str) -> List[Dict[str, Any]]:
        """Fallback strategic priorities extraction using keyword search"""
        try:
            priorities = []
            
            # Keywords that often indicate strategic priorities
            priority_keywords = [
                'strategic', 'priority', 'initiative', 'goal', 'objective',
                'focus', 'key', 'important', 'critical', 'launch', 'expand',
                'improve', 'develop', 'implement', 'target'
            ]
            
            sentences = text.split('.')
            for sentence in sentences:
                sentence = sentence.strip()
                if any(keyword in sentence.lower() for keyword in priority_keywords):
                    if len(sentence) > 20 and len(sentence) < 150:  # Reasonable length
                        priorities.append({
                            'priority_name': sentence,
                            'category': 'general',
                            'timeline': 'not specified',
                            'importance_level': 'medium',
                            'resources_mentioned': 'not specified',
                            'success_metrics': 'not specified',
                            'challenges': '',
                            'source': 'fallback_extraction'
                        })
            
            return priorities[:3]  # Limit to top 3 to avoid noise
            
        except Exception as e:
            logger.error(f"Error in fallback strategic priorities extraction: {e}")
            return []
    
    def compare_documents(self, previous_doc: ProcessedDocument, current_doc: ProcessedDocument, 
                         provider: str = "ollama", options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Compare two documents using optimized analysis suitable for Ollama.
        This method provides the same interface as AnalysisEngine.compare_documents
        but uses simpler, faster prompts optimized for local models.
        """
        if options is None:
            options = {}
            
        logger.info(f"Starting optimized document comparison with {provider}")
        
        try:
            # Analyze both documents separately
            previous_results = self.analyze_document_optimized(previous_doc, provider)
            current_results = self.analyze_document_optimized(current_doc, provider)
            
            # Compare commitments
            comparison_results = {
                'commitments': self._compare_commitments(previous_results.get('commitments', []), 
                                                       current_results.get('commitments', [])),
                'sentiment_shifts': self._compare_sentiment(previous_results.get('sentiment', {}), 
                                                          current_results.get('sentiment', {})),
                'deescalations': self._find_deescalations(previous_results, current_results),
                'summary': self._generate_comparison_summary(previous_results, current_results, provider),
                'metadata': {
                    'analysis_type': 'optimized_comparison',
                    'provider': provider,
                    'timestamp': datetime.now().isoformat(),
                    'previous_doc_length': len(previous_doc.full_text),
                    'current_doc_length': len(current_doc.full_text)
                }
            }
            
            logger.info("Optimized document comparison completed successfully")
            return comparison_results
            
        except Exception as e:
            logger.error(f"Error in optimized document comparison: {e}")
            return {
                'commitments': [],
                'sentiment_shifts': [],
                'deescalations': [],
                'summary': f"Analysis failed: {str(e)}",
                'metadata': {'error': str(e), 'provider': provider}
            }
    
    def _compare_commitments(self, previous_commitments: List[Dict], current_commitments: List[Dict]) -> List[Dict]:
        """Compare commitments between two documents"""
        try:
            comparison = []
            
            # Track new commitments
            for current in current_commitments:
                is_new = True
                for previous in previous_commitments:
                    if self._commitments_similar(current.get('text', ''), previous.get('text', '')):
                        is_new = False
                        comparison.append({
                            'type': 'continued',
                            'text': current.get('text', ''),
                            'status': 'ongoing',
                            'confidence': min(current.get('confidence', 0.5), previous.get('confidence', 0.5))
                        })
                        break
                
                if is_new:
                    comparison.append({
                        'type': 'new',
                        'text': current.get('text', ''),
                        'status': 'new',
                        'confidence': current.get('confidence', 0.5)
                    })
            
            # Track dropped commitments
            for previous in previous_commitments:
                found_in_current = False
                for current in current_commitments:
                    if self._commitments_similar(previous.get('text', ''), current.get('text', '')):
                        found_in_current = True
                        break
                
                if not found_in_current:
                    comparison.append({
                        'type': 'dropped',
                        'text': previous.get('text', ''),
                        'status': 'not_mentioned',
                        'confidence': previous.get('confidence', 0.5)
                    })
            
            return comparison
            
        except Exception as e:
            logger.error(f"Error comparing commitments: {e}")
            return []
    
    def _commitments_similar(self, text1: str, text2: str) -> bool:
        """Simple similarity check for commitments"""
        if not text1 or not text2:
            return False
        
        # Simple word overlap check
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if len(words1) == 0 or len(words2) == 0:
            return False
        
        overlap = len(words1.intersection(words2))
        total = len(words1.union(words2))
        
        return (overlap / total) > 0.3  # 30% similarity threshold
    
    def _compare_sentiment(self, previous_sentiment: Dict, current_sentiment: Dict) -> List[Dict]:
        """Compare sentiment between documents"""
        try:
            shifts = []
            
            prev_overall = previous_sentiment.get('overall', 'neutral')
            curr_overall = current_sentiment.get('overall', 'neutral')
            
            if prev_overall != curr_overall:
                shifts.append({
                    'type': 'overall_sentiment_shift',
                    'from': prev_overall,
                    'to': curr_overall,
                    'confidence': min(
                        previous_sentiment.get('confidence', 0.5),
                        current_sentiment.get('confidence', 0.5)
                    )
                })
            
            return shifts
            
        except Exception as e:
            logger.error(f"Error comparing sentiment: {e}")
            return []
    
    def _find_deescalations(self, previous_results: Dict, current_results: Dict) -> List[Dict]:
        """Find topic de-escalations between documents"""
        try:
            deescalations = []
            
            # Simple heuristic: if previous had more risks and current has fewer
            prev_risks = len(previous_results.get('risks', []))
            curr_risks = len(current_results.get('risks', []))
            
            if prev_risks > curr_risks and prev_risks > 0:
                deescalations.append({
                    'type': 'risk_reduction',
                    'description': f'Risk count decreased from {prev_risks} to {curr_risks}',
                    'confidence': 0.6
                })
            
            return deescalations
            
        except Exception as e:
            logger.error(f"Error finding deescalations: {e}")
            return []
    
    def _generate_comparison_summary(self, previous_results: Dict, current_results: Dict, provider: str) -> str:
        """Generate a comparison summary"""
        try:
            prev_commitments = len(previous_results.get('commitments', []))
            curr_commitments = len(current_results.get('commitments', []))
            prev_risks = len(previous_results.get('risks', []))
            curr_risks = len(current_results.get('risks', []))
            
            summary = f"Document comparison completed. "
            summary += f"Commitments: {prev_commitments} → {curr_commitments}. "
            summary += f"Risks: {prev_risks} → {curr_risks}. "
            
            if curr_commitments > prev_commitments:
                summary += "New commitments identified. "
            elif curr_commitments < prev_commitments:
                summary += "Some commitments may have been resolved. "
            
            if curr_risks > prev_risks:
                summary += "New risks emerged. "
            elif curr_risks < prev_risks:
                summary += "Risk profile improved. "
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating comparison summary: {e}")
            return "Comparison analysis completed with basic metrics."
