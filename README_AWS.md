# VN Stock Advisor với AWS Bedrock

## 🚀 Cấu hình AWS Bedrock

### 1. Cài đặt dependencies

```bash
# Cài đặt AWS dependencies
uv add boto3 botocore litellm

# Hoặc cài đặt tất cả
crewai install
```

### 2. Cấu hình AWS Credentials

#### Cách 1: Environment Variables
Tạo file `.env` với nội dung:

```env
# AWS Credentials
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION=us-east-1

# Model Selection
USE_AWS_MODELS=true
USE_GEMINI_MODELS=false

# AWS Bedrock Models
AWS_CLAUDE_MODEL=anthropic.claude-3-sonnet-20240229-v1:0
AWS_CLAUDE_REASONING_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0

# Other API Keys (still needed)
SERPER_API_KEY=your_serper_api_key
FIRECRAWL_API_KEY=your_firecrawl_api_key
```

#### Cách 2: AWS CLI Configuration
```bash
# Cài đặt AWS CLI
pip install awscli

# Cấu hình credentials
aws configure
# Nhập Access Key ID, Secret Access Key, Region

# Hoặc sử dụng AWS SSO
aws sso login --profile your-profile
```

#### Cách 3: IAM Role (cho EC2/ECS)
Nếu chạy trên AWS infrastructure, sử dụng IAM role thay vì credentials.

### 3. Cấu hình AWS Bedrock

#### Enable Bedrock Models
1. Đăng nhập AWS Console
2. Vào AWS Bedrock service
3. Enable các models bạn muốn sử dụng:
   - **Claude 3 Sonnet**: `anthropic.claude-3-sonnet-20240229-v1:0`
   - **Claude 3.5 Sonnet**: `anthropic.claude-3-5-sonnet-20241022-v2:0`
   - **Titan Text**: `amazon.titan-text-express-v1`
   - **Titan Embeddings**: `amazon.titan-embed-text-v1`

#### IAM Permissions
Đảm bảo user/role có permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:*::foundation-model/anthropic.claude-*",
                "arn:aws:bedrock:*::foundation-model/amazon.titan-*"
            ]
        }
    ]
}
```

## 📊 Available AWS Models

### Claude Models
- **claude-3-sonnet**: Claude 3 Sonnet (balanced performance/cost)
- **claude-3-haiku**: Claude 3 Haiku (fastest, cheapest)
- **claude-3-opus**: Claude 3 Opus (most capable)
- **claude-3-5-sonnet**: Claude 3.5 Sonnet (latest, best reasoning)

### Titan Models
- **titan-text-express**: Amazon Titan Text Express
- **titan-text-lite**: Amazon Titan Text Lite
- **titan-embed-text**: Amazon Titan Embeddings

### Jurassic Models
- **j2-ultra**: AI21 Jurassic-2 Ultra
- **j2-mid**: AI21 Jurassic-2 Mid

## 🔧 Sử dụng

### Chạy với AWS Bedrock
```bash
# Set environment variables
export USE_AWS_MODELS=true
export USE_GEMINI_MODELS=false

# Chạy API server
uv run api_server

# Hoặc chạy crew trực tiếp
crewai run
```

### Test API với AWS
```bash
curl -X POST "http://localhost:8000/analyze/complete" \
     -H "Content-Type: application/json" \
     -d '{"symbol": "HPG"}'
```

### Switch giữa AWS và Gemini
```bash
# Sử dụng AWS Bedrock
export USE_AWS_MODELS=true
export USE_GEMINI_MODELS=false

# Sử dụng Google Gemini
export USE_AWS_MODELS=false
export USE_GEMINI_MODELS=true
```

## 💰 Cost Comparison

### AWS Bedrock Pricing (us-east-1)
- **Claude 3 Sonnet**: $3.00/1M input tokens, $15.00/1M output tokens
- **Claude 3.5 Sonnet**: $3.00/1M input tokens, $15.00/1M output tokens
- **Titan Text Express**: $0.0008/1K input tokens, $0.0016/1K output tokens

### Google Gemini Pricing
- **Gemini 2.0 Flash**: $0.075/1M input tokens, $0.30/1M output tokens

## 🛠️ Troubleshooting

### Lỗi thường gặp

1. **Access Denied**
   ```
   Error: User is not authorized to perform: bedrock:InvokeModel
   ```
   **Giải pháp**: Kiểm tra IAM permissions và enable models trong Bedrock console

2. **Model not found**
   ```
   Error: Model anthropic.claude-3-sonnet-20240229-v1:0 not found
   ```
   **Giải pháp**: Enable model trong AWS Bedrock console

3. **Region not supported**
   ```
   Error: Bedrock is not available in region ap-southeast-1
   ```
   **Giải pháp**: Sử dụng region được hỗ trợ như `us-east-1`, `us-west-2`

4. **Fallback to Gemini**
   ```
   ❌ AWS configuration failed: ...
   🔄 Falling back to Google Gemini...
   ```
   **Giải pháp**: Kiểm tra AWS credentials và permissions

### Debug AWS Configuration
```python
from vn_stock_advisor.aws_config import AWSConfig

# Test configuration
try:
    config = AWSConfig()
    print("✅ AWS configuration successful")
    print(f"Region: {config.aws_region}")
    print(f"Claude model: {config.claude_model}")
except Exception as e:
    print(f"❌ AWS configuration failed: {e}")
```

## 🔒 Security Best Practices

1. **Không commit credentials**: Thêm `.env` vào `.gitignore`
2. **Sử dụng IAM roles**: Thay vì hardcode credentials
3. **Least privilege**: Chỉ cấp permissions cần thiết
4. **Rotate keys**: Thay đổi access keys định kỳ
5. **Monitor usage**: Theo dõi cost và usage trong AWS CloudWatch

## 📈 Performance Tips

1. **Chọn model phù hợp**:
   - Haiku: Nhanh nhất, rẻ nhất
   - Sonnet: Cân bằng performance/cost
   - Opus: Mạnh nhất, đắt nhất

2. **Optimize prompts**: Viết prompt ngắn gọn, rõ ràng
3. **Batch requests**: Gộp nhiều requests khi có thể
4. **Cache results**: Cache kết quả phân tích để tránh duplicate calls
