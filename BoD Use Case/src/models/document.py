"""
Document models for BoD Presentation Analysis System

Defines data structures for processed documents, pages, and metadata.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import uuid

@dataclass
class DocumentMetadata:
    """Metadata for a processed document"""
    filename: str
    file_type: str  # 'pdf' or 'pptx'
    total_pages: int = 0
    word_count: int = 0
    char_count: int = 0
    file_size_mb: float = 0.0
    
    # Optional fields
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    author: Optional[str] = None
    title: Optional[str] = None
    subject: Optional[str] = None
    quarter: Optional[str] = None  # Auto-detected or user-specified
    year: Optional[int] = None
    
    processing_date: datetime = field(default_factory=datetime.now)
    document_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    # Compatibility properties
    @property
    def file_name(self) -> str:
        return self.filename
    
    @property
    def page_count(self) -> int:
        return self.total_pages

@dataclass
class DocumentPage:
    """Represents a single page/slide from a document"""
    page_number: int
    text: str  # Extracted text content (renamed from content)
    source: str = "text"  # Source of extraction: 'text', 'ocr', or 'mixed'
    metadata: Dict[str, Any] = field(default_factory=dict)  # Page-specific metadata
    
    # Content analysis fields
    word_count: int = 0
    char_count: int = 0
    
    def __post_init__(self):
        """Calculate derived fields after initialization"""
        if self.text:
            self.word_count = len(self.text.split())
            self.char_count = len(self.text)
    
    @property
    def content(self) -> str:
        """Alias for text to maintain compatibility"""
        return self.text

@dataclass
class ProcessedDocument:
    """Complete processed document with all extracted content and analysis"""
    pages: List[DocumentPage]
    metadata: DocumentMetadata
    full_text: str = ""
    
    # Analysis results (filled by analysis engine)
    commitments: List[Dict[str, Any]] = field(default_factory=list)
    sentiment_scores: Dict[str, float] = field(default_factory=dict)
    key_topics: List[str] = field(default_factory=list)
    escalation_topics: List[str] = field(default_factory=list)
    
    # Processing metadata
    processing_time_seconds: float = 0.0
    ocr_pages: int = 0
    total_tokens_processed: int = 0
    
    def __post_init__(self):
        """Calculate derived fields after initialization"""
        # Combine all page content if full_text is empty
        if not self.full_text:
            self.full_text = "\n\n".join([page.text for page in self.pages if page.text])
        
        # Update metadata page count
        self.metadata.total_pages = len(self.pages)
        
        # Count OCR pages
        self.ocr_pages = sum(1 for page in self.pages if page.source in ["ocr", "mixed"])
    
    def get_page_content(self, page_number: int) -> Optional[str]:
        """Get content for a specific page number (1-indexed)"""
        if 1 <= page_number <= len(self.pages):
            return self.pages[page_number - 1].text
        return None
    
    def get_total_word_count(self) -> int:
        """Get total word count across all pages"""
        return sum(page.word_count for page in self.pages)
    
    def get_pages_with_content(self) -> List[DocumentPage]:
        """Get only pages that have extracted content"""
        return [page for page in self.pages if page.text.strip()]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'metadata': {
                'file_name': self.metadata.filename,
                'file_type': self.metadata.file_type,
                'quarter': self.metadata.quarter,
                'year': self.metadata.year,
                'page_count': self.metadata.total_pages,
                'document_id': self.metadata.document_id,
                'processing_date': self.metadata.processing_date.isoformat() if self.metadata.processing_date else None
            },
            'content_summary': {
                'total_pages': len(self.pages),
                'total_words': self.get_total_word_count(),
                'ocr_pages': self.ocr_pages,
                'processing_time': self.processing_time_seconds
            },
            'analysis': {
                'commitments_count': len(self.commitments),
                'key_topics': self.key_topics,
                'escalation_topics': self.escalation_topics,
                'sentiment_scores': self.sentiment_scores
            }
        }

@dataclass
class ComparisonResult:
    """Results from comparing multiple documents"""
    documents: List[ProcessedDocument]
    comparison_type: str  # 'quarterly', 'temporal', 'thematic'
    
    # Commitment tracking
    commitment_fulfillment: Dict[str, Any] = field(default_factory=dict)
    new_commitments: List[Dict[str, Any]] = field(default_factory=list)
    broken_commitments: List[Dict[str, Any]] = field(default_factory=list)
    
    # Sentiment analysis
    sentiment_trends: Dict[str, List[float]] = field(default_factory=dict)
    sentiment_shifts: List[Dict[str, Any]] = field(default_factory=list)
    
    # Topic analysis
    topic_evolution: Dict[str, Any] = field(default_factory=dict)
    escalated_topics: List[str] = field(default_factory=list)
    de_escalated_topics: List[str] = field(default_factory=list)
    
    # Summary metrics
    overall_score: float = 0.0
    confidence_level: float = 0.0
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the comparison results"""
        return {
            'documents_compared': len(self.documents),
            'comparison_type': self.comparison_type,
            'commitment_summary': {
                'fulfilled': len([c for c in self.commitment_fulfillment.values() if c.get('status') == 'fulfilled']),
                'pending': len([c for c in self.commitment_fulfillment.values() if c.get('status') == 'pending']),
                'broken': len(self.broken_commitments),
                'new': len(self.new_commitments)
            },
            'sentiment_summary': {
                'improving_topics': len([s for s in self.sentiment_shifts if s.get('direction') == 'positive']),
                'declining_topics': len([s for s in self.sentiment_shifts if s.get('direction') == 'negative']),
                'stable_topics': len([s for s in self.sentiment_shifts if s.get('direction') == 'stable'])
            },
            'topic_summary': {
                'escalated': len(self.escalated_topics),
                'de_escalated': len(self.de_escalated_topics)
            },
            'overall_score': self.overall_score,
            'confidence_level': self.confidence_level
        }
