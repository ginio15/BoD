#!/usr/bin/env python3
"""
Live comparison tool for testing different providers with real documents
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Load .env file from project root
from dotenv import load_dotenv
load_dotenv(project_root / '.env')

from src.utils.optimized_analysis_engine import OptimizedAnalysisEngine
from src.utils.enhanced_analysis_engine import EnhancedAnalysisEngine
from src.utils.document_parser import DocumentParser
from src.utils.llm_providers import LLMProviderManager

def get_available_test_documents():
    """Get list of available test documents"""
    documents = []
    
    # Check test_documents folder
    test_docs_dir = project_root / 'data' / 'test_documents'
    if test_docs_dir.exists():
        for file_path in test_docs_dir.glob('*.txt'):
            documents.append({
                'name': file_path.name,
                'path': file_path,
                'type': 'text',
                'size': file_path.stat().st_size
            })
    
    # Check uploads folder
    uploads_dir = project_root / 'data' / 'uploads'
    if uploads_dir.exists():
        for file_path in uploads_dir.glob('*.txt'):
            documents.append({
                'name': file_path.name,
                'path': file_path,
                'type': 'text',
                'size': file_path.stat().st_size
            })
        for file_path in uploads_dir.glob('*.pdf'):
            documents.append({
                'name': file_path.name,
                'path': file_path,
                'type': 'pdf',
                'size': file_path.stat().st_size
            })
    
    return documents

def display_document_menu(documents):
    """Display document selection menu"""
    print("\n📁 Available Test Documents:")
    print("-" * 50)
    
    for i, doc in enumerate(documents, 1):
        size_kb = doc['size'] / 1024
        print(f"   {i:2}. {doc['name']:30} ({doc['type']:4}) {size_kb:6.1f} KB")
    
    print(f"   {len(documents) + 1:2}. Enter custom file path")
    print(f"    0. Exit")

def select_document(documents):
    """Let user select a document"""
    while True:
        display_document_menu(documents)
        
        try:
            choice = input(f"\nSelect document (1-{len(documents) + 1}, 0 to exit): ").strip()
            
            if choice == "0":
                return None
                
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(documents):
                return documents[choice_num - 1]
            elif choice_num == len(documents) + 1:
                custom_path = input("Enter file path: ").strip()
                custom_file = Path(custom_path)
                if custom_file.exists():
                    return {
                        'name': custom_file.name,
                        'path': custom_file,
                        'type': custom_file.suffix[1:] if custom_file.suffix else 'unknown',
                        'size': custom_file.stat().st_size
                    }
                else:
                    print(f"❌ File not found: {custom_path}")
            else:
                print(f"❌ Invalid choice. Please select 1-{len(documents) + 1} or 0.")
                
        except ValueError:
            print("❌ Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return None

def display_provider_menu(available_providers):
    """Display provider selection menu"""
    print("\n🤖 Available Providers:")
    print("-" * 30)
    
    for i, provider in enumerate(available_providers, 1):
        status = "🟢" if provider == "ollama" else "🔵"
        cost = "FREE" if provider == "ollama" else "PAID"
        print(f"   {i}. {status} {provider.capitalize():10} ({cost})")
    
    print(f"   {len(available_providers) + 1}. Compare all providers")
    print(f"    0. Back to document selection")

def select_providers(available_providers):
    """Let user select provider(s)"""
    while True:
        display_provider_menu(available_providers)
        
        try:
            choice = input(f"\nSelect provider (1-{len(available_providers) + 1}, 0 to go back): ").strip()
            
            if choice == "0":
                return None
                
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(available_providers):
                return [available_providers[choice_num - 1]]
            elif choice_num == len(available_providers) + 1:
                return available_providers
            else:
                print(f"❌ Invalid choice. Please select 1-{len(available_providers) + 1} or 0.")
                
        except ValueError:
            print("❌ Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return None

def analyze_document(doc_info, provider, use_enhanced=False):
    """Analyze document with specified provider"""
    print(f"\n🔍 Analyzing {doc_info['name']} with {provider.capitalize()}...")
    
    try:
        # Parse document
        parser = DocumentParser()
        
        if doc_info['type'] == 'text' or doc_info['name'].endswith('.txt'):
            with open(doc_info['path'], 'r', encoding='utf-8') as f:
                content = f.read()
            # Create a simple processed document
            from src.models.document import ProcessedDocument, DocumentMetadata, DocumentPage
            metadata = DocumentMetadata(
                filename=doc_info['name'],
                file_type='txt',
                total_pages=1,
                word_count=len(content.split())
            )
            page = DocumentPage(page_number=1, text=content)
            document = ProcessedDocument(pages=[page], metadata=metadata, full_text=content)
        else:
            document = parser.process_document(str(doc_info['path']))
        
        print(f"   Document loaded: {len(document.full_text):,} characters")
        
        # Select engine and analyze
        if use_enhanced and provider in ["openai", "mistral"]:
            engine = EnhancedAnalysisEngine()
            start_time = time.time()
            results = engine.analyze_document_enhanced(document, provider=provider)
            end_time = time.time()
        else:
            engine = OptimizedAnalysisEngine()
            start_time = time.time()
            results = engine.analyze_document_optimized(document, provider=provider)
            end_time = time.time()
        
        duration = end_time - start_time
        
        # Extract metrics
        commitments = results.get('enhanced_commitments', results.get('commitments', []))
        risks = results.get('risk_assessment', results.get('risks', []))
        financial = results.get('financial_insights', [])
        sentiment = results.get('sentiment_analysis', results.get('sentiment', {}))
        priorities = results.get('strategic_priorities', [])
        executive_summary = results.get('executive_summary', '')
        
        analysis_result = {
            'provider': provider,
            'document': doc_info['name'],
            'duration': duration,
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'metrics': {
                'commitments': len(commitments),
                'risks': len(risks),
                'financial_insights': len(financial),
                'strategic_priorities': len(priorities),
                'has_sentiment': bool(sentiment),
                'has_executive_summary': bool(executive_summary),
                'document_length': len(document.full_text)
            },
            'sample_results': {
                'first_commitment': commitments[0] if commitments else None,
                'first_risk': risks[0] if risks else None,
                'sentiment_summary': sentiment.get('overall', 'N/A') if sentiment else 'N/A',
                'executive_summary_preview': executive_summary[:200] + '...' if len(executive_summary) > 200 else executive_summary
            }
        }
        
        print(f"✅ Analysis completed in {duration:.1f} seconds")
        print(f"   📋 Commitments: {analysis_result['metrics']['commitments']}")
        print(f"   ⚠️  Risks: {analysis_result['metrics']['risks']}")
        print(f"   💰 Financial insights: {analysis_result['metrics']['financial_insights']}")
        print(f"   🎯 Strategic priorities: {analysis_result['metrics']['strategic_priorities']}")
        print(f"   😊 Sentiment: {analysis_result['sample_results']['sentiment_summary']}")
        
        if executive_summary:
            print(f"   📄 Executive summary: {len(executive_summary)} characters")
        
        return analysis_result
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return {
            'provider': provider,
            'document': doc_info['name'],
            'duration': 0,
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def save_results(results, doc_name):
    """Save comparison results to file"""
    # Create results directory if it doesn't exist
    results_dir = project_root / 'tests' / 'outputs'
    results_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"live_comparison_{doc_name}_{timestamp}.json"
    results_file = results_dir / filename
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {results_file}")
    return results_file

def display_comparison_results(results):
    """Display formatted comparison results"""
    print(f"\n📊 LIVE COMPARISON RESULTS")
    print("=" * 60)
    
    successful_results = [r for r in results if r['success']]
    failed_results = [r for r in results if not r['success']]
    
    if successful_results:
        print("\n⚡ Performance Summary:")
        print(f"{'Provider':12} {'Duration':10} {'Commits':8} {'Risks':6} {'Financial':9} {'Sentiment':9}")
        print("-" * 65)
        
        for result in successful_results:
            metrics = result['metrics']
            sentiment_status = "✅" if metrics['has_sentiment'] else "❌"
            print(f"{result['provider'].capitalize():12} {result['duration']:8.1f}s {metrics['commitments']:7} {metrics['risks']:5} {metrics['financial_insights']:8} {sentiment_status:8}")
        
        # Performance leader
        fastest = min(successful_results, key=lambda r: r['duration'])
        print(f"\n🏆 Fastest: {fastest['provider'].capitalize()} ({fastest['duration']:.1f}s)")
        
        # Quality leader
        most_comprehensive = max(successful_results, 
                               key=lambda r: sum([r['metrics']['commitments'], 
                                                r['metrics']['risks'], 
                                                r['metrics']['financial_insights']]))
        total_insights = sum([most_comprehensive['metrics']['commitments'], 
                            most_comprehensive['metrics']['risks'], 
                            most_comprehensive['metrics']['financial_insights']])
        print(f"🎯 Most comprehensive: {most_comprehensive['provider'].capitalize()} ({total_insights} insights)")
        
        print(f"\n📋 Sample Analysis Quality:")
        for result in successful_results:
            sample = result['sample_results']
            print(f"\n{result['provider'].capitalize()}:")
            if sample.get('first_commitment'):
                commitment_text = sample['first_commitment'].get('text', 
                                sample['first_commitment'].get('exact_text', 'N/A'))
                print(f"   💼 Sample commitment: {commitment_text[:60]}...")
            if sample.get('executive_summary_preview'):
                print(f"   📄 Executive summary: {sample['executive_summary_preview']}")
    
    if failed_results:
        print(f"\n❌ Failed Analyses:")
        for result in failed_results:
            print(f"   {result['provider'].capitalize()}: {result.get('error', 'Unknown error')}")

def main():
    """Main live comparison interface"""
    print("🚀 Live Comparison Tool")
    print("=" * 50)
    print("Compare different LLM providers with real documents")
    
    # Check available providers
    manager = LLMProviderManager()
    available_providers = manager.get_available_providers()
    
    if not available_providers:
        print("❌ No LLM providers available. Please configure at least one provider.")
        return
    
    print(f"Available providers: {', '.join(available_providers)}")
    
    # Get available documents
    documents = get_available_test_documents()
    
    if not documents:
        print("❌ No test documents found. Please add documents to data/test_documents/ or data/uploads/")
        return
    
    while True:
        try:
            # Select document
            selected_doc = select_document(documents)
            if selected_doc is None:
                break
            
            print(f"\n📄 Selected: {selected_doc['name']} ({selected_doc['size']/1024:.1f} KB)")
            
            # Select provider(s)
            selected_providers = select_providers(available_providers)
            if selected_providers is None:
                continue
            
            print(f"\n🤖 Testing with: {', '.join(selected_providers)}")
            
            # Run analyses
            results = []
            for provider in selected_providers:
                result = analyze_document(selected_doc, provider)
                results.append(result)
            
            # Display results
            display_comparison_results(results)
            
            # Save results
            save_results(results, selected_doc['name'].replace('.', '_'))
            
            # Continue or exit
            while True:
                choice = input(f"\nContinue with another test? (y/n): ").strip().lower()
                if choice in ['y', 'yes']:
                    break
                elif choice in ['n', 'no']:
                    print("\n👋 Thanks for using the Live Comparison Tool!")
                    return
                else:
                    print("Please enter 'y' or 'n'")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()