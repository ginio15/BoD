"""
Analysis Engine for BoD Presentation Analysis System

Core analysis functionality for commitment tracking, sentiment analysis,
and topic de-escalation detection across Board of Directors presentations.
"""

import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.models.document import ProcessedDocument, ComparisonResult
from src.utils.llm_providers import LLMProviderManager, LLMResponse
from config.settings import Config

logger = logging.getLogger(__name__)

class AnalysisEngine:
    """Main analysis engine for BoD presentation analysis"""
    
    def __init__(self):
        self.config = Config()
        self.llm_manager = LLMProviderManager()
        self.commitment_patterns = self._load_commitment_patterns()
        self.sentiment_keywords = self._load_sentiment_keywords()
    
    def _load_commitment_patterns(self) -> List[Dict[str, Any]]:
        """Load patterns for detecting commitments in text"""
        return [
            {
                "pattern": r"(?i)(?:we will|we shall|we commit to|we plan to|we intend to|we aim to)",
                "type": "future_commitment",
                "confidence": 0.8
            },
            {
                "pattern": r"(?i)(?:by|before|within|no later than)\s+(?:q[1-4]|quarter|month|year|\d+)",
                "type": "time_bound_commitment",
                "confidence": 0.9
            },
            {
                "pattern": r"(?i)(?:target|goal|objective|milestone|deadline)",
                "type": "goal_commitment",
                "confidence": 0.7
            },
            {
                "pattern": r"(?i)(?:deliver|implement|complete|achieve|establish|launch)",
                "type": "action_commitment",
                "confidence": 0.8
            }
        ]
    
    def _load_sentiment_keywords(self) -> Dict[str, List[str]]:
        """Load sentiment keywords for analysis"""
        return {
            "positive": [
                "excellent", "outstanding", "successful", "improved", "growth", "strong",
                "progress", "achievement", "exceed", "positive", "opportunity", "optimistic",
                "confident", "effective", "efficient", "innovative", "robust", "solid"
            ],
            "negative": [
                "challenge", "concern", "issue", "problem", "decline", "decrease", "weakness",
                "risk", "difficulty", "obstacle", "setback", "shortfall", "disappointing",
                "underperform", "delay", "failed", "critical", "urgent", "crisis"
            ],
            "escalation": [
                "escalate", "urgent", "critical", "immediate", "crisis", "emergency",
                "escalation", "priority", "attention", "action required", "must address"
            ],
            "de_escalation": [
                "resolved", "improvement", "better", "stabilized", "under control",
                "managed", "addressed", "mitigated", "reduced", "decreased concern"
            ]
        }
    
    def analyze_document(self, document: ProcessedDocument, provider: str = "openai") -> ProcessedDocument:
        """Perform comprehensive analysis on a single document"""
        logger.info(f"Starting analysis of document: {document.metadata.file_name}")
        
        # Extract commitments
        document.commitments = self._extract_commitments(document, provider)
        
        # Analyze sentiment
        document.sentiment_scores = self._analyze_sentiment(document, provider)
        
        # Extract key topics
        document.key_topics = self._extract_key_topics(document, provider)
        
        # Detect escalation topics
        document.escalation_topics = self._detect_escalation_topics(document, provider)
        
        logger.info(f"Analysis complete for {document.metadata.file_name}")
        return document
    
    def _extract_commitments(self, document: ProcessedDocument, provider: str) -> List[Dict[str, Any]]:
        """Extract commitments from document using pattern matching and LLM verification"""
        commitments = []
        
        # Pattern-based extraction
        pattern_commitments = self._extract_commitments_by_pattern(document.full_text)
        
        # LLM-based extraction and verification
        llm_commitments = self._extract_commitments_by_llm(document.full_text, provider)
        
        # Combine and deduplicate
        all_commitments = pattern_commitments + llm_commitments
        commitments = self._deduplicate_commitments(all_commitments)
        
        logger.info(f"Extracted {len(commitments)} commitments from {document.metadata.file_name}")
        return commitments
    
    def _extract_commitments_by_pattern(self, text: str) -> List[Dict[str, Any]]:
        """Extract commitments using regex patterns"""
        commitments = []
        
        for pattern_info in self.commitment_patterns:
            matches = re.finditer(pattern_info["pattern"], text, re.IGNORECASE | re.MULTILINE)
            
            for match in matches:
                # Extract surrounding context
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 100)
                context = text[start:end].strip()
                
                commitment = {
                    "text": match.group(),
                    "context": context,
                    "type": pattern_info["type"],
                    "confidence": pattern_info["confidence"],
                    "extraction_method": "pattern",
                    "position": match.start()
                }
                commitments.append(commitment)
        
        return commitments
    
    def _extract_commitments_by_llm(self, text: str, provider: str) -> List[Dict[str, Any]]:
        """Extract commitments using LLM analysis"""
        prompt = f"""
        Analyze the following Board of Directors presentation text and extract all commitments, promises, or future actions mentioned.
        
        For each commitment, provide:
        1. The exact text of the commitment
        2. The type of commitment (goal, deadline, action, etc.)
        3. Any timeline mentioned
        4. Confidence level (0-1)
        5. The broader context
        
        Text to analyze:
        {text[:4000]}  # Limit text length for token efficiency
        
        Return the results in JSON format as a list of commitment objects.
        """
        
        try:
            response = self.llm_manager.generate_response(prompt, provider)
            
            if response.error:
                logger.error(f"LLM commitment extraction failed: {response.error}")
                return []
            
            # Try to parse JSON response
            try:
                commitments_data = json.loads(response.content)
                if isinstance(commitments_data, list):
                    for commitment in commitments_data:
                        commitment["extraction_method"] = "llm"
                        commitment["llm_provider"] = provider
                    return commitments_data
            except json.JSONDecodeError:
                logger.warning("Failed to parse LLM response as JSON")
                return []
                
        except Exception as e:
            logger.error(f"Error in LLM commitment extraction: {e}")
            return []
        
        return []
    
    def _deduplicate_commitments(self, commitments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate commitments based on text similarity"""
        if not commitments:
            return []
        
        unique_commitments = []
        
        for commitment in commitments:
            is_duplicate = False
            commitment_text = commitment.get("text", "").lower()
            
            for existing in unique_commitments:
                existing_text = existing.get("text", "").lower()
                
                # Simple similarity check
                if (commitment_text in existing_text or 
                    existing_text in commitment_text or
                    self._text_similarity(commitment_text, existing_text) > 0.8):
                    is_duplicate = True
                    # Keep the one with higher confidence
                    if commitment.get("confidence", 0) > existing.get("confidence", 0):
                        unique_commitments.remove(existing)
                        unique_commitments.append(commitment)
                    break
            
            if not is_duplicate:
                unique_commitments.append(commitment)
        
        return unique_commitments
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        """Simple text similarity calculation"""
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _analyze_sentiment(self, document: ProcessedDocument, provider: str) -> Dict[str, float]:
        """Analyze sentiment across different topics and themes"""
        sentiment_scores = {}
        
        # Overall document sentiment
        overall_sentiment = self._calculate_sentiment_score(document.full_text)
        sentiment_scores["overall"] = overall_sentiment
        
        # Page-by-page sentiment analysis
        page_sentiments = []
        for i, page in enumerate(document.pages):
            if page.content:
                page_sentiment = self._calculate_sentiment_score(page.content)
                page_sentiments.append(page_sentiment)
                sentiment_scores[f"page_{i+1}"] = page_sentiment
        
        # Average page sentiment
        if page_sentiments:
            sentiment_scores["average_page"] = sum(page_sentiments) / len(page_sentiments)
        
        # Topic-specific sentiment using LLM
        topic_sentiment = self._analyze_topic_sentiment(document.full_text, provider)
        sentiment_scores.update(topic_sentiment)
        
        return sentiment_scores
    
    def _calculate_sentiment_score(self, text: str) -> float:
        """Calculate sentiment score using keyword-based approach"""
        words = text.lower().split()
        
        positive_count = sum(1 for word in words if word in self.sentiment_keywords["positive"])
        negative_count = sum(1 for word in words if word in self.sentiment_keywords["negative"])
        
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            return 0.0  # Neutral
        
        # Return score between -1 and 1
        return (positive_count - negative_count) / total_sentiment_words
    
    def _analyze_topic_sentiment(self, text: str, provider: str) -> Dict[str, float]:
        """Analyze sentiment for specific topics using LLM"""
        prompt = f"""
        Analyze the sentiment for key business topics in this Board of Directors presentation.
        
        For each major topic mentioned (e.g., financial performance, market conditions, operations, strategy, etc.),
        provide a sentiment score from -1 (very negative) to +1 (very positive).
        
        Text to analyze:
        {text[:3000]}
        
        Return results in JSON format with topic names as keys and sentiment scores as values.
        """
        
        try:
            response = self.llm_manager.generate_response(prompt, provider)
            
            if response.error:
                logger.error(f"Topic sentiment analysis failed: {response.error}")
                return {}
            
            try:
                topic_sentiments = json.loads(response.content)
                if isinstance(topic_sentiments, dict):
                    return {f"topic_{k}": v for k, v in topic_sentiments.items() if isinstance(v, (int, float))}
            except json.JSONDecodeError:
                logger.warning("Failed to parse topic sentiment response as JSON")
                
        except Exception as e:
            logger.error(f"Error in topic sentiment analysis: {e}")
        
        return {}
    
    def _extract_key_topics(self, document: ProcessedDocument, provider: str) -> List[str]:
        """Extract key topics and themes from document"""
        prompt = f"""
        Extract the key topics and themes discussed in this Board of Directors presentation.
        
        Focus on:
        - Main business areas discussed
        - Strategic initiatives
        - Performance metrics
        - Challenges and opportunities
        - Future plans and commitments
        
        Text to analyze:
        {document.full_text[:3000]}
        
        Return a JSON list of key topics (5-10 topics maximum).
        """
        
        try:
            response = self.llm_manager.generate_response(prompt, provider)
            
            if response.error:
                logger.error(f"Topic extraction failed: {response.error}")
                return []
            
            try:
                topics = json.loads(response.content)
                if isinstance(topics, list):
                    return [str(topic) for topic in topics[:10]]  # Limit to 10 topics
            except json.JSONDecodeError:
                logger.warning("Failed to parse topic extraction response as JSON")
                
        except Exception as e:
            logger.error(f"Error in topic extraction: {e}")
        
        return []
    
    def _detect_escalation_topics(self, document: ProcessedDocument, provider: str) -> List[str]:
        """Detect topics that show escalation or increased urgency"""
        escalation_topics = []
        
        # Keyword-based detection
        for keyword in self.sentiment_keywords["escalation"]:
            if keyword.lower() in document.full_text.lower():
                # Extract context around escalation keywords
                escalation_topics.append(f"escalation_detected: {keyword}")
        
        # LLM-based escalation detection
        llm_escalations = self._detect_escalation_by_llm(document.full_text, provider)
        escalation_topics.extend(llm_escalations)
        
        return list(set(escalation_topics))  # Remove duplicates
    
    def _detect_escalation_by_llm(self, text: str, provider: str) -> List[str]:
        """Detect escalation topics using LLM analysis"""
        prompt = f"""
        Analyze this Board of Directors presentation for topics that show escalation, increased urgency, 
        or critical issues that require immediate attention.
        
        Look for:
        - Issues marked as urgent or critical
        - Problems that have worsened since last report
        - New risks or challenges
        - Items requiring board intervention
        
        Text to analyze:
        {text[:3000]}
        
        Return a JSON list of escalated topics with brief descriptions.
        """
        
        try:
            response = self.llm_manager.generate_response(prompt, provider)
            
            if response.error:
                logger.error(f"Escalation detection failed: {response.error}")
                return []
            
            try:
                escalations = json.loads(response.content)
                if isinstance(escalations, list):
                    return [str(escalation) for escalation in escalations[:5]]
            except json.JSONDecodeError:
                logger.warning("Failed to parse escalation detection response as JSON")
                
        except Exception as e:
            logger.error(f"Error in escalation detection: {e}")
        
        return []
    
    def compare_documents(self, documents: List[ProcessedDocument], provider: str = "openai") -> ComparisonResult:
        """Compare multiple documents to track changes over time"""
        logger.info(f"Comparing {len(documents)} documents")
        
        if len(documents) < 2:
            logger.warning("Need at least 2 documents for comparison")
            return ComparisonResult(documents=documents, comparison_type="insufficient_data")
        
        # Sort documents by date if possible
        sorted_docs = sorted(documents, key=lambda d: d.metadata.processing_date)
        
        comparison = ComparisonResult(
            documents=sorted_docs,
            comparison_type="temporal"
        )
        
        # Track commitment fulfillment
        comparison.commitment_fulfillment = self._track_commitment_fulfillment(sorted_docs, provider)
        
        # Analyze sentiment trends
        comparison.sentiment_trends = self._analyze_sentiment_trends(sorted_docs)
        
        # Track topic evolution
        comparison.topic_evolution = self._analyze_topic_evolution(sorted_docs, provider)
        
        # Calculate overall score
        comparison.overall_score = self._calculate_comparison_score(comparison)
        
        logger.info(f"Document comparison complete")
        return comparison
    
    def _track_commitment_fulfillment(self, documents: List[ProcessedDocument], provider: str) -> Dict[str, Any]:
        """Track fulfillment of commitments across documents"""
        # This is a simplified implementation
        # In practice, would need more sophisticated matching
        
        fulfillment_tracking = {}
        
        if len(documents) >= 2:
            older_doc = documents[0]
            newer_doc = documents[-1]
            
            # Compare commitments between documents
            older_commitments = older_doc.commitments
            newer_commitments = newer_doc.commitments
            
            fulfillment_tracking = {
                "previous_commitments": len(older_commitments),
                "current_commitments": len(newer_commitments),
                "status": "analysis_pending"  # Would implement detailed matching
            }
        
        return fulfillment_tracking
    
    def _analyze_sentiment_trends(self, documents: List[ProcessedDocument]) -> Dict[str, List[float]]:
        """Analyze sentiment trends across documents"""
        trends = {}
        
        for doc in documents:
            doc_date = doc.metadata.processing_date.isoformat() if doc.metadata.processing_date else "unknown"
            
            for sentiment_type, score in doc.sentiment_scores.items():
                if sentiment_type not in trends:
                    trends[sentiment_type] = []
                trends[sentiment_type].append(score)
        
        return trends
    
    def _analyze_topic_evolution(self, documents: List[ProcessedDocument], provider: str) -> Dict[str, Any]:
        """Analyze how topics evolve across documents"""
        all_topics = []
        
        for doc in documents:
            all_topics.extend(doc.key_topics)
        
        # Count topic frequency
        topic_counts = {}
        for topic in all_topics:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        return {
            "recurring_topics": [topic for topic, count in topic_counts.items() if count > 1],
            "new_topics": [topic for topic, count in topic_counts.items() if count == 1],
            "topic_frequency": topic_counts
        }
    
    def _calculate_comparison_score(self, comparison: ComparisonResult) -> float:
        """Calculate overall comparison score"""
        # Simplified scoring based on available data
        score = 0.5  # Base score
        
        # Adjust based on sentiment trends
        if comparison.sentiment_trends:
            avg_sentiment = sum(
                sum(scores) / len(scores) for scores in comparison.sentiment_trends.values()
            ) / len(comparison.sentiment_trends)
            score += avg_sentiment * 0.3
        
        # Adjust based on escalation topics
        if comparison.escalated_topics:
            score -= len(comparison.escalated_topics) * 0.1
        
        # Adjust based on de-escalated topics
        if comparison.de_escalated_topics:
            score += len(comparison.de_escalated_topics) * 0.1
        
        return max(0.0, min(1.0, score))  # Clamp between 0 and 1
