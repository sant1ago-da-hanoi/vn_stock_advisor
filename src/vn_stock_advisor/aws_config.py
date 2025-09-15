"""
AWS Bedrock configuration for VN Stock Advisor
"""
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class AWSConfig:
    """AWS Bedrock configuration class"""
    
    def __init__(self):
        self.aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        self.aws_region = os.environ.get("AWS_REGION", "us-east-1")
        self.aws_session_token = os.environ.get("AWS_SESSION_TOKEN")  # Optional for temporary credentials
        
        # Model configurations
        self.claude_model = os.environ.get("AWS_CLAUDE_MODEL", "anthropic.claude-3-sonnet-20240229-v1:0")
        self.claude_reasoning_model = os.environ.get("AWS_CLAUDE_REASONING_MODEL", "anthropic.claude-3-5-sonnet-20241022-v2:0")
        self.titan_model = os.environ.get("AWS_TITAN_MODEL", "amazon.titan-text-express-v1")
        
        # Validate required credentials
        if not self.aws_access_key_id or not self.aws_secret_access_key:
            raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are required")
    
    def get_bedrock_config(self) -> dict:
        """Get Bedrock configuration for LiteLLM"""
        config = {
            "aws_access_key_id": self.aws_access_key_id,
            "aws_secret_access_key": self.aws_secret_access_key,
            "aws_region_name": self.aws_region,
        }
        
        if self.aws_session_token:
            config["aws_session_token"] = self.aws_session_token
            
        return config
    
    
    def get_model_config(self, model_type: str = "claude") -> dict:
        """Get model configuration for specific model type"""
        base_config = self.get_bedrock_config()
        
        if model_type == "claude":
            base_config["model"] = self.claude_model
        elif model_type == "claude_reasoning":
            base_config["model"] = self.claude_reasoning_model
        elif model_type == "titan":
            base_config["model"] = self.titan_model
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
            
        return base_config

# Available AWS Bedrock models
AWS_MODELS = {
    "claude": {
        "claude-3-sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
        "claude-3-haiku": "anthropic.claude-3-haiku-20240307-v1:0", 
        "claude-3-opus": "anthropic.claude-3-opus-20240229-v1:0",
        "claude-3-5-sonnet": "anthropic.claude-3-5-sonnet-20241022-v2:0",
        "claude-3-5-haiku": "anthropic.claude-3-5-haiku-20241022-v1:0",
    },
    "titan": {
        "titan-text-express": "amazon.titan-text-express-v1",
        "titan-text-lite": "amazon.titan-text-lite-v1",
        "titan-embed-text": "amazon.titan-embed-text-v1",
    },
    "jurassic": {
        "j2-ultra": "ai21.j2-ultra-v1",
        "j2-mid": "ai21.j2-mid-v1",
    }
}

def get_aws_llm_config(model_name: str, temperature: float = 0, max_tokens: int = 4096) -> dict:
    """Get LiteLLM configuration for AWS Bedrock model"""
    aws_config = AWSConfig()
    
    # Determine model type and get full model ID
    model_id = None
    for model_type, models in AWS_MODELS.items():
        if model_name in models:
            model_id = models[model_name]
            break
    
    if not model_id:
        raise ValueError(f"Model {model_name} not found in AWS_MODELS")
    
    config = aws_config.get_bedrock_config()
    config.update({
        "model": f"bedrock/{model_id}",
        "temperature": temperature,
        "max_tokens": max_tokens,
    })
    
    return config
