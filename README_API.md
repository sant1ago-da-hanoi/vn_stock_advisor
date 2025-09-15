# VN Stock Advisor API

## 🚀 Khởi động API Server

### Cài đặt dependencies
```bash
# Cài đặt FastAPI và uvicorn
uv add fastapi uvicorn

# Hoặc nếu đã cài đặt rồi
crewai install
```

### Chạy API Server
```bash
# Cách 1: Sử dụng script command từ pyproject.toml
api_server

# Cách 2: Sử dụng uvicorn trực tiếp
uvicorn src.vn_stock_advisor.api:app --host 0.0.0.0 --port 8000 --reload

# Cách 3: Chạy trực tiếp từ module
python -m src.vn_stock_advisor.api

# Cách 4: Sử dụng uv run
uv run api_server
```

## 📊 API Endpoints

### 1. **GET** `/` - Thông tin API
```json
{
  "message": "VN Stock Advisor API",
  "version": "0.4.1",
  "description": "API cho hệ thống phân tích cổ phiếu Việt Nam"
}
```

### 2. **GET** `/health` - Health Check
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15"
}
```

### 3. **POST** `/analyze/market` - Phân tích tin tức vĩ mô
```bash
curl -X POST "http://localhost:8000/analyze/market" \
     -H "Content-Type: application/json" \
     -d '{"symbol": "HPG"}'
```

### 4. **POST** `/analyze/fundamental` - Phân tích cơ bản
```bash
curl -X POST "http://localhost:8000/analyze/fundamental" \
     -H "Content-Type: application/json" \
     -d '{"symbol": "HPG"}'
```

### 5. **POST** `/analyze/technical` - Phân tích kỹ thuật
```bash
curl -X POST "http://localhost:8000/analyze/technical" \
     -H "Content-Type: application/json" \
     -d '{"symbol": "HPG"}'
```

### 6. **POST** `/analyze/decision` - Quyết định đầu tư
```bash
curl -X POST "http://localhost:8000/analyze/decision" \
     -H "Content-Type: application/json" \
     -d '{"symbol": "HPG"}'
```

### 7. **POST** `/analyze/complete` - Phân tích toàn diện
```bash
curl -X POST "http://localhost:8000/analyze/complete" \
     -H "Content-Type: application/json" \
     -d '{"symbol": "HPG"}'
```

## 📋 Request Format

```json
{
  "symbol": "HPG",
  "current_date": "2024-01-15"  // Optional, mặc định là hôm nay
}
```

## 📋 Response Examples

### Market Analysis Response
```json
{
  "symbol": "HPG",
  "analysis_date": "2024-01-15",
  "news_summary": "Tóm tắt tin tức vĩ mô...",
  "market_impact": "Phân tích tác động thị trường"
}
```

### Investment Decision Response
```json
{
  "stock_ticker": "HPG",
  "full_name": "Tập đoàn Hòa Phát",
  "industry": "Kim loại và khai khoáng",
  "today_date": "2024-01-15",
  "decision": "MUA",
  "macro_reasoning": "Phân tích vĩ mô...",
  "fund_reasoning": "Phân tích cơ bản...",
  "tech_reasoning": "Phân tích kỹ thuật...",
  "buy_price": 25000.0,
  "sell_price": 30000.0,
  "overall_score": 7.8
}
```

## 🔧 Cấu hình

### Environment Variables
Tạo file `.env` với các biến môi trường:
```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini/gemini-2.0-flash-001
GEMINI_REASONING_MODEL=gemini/gemini-2.0-flash-001
SERPER_API_KEY=your_serper_api_key
FIRECRAWL_API_KEY=your_firecrawl_api_key
```

## 📚 API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🛠️ Development

### Hot Reload
API server hỗ trợ hot reload khi có thay đổi code:
```bash
uvicorn src.vn_stock_advisor.api:app --reload
```

### CORS
API đã được cấu hình CORS để hỗ trợ frontend từ các domain khác nhau.

### Error Handling
API trả về HTTP status codes chuẩn:
- `200`: Thành công
- `422`: Validation error
- `500`: Internal server error

## 🔒 Security Notes

- Trong production, nên cấu hình CORS origins cụ thể thay vì `"*"`
- Sử dụng authentication/authorization nếu cần
- Rate limiting để tránh abuse API
- Logging và monitoring cho production
