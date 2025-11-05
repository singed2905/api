# 🚀 Geometry Calculator API - Quick Start Guide

Hướng dẫn nhanh để chạy API trong **5 phút**!

## 🚨 Lưu ý quan trọng về testing:

**❌ KHÔNG chạy:** `pytest test_api.py` (sẽ bị conflict)  
**✅ CHẠY:** `python test_api_manual.py` hoặc `python test_api.py`

---

## 📚 Bước 1: Clone và Setup

```bash
# Clone repository
git clone https://github.com/singed2905/api.git
cd api

# Cấp quyền thực thi
chmod +x run.sh setup.sh

# Setup tự động (tạo venv, install dependencies)
./setup.sh
```

## 🚀 Bước 2: Chạy API Server

```bash
# Start API server
./run.sh
```

**API sẽ chạy tại:**
- 🌍 **Main API**: http://localhost:8000
- 📚 **Interactive Docs**: http://localhost:8000/docs
- ❤️ **Health Check**: http://localhost:8000/health

## 🧪 Bước 3: Test API

**Option 1: Manual Test Script (Recommended)**
```bash
# Mở terminal mới (giữ API chạy)
python test_api_manual.py
```

**Option 2: Quick Manual Test**
```bash
# Test health
curl http://localhost:8000/health

# Test shapes
curl http://localhost:8000/api/v1/geometry/shapes

# Test calculation
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

## 📊 Expected Test Results:

**✅ Nếu thành công, bạn sẽ thấy:**
```
✅ Root endpoint - OK
✅ Health endpoint - OK  
✅ Shapes endpoint - OK
✅ Examples endpoint - OK
✅ Point Distance 3D calculation - OK
✅ Circle Area 2D calculation - OK

🎉 ALL TESTS PASSED!
Geometry Calculator API is working correctly!
```

**❌ Nếu có lỗi:**
- **Connection Error**: API chưa chạy → Chạy `./run.sh`
- **Import Error**: Dependencies chưa đủ → Chạy `pip install -r requirements.txt`
- **Port Error**: Port 8000 đã dùng → Tắt các ứng dụng khác

## 📚 Bước 4: Sử dụng API

### Ví dụ requests:

**1. Tính khoảng cách 2 điểm 3D:**
```bash
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

**2. Tính diện tích đường tròn:**
```bash
curl -X POST "http://localhost:8000/api/v1/geometry/calculate" \
-H "Content-Type: application/json" \
-d '{
  "operation": "Diện tích",
  "shape_a": "Đường tròn",
  "dimension_a": "2",
  "calculator_version": "fx799",
  "circle_a": {
    "center": "0,0",
    "radius": "5"
  }
}'
```

**3. Lấy danh sách shapes và operations:**
```bash
curl http://localhost:8000/api/v1/geometry/shapes
```

## 🔧 Available Endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/docs` | GET | Interactive docs |
| `/api/v1/geometry/calculate` | POST | Main calculation |
| `/api/v1/geometry/shapes` | GET | Available shapes |
| `/api/v1/geometry/examples` | GET | Usage examples |
| `/api/v1/geometry/validate` | POST | Input validation |
| `/api/v1/geometry/config` | GET | Debug config |

## 📊 Current API Capabilities:

### ✅ **Working Features:**
- ✅ Health monitoring với system stats
- ✅ JSON configuration loading
- ✅ Comprehensive input validation
- ✅ Operation compatibility checking
- ✅ Mock keylog generation (basic patterns)
- ✅ Mock calculations (distance, area)
- ✅ Error handling với detailed messages
- ✅ OpenAPI documentation
- ✅ CORS support cho web integration

### 🔧 **Ready to Implement:**
- Real geometry calculations
- Actual keylog encoding
- Excel processing endpoints
- Background task processing
- Advanced caching

## 🐛 Troubleshooting:

**Lỗi thường gặp:**

1. **`ModuleNotFoundError`**:
   ```bash
   pip install -r requirements.txt
   ```

2. **`Port already in use`**:
   ```bash
   # Tìm và tắt process dùng port 8000
   lsof -ti:8000 | xargs kill -9  # Linux/Mac
   netstat -ano | findstr :8000   # Windows
   ```

3. **`Permission denied` for scripts**:
   ```bash
   chmod +x run.sh setup.sh
   ```

4. **Config files not found**:
   - Kiểm tra thư mục `config/` tồn tại
   - Các file JSON đã được push trong các commits trước

## 🌍 Production Deployment:

**Docker:**
```bash
# Build và chạy
docker-compose up --build

# API sẽ available tại http://localhost:8000
```

**Manual Production:**
```bash
# Install production server
pip install gunicorn

# Chạy production
gunicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🎆 Kết quả mong đợi:

Sau khi hoàn thành các bước trên, bản sẽ có:

✅ **Working Geometry Calculator API**  
✅ **OpenAPI Documentation**  
✅ **JSON Configuration System**  
✅ **Comprehensive Validation**  
✅ **Health Monitoring**  
✅ **Docker Deployment Ready**  

**API sẵn sàng cho web integration và further development!** 🚀🎉

---

**Made with ❤️ by [Đặng Vũ Hưng](https://github.com/singed2905)**
