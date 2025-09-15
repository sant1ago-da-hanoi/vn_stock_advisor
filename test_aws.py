#!/usr/bin/env python3
"""
Test script for AWS Bedrock integration
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append('src')

def test_aws_config():
    """Test AWS configuration"""
    print("🔧 Testing AWS Configuration...")
    
    try:
        from vn_stock_advisor.aws_config import AWSConfig, AWS_MODELS
        
        config = AWSConfig()
        print("✅ AWS configuration loaded successfully")
        print(f"   Region: {config.aws_region}")
        print(f"   Claude model: {config.claude_model}")
        print(f"   Claude reasoning model: {config.claude_reasoning_model}")
        
        # Test bedrock config
        bedrock_config = config.get_bedrock_config()
        print(f"   Bedrock config keys: {list(bedrock_config.keys())}")
        
        # Show available models
        print("\n📋 Available AWS Models:")
        for model_type, models in AWS_MODELS.items():
            print(f"   {model_type.upper()}:")
            for name, model_id in models.items():
                print(f"     - {name}: {model_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ AWS configuration failed: {e}")
        return False

def test_llm_initialization():
    """Test LLM initialization"""
    print("\n🤖 Testing LLM Initialization...")
    
    try:
        from vn_stock_advisor.crew import llm, llm_reasoning, USE_AWS_MODELS, USE_GEMINI_MODELS
        
        print(f"   Using AWS models: {USE_AWS_MODELS}")
        print(f"   Using Gemini models: {USE_GEMINI_MODELS}")
        print(f"   Main LLM: {llm}")
        print(f"   Reasoning LLM: {llm_reasoning}")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM initialization failed: {e}")
        return False

def test_crew_creation():
    """Test crew creation"""
    print("\n👥 Testing Crew Creation...")
    
    try:
        from vn_stock_advisor.crew import VnStockAdvisor
        
        crew = VnStockAdvisor().crew()
        print("✅ Crew created successfully")
        print(f"   Agents: {len(crew.agents)}")
        print(f"   Tasks: {len(crew.tasks)}")
        
        # Test agent LLMs
        for i, agent in enumerate(crew.agents):
            print(f"   Agent {i}: {agent.llm}")
        
        return True
        
    except Exception as e:
        print(f"❌ Crew creation failed: {e}")
        return False

def test_simple_analysis():
    """Test simple analysis"""
    print("\n📊 Testing Simple Analysis...")
    
    try:
        from vn_stock_advisor.crew import VnStockAdvisor
        
        inputs = {
            "symbol": "HPG",
            "current_date": "2025-09-15"
        }
        
        print("   Running crew analysis...")
        crew = VnStockAdvisor().crew()
        result = crew.kickoff(inputs=inputs)
        
        print("✅ Analysis completed successfully")
        print(f"   Result type: {type(result)}")
        
        if hasattr(result, 'tasks_output'):
            print(f"   Tasks output: {len(result.tasks_output) if isinstance(result.tasks_output, list) else 'Not a list'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 VN Stock Advisor AWS Integration Test")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    
    # Check environment variables
    print("🔍 Checking Environment Variables...")
    required_vars = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION"]
    optional_vars = ["USE_AWS_MODELS", "USE_GEMINI_MODELS"]
    
    for var in required_vars:
        if os.environ.get(var):
            print(f"   ✅ {var}: {'*' * 10}")
        else:
            print(f"   ❌ {var}: Not set")
    
    for var in optional_vars:
        value = os.environ.get(var, "Not set")
        print(f"   ℹ️  {var}: {value}")
    
    print("\n" + "=" * 50)
    
    # Run tests
    tests = [
        test_aws_config,
        test_llm_initialization,
        test_crew_creation,
        # test_simple_analysis,  # Comment out to avoid long running test
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! AWS integration is working.")
    else:
        print("⚠️  Some tests failed. Check configuration and try again.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
