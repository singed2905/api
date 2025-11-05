# Geometry Calculator API

🔧 **API chuyển đổi từ Desktop Geometry Mode thành Web Service**

API này cung cấp đầy đủ chức năng của **Geometry Mode** từ desktop application, được thiết kế để tích hợp vào các ứng dụng web hiện đại.

## ✨ Tính năng chính

### 🧮 Tính toán hình học
- **Khoảng cách**: Giữa điểm-điểm, điểm-đường thẳng, điểm-mặt phẳng
- **Tương giao**: Đường thẳng-đường thẳng, đường thẳng-mặt phẳng  
- **Diện tích**: Đường tròn, hình phẳng
- **Thể tích**: Mặt cầu, khối 3D
- **Phương trình đường thẳng**: Qua 2 điểm, vuông góc mặt phẳng

### 📊 Xử lý Excel Batch
- Upload và xử lý file Excel (hỗ trợ đến 250k+ rows)
- Anti-crash system với memory monitoring
- Tạo template Excel theo cấu hình hình học
- Download kết quả đã mã hóa
- Background processing cho file lớn

### 🎯 Mã hóa Keylog Casio
- Sinh keylog cho máy tính Casio (fx799, fx991, fx570, fx880, fx801)
- Encoding tối ưu theo từng phiên bản máy
- Format tương thích trực tiếp với máy tính

### 🚀 Performance & Scalability
- Async processing với FastAPI
- Background tasks cho heavy operations
- Memory monitoring và optimization
- REST API chuẩn với OpenAPI documentation
- Docker support cho easy deployment

## 🛠️ Tech Stack

- **Framework**: FastAPI + Uvicorn
- **Data Processing**: Pandas + NumPy + OpenPyXL
- **Validation**: Pydantic
- **System Monitoring**: psutil
- **Deployment**: Docker + Docker Compose

## 📖 Quick Start

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/singed2905/api.git
cd api

# 2. Setup environment
chmod +x setup.sh
./setup.sh

# 3. Activate virtual environment
source venv/bin/activate  # Linux/Mac
# hoặc venv\Scripts\activate  # Windows

# 4. Run API
./run.sh
# hoặc uvicorn app.main:app --reload
```

### Docker Deployment

```bash
# Build và chạy
docker-compose up --build

# API sẽ available tại http://localhost:8000
```

## 📚 API Documentation

- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json
- **Health Check**: http://localhost:8000/health

## 🔗 Main Endpoints

| Endpoint | Method | Description |
|----------|--------|--------------|
| `/api/v1/geometry/calculate` | POST | Tính toán hình học |
| `/api/v1/geometry/shapes` | GET | Danh sách hình học |
| `/api/v1/geometry/examples` | GET | Ví dụ requests |
| `/api/v1/excel/process` | POST | Xử lý Excel batch |
| `/api/v1/excel/template` | POST | Tạo Excel template |
| `/health` | GET | Health check |

## 📋 Project Structure

```
api/
├── app/                    # Main application
│   ├── models/            # Pydantic models
│   ├── routers/           # API endpoints
│   ├── services/          # Business logic
│   └── utils/             # Utilities
├── config/                # Configuration files
├── uploads/               # Temporary uploads
├── outputs/               # Generated files
├── tests/                 # Test files
├── docs/                  # Documentation
├── scripts/               # Setup/deployment scripts
├── docker-compose.yml     # Docker services
├── Dockerfile            # Container definition
└── requirements.txt      # Python dependencies
```

## 🧪 Testing

```bash
# Run tests
python test_api.py

# Test specific endpoint
curl -X POST "http://localhost:8000/api/v1/geometry/calculate" \
-H "Content-Type: application/json" \
-d '{
  "operation": "Khoảng cách",
  "shape_a": "Điểm", 
  "shape_b": "Điểm",
  "dimension_a": "3",
  "dimension_b": "3",
  "calculator_version": "fx799",
  "point_a": {"coordinates": "1,2,3"},
  "point_b": {"coordinates": "4,5,6"}
}'
```

## 🚀 Deployment

### Production với Docker

```bash
# Build production image
docker build -t geometry-api:latest .

# Run production container
docker run -d \
  --name geometry-api \
  -p 8000:8000 \
  -v ./uploads:/app/uploads \
  -v ./outputs:/app/outputs \
  geometry-api:latest
```

### Cloud Deployment

- **Heroku**: Sử dụng `Procfile`
- **Railway**: Auto-deploy từ GitHub
- **Vercel**: Serverless functions
- **AWS/GCP**: Docker containers

## 📊 Performance

- **Response time**: < 100ms cho tính toán đơn giản
- **File processing**: 1000+ rows/second
- **Memory usage**: < 100MB cho operations thông thường
- **Concurrent requests**: Hỗ trợ 100+ requests/second

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Tạo Pull Request

## 📄 License

MIT License - xem [LICENSE](LICENSE) file để biết thêm chi tiết.

## 🔗 Related Projects

- [singed2905/clone](https://github.com/singed2905/clone) - Original desktop application
- [Geometry Mode Documentation](docs/) - Detailed technical documentation

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/singed2905/api/issues)
- **Discussions**: [GitHub Discussions](https://github.com/singed2905/api/discussions)
- **Email**: support@geometryapi.com

---

**Made with ❤️ by [Đặng Vũ Hưng](https://github.com/singed2905)**