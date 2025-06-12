#!/usr/bin/env python3
"""
Interactive guide for running comparison tests
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def display_main_menu():
    """Display the main comparison menu"""
    print("\n🧪 BoD Analysis Comparison Guide")
    print("=" * 50)
    print("Choose a comparison test to run:")
    print()
    print("1. 🔧 Test OpenAI Configuration")
    print("   - Verify OpenAI API key and basic functionality")
    print("   - Quick test with sample document")
    print()
    print("2. ⚡ Simple Comparison (OpenAI vs Ollama)")
    print("   - Quick performance comparison")
    print("   - Basic analysis metrics")
    print()
    print("3. 🧪 Comprehensive Comparison")
    print("   - Detailed analysis quality comparison")
    print("   - Multiple metrics and sample outputs")
    print()
    print("4. 🔴 Live Comparison Tool")
    print("   - Interactive tool with your own documents")
    print("   - Real-time provider selection")
    print()
    print("5. 📖 View Comparison Guide")
    print("   - Tips for choosing the right provider")
    print("   - Performance vs cost considerations")
    print()
    print("0. Exit")

def run_openai_config_test():
    """Run OpenAI configuration test"""
    print("\n🔧 Running OpenAI Configuration Test...")
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, 
            str(project_root / 'tests' / 'comparison' / 'test_openai_config.py')
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Failed to run test: {e}")
        return False

def run_simple_comparison():
    """Run simple comparison test"""
    print("\n⚡ Running Simple Comparison...")
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, 
            str(project_root / 'tests' / 'comparison' / 'simple_comparison.py')
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Failed to run test: {e}")
        return False

def run_comprehensive_comparison():
    """Run comprehensive comparison test"""
    print("\n🧪 Running Comprehensive Comparison...")
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, 
            str(project_root / 'tests' / 'comparison' / 'test_openai_vs_ollama.py')
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Failed to run test: {e}")
        return False

def run_live_comparison():
    """Run live comparison tool"""
    print("\n🔴 Starting Live Comparison Tool...")
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, 
            str(project_root / 'tests' / 'comparison' / 'live_comparison.py')
        ])
        return True
    except Exception as e:
        print(f"❌ Failed to run tool: {e}")
        return False

def show_comparison_guide():
    """Display comparison guide information"""
    print("\n📖 BoD Analysis Provider Comparison Guide")
    print("=" * 60)
    
    print("\n🤖 Provider Overview:")
    print("┌─────────────┬──────────┬─────────┬──────────┬─────────────┐")
    print("│ Provider    │ Cost     │ Speed   │ Quality  │ Best For    │")
    print("├─────────────┼──────────┼─────────┼──────────┼─────────────┤")
    print("│ Ollama      │ FREE     │ ~25s    │ Very Good│ Daily Use   │")
    print("│ OpenAI      │ $0.01-05 │ ~18s    │ Excellent│ Critical    │")
    print("│ Mistral     │ $0.01-03 │ ~22s    │ Good     │ Cost-Aware  │")
    print("└─────────────┴──────────┴─────────┴──────────┴─────────────┘")
    
    print("\n💡 Choosing the Right Provider:")
    print("   🆓 Ollama: Best for regular analysis, no ongoing costs")
    print("   🚀 OpenAI: Best for complex documents requiring high accuracy")
    print("   💰 Mistral: Good balance of cost and quality")
    
    print("\n⚡ Performance Considerations:")
    print("   • Document length affects processing time")
    print("   • Complex documents may benefit from premium providers")
    print("   • Ollama requires local installation but is completely free")
    print("   • Cloud providers need API keys and have usage costs")
    
    print("\n🎯 Recommendation:")
    print("   1. Start with Ollama for daily board analysis tasks")
    print("   2. Use OpenAI for critical presentations or complex documents")
    print("   3. Consider Mistral as a cost-effective premium alternative")
    
    print("\n🔧 Setup Requirements:")
    print("   • Ollama: Install from https://ollama.ai and run 'ollama pull llama3.2:3b'")
    print("   • OpenAI: Set OPENAI_API_KEY in your .env file")
    print("   • Mistral: Set MISTRAL_API_KEY in your .env file")
    
    # Read additional guide from docs if available
    guide_file = project_root / 'docs' / 'guides' / 'ui_comparison_guide.txt'
    if guide_file.exists():
        print(f"\n📄 Additional Information:")
        print(f"   See detailed guide: {guide_file}")
    
    input("\nPress Enter to continue...")

def main():
    """Main interactive guide"""
    print("🚀 Welcome to the BoD Analysis Comparison Suite!")
    
    while True:
        try:
            display_main_menu()
            
            choice = input("\nSelect an option (0-5): ").strip()
            
            if choice == "0":
                print("\n👋 Thank you for using the comparison suite!")
                break
            elif choice == "1":
                run_openai_config_test()
            elif choice == "2":
                run_simple_comparison()
            elif choice == "3":
                run_comprehensive_comparison()
            elif choice == "4":
                run_live_comparison()
            elif choice == "5":
                show_comparison_guide()
            else:
                print("❌ Invalid choice. Please select 0-5.")
            
            if choice in ["1", "2", "3"]:
                input("\nPress Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()