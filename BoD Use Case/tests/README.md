# Tests Directory - BoD Presentation Analysis System v2.1.0

This directory contains all testing files and test outputs for the Board of Directors Presentation Analysis System.

## Directory Structure

### Test Scripts
- **Core System Tests:**
  - `test_system.py` - Basic system functionality tests
  - `test_final_system.py` - Final system validation
  - `final_system_test.py` - Comprehensive system test
  - `final_verification_test.py` - Final verification and validation

- **Analysis Engine Tests:**
  - `test_enhanced_analysis.py` - Enhanced analysis engine tests
  - `test_optimized_engine.py` - Optimized analysis engine tests
  - `test_comprehensive_analysis.py` - Comprehensive analysis tests

- **OCR and PPTX Tests:**
  - `test_enhanced_pptx_ocr.py` - Enhanced PPTX OCR functionality
  - `test_pptx_comprehensive.py` - Comprehensive PPTX processing
  - `test_pptx_files.py` - PPTX file processing tests
  - `test_pptx_final.py` - Final PPTX testing
  - `test_ocr_consistency.py` - OCR consistency validation

- **Application Tests:**
  - `test_apps.py` - Application interface tests
  - `test_fixed_app.py` - Fixed application functionality
  - `test_complete_pipeline.py` - Complete processing pipeline

- **LLM and Integration Tests:**
  - `test_ollama.py` - Ollama LLM integration tests
  - `test_optimized_prompts.py` - Optimized prompt testing
  - `test_optimized_fixes.py` - Optimization fixes validation

- **Consistency and Validation:**
  - `test_consistency.py` - System consistency tests
  - `test_no_ocr.py` - Non-OCR processing tests

### Quick Tests
- `quick_test.py` - Quick system validation
- `quick_test_optimized.py` - Optimized quick testing

### Demo and Analysis Scripts
- `demo.py` - Basic demonstration script
- `demo_complete_system.py` - Complete system demonstration
- `debug_analysis.py` - Analysis debugging utilities
- `simple_comprehensive_test.py` - Simplified comprehensive testing

### Utility Scripts
- `create_samples.py` - Sample data creation
- `inspect_word_count.py` - Word count inspection
- `final_word_count_validation.py` - Word count validation
- `final_status_report.py` - Final status reporting

### Test Outputs (`outputs/` folder)
- `comprehensive_test.txt` - Comprehensive test results
- `demo_output.txt` - Demo execution outputs  
- `test_output.txt` - General test outputs
- `consistency_test_results.json` - Consistency test results

## Usage

### Running Quick Tests
```bash
# Basic quick test
python tests/quick_test.py

# Optimized quick test  
python tests/quick_test_optimized.py
```

### Running Comprehensive Tests
```bash
# Full system test
python tests/final_system_test.py

# Complete pipeline test
python tests/test_complete_pipeline.py
```

### Running Demo
```bash
# Basic demo
python tests/demo.py

# Complete system demo
python tests/demo_complete_system.py
```

## Test Categories

1. **Unit Tests** - Individual component testing
2. **Integration Tests** - Component interaction testing  
3. **System Tests** - End-to-end system validation
4. **Performance Tests** - System performance validation
5. **Consistency Tests** - Output consistency validation

## Notes

- All test output files are organized in the `outputs/` subfolder
- Test scripts are designed to work with the v2.1.0 production system
- Most tests can be run independently or as part of the full test suite
- Demo scripts provide examples of system usage and capabilities

For detailed information about specific tests, refer to the individual test files and their documentation.
