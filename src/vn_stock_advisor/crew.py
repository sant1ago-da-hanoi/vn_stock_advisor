from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool
from vn_stock_advisor.tools.custom_tool import FundDataTool, TechDataTool, FileReadTool
from vn_stock_advisor.aws_config import AWSConfig
from pydantic import BaseModel, Field
from typing import List, Literal
from dotenv import load_dotenv
import os, json
import warnings
warnings.filterwarnings("ignore") # Suppress unimportant warnings

# Load environment variables
load_dotenv()

# Model selection flags
USE_AWS_MODELS = os.environ.get("USE_AWS_MODELS", "false").lower() == "true"
USE_GEMINI_MODELS = os.environ.get("USE_GEMINI_MODELS", "true").lower() == "true"

# API Keys
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL")
GEMINI_REASONING_MODEL = os.environ.get("GEMINI_REASONING_MODEL")
SERPER_API_KEY = os.environ.get("SERPER_API_KEY")

# Initialize LLM based on configuration
if USE_AWS_MODELS:
    aws_config = AWSConfig()
    
    # Set environment variables for AWS Bedrock
    os.environ["AWS_ACCESS_KEY_ID"] = aws_config.aws_access_key_id
    os.environ["AWS_SECRET_ACCESS_KEY"] = aws_config.aws_secret_access_key
    os.environ["AWS_REGION_NAME"] = aws_config.aws_region
    
    if aws_config.aws_session_token:
        os.environ["AWS_SESSION_TOKEN"] = aws_config.aws_session_token
    
    # Create LLM with Claude model
    main_llm = LLM(
        model="bedrock/apac.anthropic.claude-sonnet-4-20250514-v1:0",
        temperature=0,
        max_tokens=4096
    )
    
    # Create reasoning LLM
    reasoning_llm = LLM(
        model="bedrock/apac.anthropic.claude-sonnet-4-20250514-v1:0",
        temperature=0,
        max_tokens=4096
    )
    print("✅ Using AWS Bedrock models (Claude)")

else:
    # Create Gemini LLMs
    main_llm = LLM(
        model=GEMINI_MODEL,
        api_key=GEMINI_API_KEY,
        temperature=0,
        max_tokens=4096
    )

    reasoning_llm = LLM(
        model=GEMINI_REASONING_MODEL if GEMINI_REASONING_MODEL else GEMINI_MODEL,
        api_key=GEMINI_API_KEY,
        temperature=0,
        max_tokens=4096
    )
    print("✅ Using Google Gemini models")

# Set the LLM variables for backward compatibility
llm = main_llm

# Initialize the tools
file_read_tool = FileReadTool(file_path="knowledge/PE_PB_industry_average.json")
fund_tool=FundDataTool()
tech_tool=TechDataTool(result_as_answer=True)
scrape_tool = ScrapeWebsiteTool()
# Use standard SerperDevTool with reduced results
search_tool = SerperDevTool(
    country="vn",
    locale="vn",
    location="Hanoi, Hanoi, Vietnam",
    n_results=3
)
# Skip web search tool - it's causing too many issues with AWS Bedrock
# The search_tool (SerperDevTool) is sufficient for web search functionality
web_search_tool = None

# Skip JSON knowledge source for now to avoid OpenAI API key issues
# json_source = JSONKnowledgeSource(
#     file_paths=["PE_PB_industry_average.json"]
# )
json_source = None

# Create Pydantic Models for Structured Output
class InvestmentDecision(BaseModel):
    stock_ticker: str = Field(..., description="Mã cổ phiếu")
    full_name: str = Field(..., description="Tên đầy đủ công ty")
    industry: str =Field(..., description="Lĩnh vực kinh doanh")
    today_date: str = Field(..., description="Ngày phân tích")
    decision: str = Field(..., description="Quyết định mua, giữ hay bán cổ phiếu")
    macro_reasoning: str = Field(..., description="Giải thích quyết định từ góc nhìn kinh tế vĩ mô và các chính sách quan trọng")
    fund_reasoning: str = Field(..., description="Giải thích quyết định từ góc độ phân tích cơ bản")
    tech_reasoning: str = Field(..., description="Giải thích quyết định từ góc độ phân tích kỹ thuật")
    buy_price: float = Field(..., description="Giá mua cổ phiếu khuyến nghị dựa trên phân tích kỹ thuật")
    sell_price: float = Field(..., description="Giá bán cổ phiếu khuyến nghị dựa trên phân tích kỹ thuật")

@CrewBase
class VnStockAdvisor():
    """VnStockAdvisor crew"""

    # Create type-hinted class attributes that expects a list of agents and a list of tasks
    agents: List[BaseAgent] # ← auto-filled with all the @agent-decorated outputs
    tasks: List[Task]       # ← auto-filled with all the @task-decorated outputs

    @agent
    def stock_news_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["stock_news_researcher"],
            verbose=True,
            llm=llm,
            tools=[search_tool, scrape_tool],
            max_rpm=5
        )

    @agent
    def fundamental_analyst(self) -> Agent:
        # Configure embedder based on model provider
        embedder_config = None
        
        if USE_AWS_MODELS:
            # For AWS, skip embedder configuration to avoid schema issues
            embedder_config = None
        elif 'GEMINI_API_KEY' in locals() and GEMINI_API_KEY:
            embedder_config = {
                "provider": "google",
                "config": {
                    "model": "models/text-embedding-004",
                    "api_key": GEMINI_API_KEY,
                }
            }
        
        return Agent(
            config=self.agents_config["fundamental_analyst"],
            verbose=True,
            llm=llm,
            tools=[fund_tool, file_read_tool],
            knowledge_sources=[json_source] if json_source else [],
            max_rpm=5,
            embedder=embedder_config
        )

    @agent
    def technical_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["technical_analyst"],
            verbose=True,
            llm=llm,
            tools=[tech_tool],
            max_rpm=5
        )
    
    @agent
    def investment_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config["investment_strategist"],
            verbose=True,
            llm=reasoning_llm,
            max_rpm=5
        )

    @task
    def news_collecting(self) -> Task:
        return Task(
            config=self.tasks_config["news_collecting"],
            async_execution=True
        )

    @task
    def fundamental_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["fundamental_analysis"],
            async_execution=True
        )

    @task
    def technical_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["technical_analysis"],
            async_execution=True
        )
    
    @task
    def investment_decision(self) -> Task:
        return Task(
            config=self.tasks_config["investment_decision"],
            context=[self.news_collecting(), self.fundamental_analysis(), self.technical_analysis()],
            output_json=InvestmentDecision
        )

    @crew
    def crew(self) -> Crew:
        """Creates the VnStockAdvisor crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True
        )