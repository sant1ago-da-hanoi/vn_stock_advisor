from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import uvicorn
from datetime import date
import json
import asyncio

from .crew import VnStockAdvisor

app = FastAPI(
    title="VN Stock Advisor API",
    description="API cho hệ thống phân tích cổ phiếu Việt Nam sử dụng Multi-AI-Agent",
    version="0.4.1"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production nên chỉ định domain cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class StockAnalysisRequest(BaseModel):
    symbol: str = Field(..., description="Mã cổ phiếu cần phân tích", example="HPG")
    current_date: Optional[str] = Field(None, description="Ngày phân tích (YYYY-MM-DD), mặc định là hôm nay")

class MarketAnalysisResponse(BaseModel):
    symbol: str
    analysis_date: str
    news_summary: str
    market_impact: str

class FundamentalAnalysisResponse(BaseModel):
    symbol: str
    company_name: str
    industry: str
    analysis_date: str
    financial_ratios: Dict[str, Any]
    quarterly_trends: Dict[str, Any]
    valuation_assessment: str
    performance_evaluation: str

class TechnicalAnalysisResponse(BaseModel):
    symbol: str
    company_name: str
    industry: str
    analysis_date: str
    current_price: float
    current_volume: float
    technical_indicators: Dict[str, Any]
    support_resistance: Dict[str, Any]
    trend_analysis: str
    technical_signals: str

class InvestmentDecisionResponse(BaseModel):
    stock_ticker: str
    full_name: str
    industry: str
    today_date: str
    decision: str
    macro_reasoning: str
    fund_reasoning: str
    tech_reasoning: str
    buy_price: float
    sell_price: float
    overall_score: float

class CompleteAnalysisResponse(BaseModel):
    symbol: str
    analysis_date: str
    market_analysis: MarketAnalysisResponse
    fundamental_analysis: FundamentalAnalysisResponse
    technical_analysis: TechnicalAnalysisResponse
    investment_decision: InvestmentDecisionResponse

@app.get("/")
async def root():
    return {
        "message": "VN Stock Advisor API",
        "version": "0.4.1",
        "description": "API cho hệ thống phân tích cổ phiếu Việt Nam"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": str(date.today())}

# Cache management endpoints removed - using standard SerperDevTool

@app.post("/analyze/market", response_model=MarketAnalysisResponse)
async def analyze_market(request: StockAnalysisRequest):
    """
    Phân tích tin tức vĩ mô và tác động thị trường
    """
    try:
        inputs = {
            "symbol": request.symbol,
            "current_date": request.current_date or str(date.today())
        }
        
        # Tạo crew và chạy toàn bộ pipeline
        crew = VnStockAdvisor().crew()
        result = crew.kickoff(inputs=inputs)
        
        # Lấy output từ task đầu tiên (news_collecting)
        # Thử nhiều cách khác nhau để lấy task output
        news_task_output = ""
        
        if hasattr(result, 'tasks_output'):
            tasks_output = result.tasks_output
            if isinstance(tasks_output, dict):
                # Nếu là dict, lấy theo key
                news_task_output = tasks_output.get('news_collecting', '')
            elif isinstance(tasks_output, list) and len(tasks_output) > 0:
                # Nếu là list, lấy task đầu tiên
                first_task = tasks_output[0]
                if hasattr(first_task, 'output'):
                    news_task_output = first_task.output
                elif hasattr(first_task, 'raw'):
                    news_task_output = first_task.raw
                else:
                    news_task_output = str(first_task)
        
        # Fallback: nếu không lấy được, trả về string representation của toàn bộ result
        if not news_task_output:
            news_task_output = str(result) if result else ""
        
        return MarketAnalysisResponse(
            symbol=request.symbol,
            analysis_date=inputs["current_date"],
            news_summary=news_task_output[:500] + "..." if len(news_task_output) > 500 else news_task_output,
            market_impact="Phân tích tác động thị trường từ tin tức vĩ mô"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi phân tích thị trường: {str(e)}")

@app.post("/analyze/fundamental", response_model=FundamentalAnalysisResponse)
async def analyze_fundamental(request: StockAnalysisRequest):
    """
    Phân tích cơ bản cổ phiếu
    """
    try:
        inputs = {
            "symbol": request.symbol,
            "current_date": request.current_date or str(date.today())
        }
        
        crew = VnStockAdvisor().crew()
        result = crew.kickoff(inputs=inputs)
        
        # Lấy output từ task thứ 2 (fundamental_analysis)
        fundamental_output = ""
        
        if hasattr(result, 'tasks_output'):
            tasks_output = result.tasks_output
            if isinstance(tasks_output, dict):
                fundamental_output = tasks_output.get('fundamental_analysis', '')
            elif isinstance(tasks_output, list) and len(tasks_output) > 1:
                second_task = tasks_output[1]
                if hasattr(second_task, 'output'):
                    fundamental_output = second_task.output
                elif hasattr(second_task, 'raw'):
                    fundamental_output = second_task.raw
                else:
                    fundamental_output = str(second_task)
        
        if not fundamental_output:
            fundamental_output = str(result) if result else ""
        
        return FundamentalAnalysisResponse(
            symbol=request.symbol,
            company_name="Công ty cổ phần",
            industry="Chưa xác định",
            analysis_date=inputs["current_date"],
            financial_ratios={},
            quarterly_trends={},
            valuation_assessment=fundamental_output[:300] + "..." if len(fundamental_output) > 300 else fundamental_output,
            performance_evaluation="Đánh giá hiệu suất tài chính"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi phân tích cơ bản: {str(e)}")

@app.post("/analyze/technical", response_model=TechnicalAnalysisResponse)
async def analyze_technical(request: StockAnalysisRequest):
    """
    Phân tích kỹ thuật cổ phiếu
    """
    try:
        inputs = {
            "symbol": request.symbol,
            "current_date": request.current_date or str(date.today())
        }
        
        crew = VnStockAdvisor().crew()
        result = crew.kickoff(inputs=inputs)
        
        # Lấy output từ task thứ 3 (technical_analysis)
        technical_output = ""
        
        if hasattr(result, 'tasks_output'):
            tasks_output = result.tasks_output
            if isinstance(tasks_output, dict):
                technical_output = tasks_output.get('technical_analysis', '')
            elif isinstance(tasks_output, list) and len(tasks_output) > 2:
                third_task = tasks_output[2]
                if hasattr(third_task, 'output'):
                    technical_output = third_task.output
                elif hasattr(third_task, 'raw'):
                    technical_output = third_task.raw
                else:
                    technical_output = str(third_task)
        
        if not technical_output:
            technical_output = str(result) if result else ""
        
        return TechnicalAnalysisResponse(
            symbol=request.symbol,
            company_name="Công ty cổ phần",
            industry="Chưa xác định",
            analysis_date=inputs["current_date"],
            current_price=0.0,
            current_volume=0,
            technical_indicators={},
            support_resistance={},
            trend_analysis=technical_output[:300] + "..." if len(technical_output) > 300 else technical_output,
            technical_signals="Tín hiệu kỹ thuật"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi phân tích kỹ thuật: {str(e)}")

@app.post("/analyze/decision", response_model=InvestmentDecisionResponse)
async def get_investment_decision(request: StockAnalysisRequest):
    """
    Lấy quyết định đầu tư cuối cùng
    """
    try:
        inputs = {
            "symbol": request.symbol,
            "current_date": request.current_date or str(date.today())
        }
        
        crew = VnStockAdvisor().crew()
        result = crew.kickoff(inputs=inputs)
        
        # Lấy output từ task thứ 4 (investment_decision)
        decision_output = {}
        
        if hasattr(result, 'tasks_output'):
            tasks_output = result.tasks_output
            if isinstance(tasks_output, dict):
                decision_output = tasks_output.get('investment_decision', {})
            elif isinstance(tasks_output, list) and len(tasks_output) > 3:
                fourth_task = tasks_output[3]
                if hasattr(fourth_task, 'output'):
                    decision_output = fourth_task.output
                elif hasattr(fourth_task, 'raw'):
                    decision_output = fourth_task.raw
                else:
                    decision_output = str(fourth_task)
        
        if not decision_output:
            decision_output = str(result) if result else {}
        
        # Try to parse as JSON if it's a string
        if isinstance(decision_output, str):
            try:
                import json
                decision_output = json.loads(decision_output)
            except:
                decision_output = {}
        
        # Nếu là dict, parse thành InvestmentDecisionResponse
        if isinstance(decision_output, dict):
            return InvestmentDecisionResponse(
                stock_ticker=decision_output.get('stock_ticker', request.symbol),
                full_name=decision_output.get('full_name', ''),
                industry=decision_output.get('industry', ''),
                today_date=decision_output.get('today_date', inputs["current_date"]),
                decision=decision_output.get('decision', 'GIỮ'),
                macro_reasoning=decision_output.get('macro_reasoning', ''),
                fund_reasoning=decision_output.get('fund_reasoning', ''),
                tech_reasoning=decision_output.get('tech_reasoning', ''),
                buy_price=decision_output.get('buy_price', 0.0),
                sell_price=decision_output.get('sell_price', 0.0),
                overall_score=7.5  # Placeholder
            )
        else:
            # Fallback nếu không parse được
            return InvestmentDecisionResponse(
                stock_ticker=request.symbol,
                full_name="Công ty cổ phần",
                industry="Chưa xác định",
                today_date=inputs["current_date"],
                decision="GIỮ",
                macro_reasoning=str(decision_output)[:200],
                fund_reasoning="Phân tích cơ bản",
                tech_reasoning="Phân tích kỹ thuật",
                buy_price=0.0,
                sell_price=0.0,
                overall_score=7.5
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi lấy quyết định đầu tư: {str(e)}")

@app.post("/analyze/complete", response_model=CompleteAnalysisResponse)
async def complete_analysis(request: StockAnalysisRequest):
    """
    Thực hiện phân tích toàn diện và trả về tất cả kết quả
    """
    try:
        inputs = {
            "symbol": request.symbol,
            "current_date": request.current_date or str(date.today())
        }
        
        crew = VnStockAdvisor().crew()
        # Add timeout to prevent hanging
        result = await asyncio.wait_for(
            asyncio.to_thread(crew.kickoff, inputs=inputs),
            timeout=60  # 1 minute timeout - force faster completion
        )
        
        # Parse tất cả kết quả - xử lý cả dict và list
        tasks_output = getattr(result, 'tasks_output', {})
        
        # Helper function để lấy task output an toàn
        def get_task_output(task_name, task_index):
            output = ""
            
            if isinstance(tasks_output, dict):
                output = tasks_output.get(task_name, '')
            elif isinstance(tasks_output, list) and len(tasks_output) > task_index:
                task = tasks_output[task_index]
                if hasattr(task, 'output'):
                    output = task.output
                elif hasattr(task, 'raw'):
                    output = task.raw
                else:
                    output = str(task)
            
            if not output:
                output = str(result) if result else ""
            
            return output
        
        # Tạo response cho từng phần
        news_output = get_task_output('news_collecting', 0)
        market_analysis = MarketAnalysisResponse(
            symbol=request.symbol,
            analysis_date=inputs["current_date"],
            news_summary=news_output[:500] + "..." if len(str(news_output)) > 500 else str(news_output),
            market_impact="Phân tích tác động thị trường"
        )
        
        fundamental_output = get_task_output('fundamental_analysis', 1)
        fundamental_analysis = FundamentalAnalysisResponse(
            symbol=request.symbol,
            company_name="Công ty cổ phần",
            industry="Chưa xác định",
            analysis_date=inputs["current_date"],
            financial_ratios={},
            quarterly_trends={},
            valuation_assessment=str(fundamental_output)[:300] + "..." if len(str(fundamental_output)) > 300 else str(fundamental_output),
            performance_evaluation="Đánh giá hiệu suất tài chính"
        )
        
        technical_output = get_task_output('technical_analysis', 2)
        technical_analysis = TechnicalAnalysisResponse(
            symbol=request.symbol,
            company_name="Công ty cổ phần",
            industry="Chưa xác định",
            analysis_date=inputs["current_date"],
            current_price=0.0,
            current_volume=0,
            technical_indicators={},
            support_resistance={},
            trend_analysis=str(technical_output)[:300] + "..." if len(str(technical_output)) > 300 else str(technical_output),
            technical_signals="Tín hiệu kỹ thuật"
        )
        
        # Parse investment decision
        decision_data = get_task_output('investment_decision', 3)
        
        # Try to parse as JSON if it's a string
        if isinstance(decision_data, str):
            try:
                import json
                decision_data = json.loads(decision_data)
            except:
                decision_data = {}
        
        if isinstance(decision_data, dict):
            investment_decision = InvestmentDecisionResponse(
                stock_ticker=decision_data.get('stock_ticker', request.symbol),
                full_name=decision_data.get('full_name', ''),
                industry=decision_data.get('industry', ''),
                today_date=decision_data.get('today_date', inputs["current_date"]),
                decision=decision_data.get('decision', 'GIỮ'),
                macro_reasoning=decision_data.get('macro_reasoning', ''),
                fund_reasoning=decision_data.get('fund_reasoning', ''),
                tech_reasoning=decision_data.get('tech_reasoning', ''),
                buy_price=decision_data.get('buy_price', 0.0),
                sell_price=decision_data.get('sell_price', 0.0),
                overall_score=7.5
            )
        else:
            investment_decision = InvestmentDecisionResponse(
                stock_ticker=request.symbol,
                full_name="Công ty cổ phần",
                industry="Chưa xác định",
                today_date=inputs["current_date"],
                decision="GIỮ",
                macro_reasoning=str(decision_data)[:200],
                fund_reasoning="Phân tích cơ bản",
                tech_reasoning="Phân tích kỹ thuật",
                buy_price=0.0,
                sell_price=0.0,
                overall_score=7.5
            )
        
        return CompleteAnalysisResponse(
            symbol=request.symbol,
            analysis_date=inputs["current_date"],
            market_analysis=market_analysis,
            fundamental_analysis=fundamental_analysis,
            technical_analysis=technical_analysis,
            investment_decision=investment_decision
        )
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Phân tích quá thời gian cho phép (1 phút)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi phân tích toàn diện: {str(e)}")

def main():
    """Main function để chạy API server"""
    print("🚀 Khởi động VN Stock Advisor API Server...")
    print("📊 API Documentation: http://localhost:8000/docs")
    print("🔍 Interactive API: http://localhost:8000/redoc")
    print("💡 Health Check: http://localhost:8000/health")
    
    uvicorn.run(
        "vn_stock_advisor.api:app",  # Import string thay vì app object
        host="0.0.0.0", 
        port=8000,
        reload=True,  # Auto-reload khi có thay đổi code
        log_level="info"
    )

if __name__ == "__main__":
    main()
