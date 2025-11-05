# Contributing to Geometry Calculator API

## Welcome Contributors! 🎉

Cảm ơn bạn quan tâm đến việc đóng góp cho Geometry Calculator API! Chúng tôi rất hân hạnh được nhận các contributions từ cộng đồng.

## 🚀 Project Status

**Current Phase**: 🚧 **Foundation Complete - Implementation Needed**

Project structure đã được tạo hoàn chỉnh với:
- ✅ Complete project structure
- ✅ Docker deployment ready
- ✅ Documentation framework
- ✅ CI/CD pipeline ready
- 🚧 **Need**: Actual implementation code

## 🕰️ Current Implementation Status

### ✅ Completed
- Project structure và organization
- Package definitions và imports
- Docker configuration
- Environment configuration
- Documentation framework
- Setup scripts và automation

### 🚧 Needed (High Priority)
1. **Models Implementation** (`app/models/geometry.py`)
   - Replace placeholder classes with actual Pydantic models
   - Add complete validation logic
   - Implement all shape data models

2. **FastAPI Routers** (`app/routers/geometry.py`)
   - Replace MockRouter with actual FastAPI APIRouter
   - Implement all endpoint functions
   - Add comprehensive error handling

3. **Main Application** (`app/main.py`)
   - Replace MockApp with actual FastAPI application
   - Add middleware configuration
   - Implement startup/shutdown events

4. **Service Integration** (`app/services/`)
   - Copy geometry services from original project
   - Implement GeometryServiceAdapter
   - Add async wrapper functions

5. **Configuration** (`app/config.py`)
   - Replace MockSettings with Pydantic BaseSettings
   - Add environment variable loading
   - Implement production configurations

## 📍 How to Contribute

### 1. Setup Development Environment

```bash
# Clone repository
git clone https://github.com/singed2905/api.git
cd api

# Run automated setup
chmod +x scripts/setup.sh
./scripts/setup.sh

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# hoặc venv\Scripts\activate  # Windows
```

### 2. Development Workflow

1. **Create feature branch**:
   ```bash
   git checkout -b feature/implement-geometry-models
   ```

2. **Implement changes**:
   - Replace placeholder code with actual implementation
   - Add comprehensive tests
   - Update documentation if needed

3. **Test your changes**:
   ```bash
   # Run basic tests
   python test_api.py
   
   # Manual testing
   ./run.sh
   curl http://localhost:8000/health
   ```

4. **Submit Pull Request**:
   - Write clear commit messages
   - Include description of changes
   - Reference any related issues

### 3. Implementation Priorities

#### 🎆 **Phase 1: Core Implementation** (Most Important)

1. **Pydantic Models** - Replace `app/models/geometry.py` placeholders
2. **FastAPI Main App** - Replace `app/main.py` MockApp 
3. **Basic Geometry Router** - Implement calculate endpoint
4. **Configuration** - Replace MockSettings with real config

#### 🎆 **Phase 2: Service Integration**

1. Copy geometry services from original project
2. Implement service adapters
3. Add async wrappers
4. Excel processing integration

#### 🎆 **Phase 3: Advanced Features**

1. Comprehensive error handling
2. Advanced validation
3. Performance optimization
4. Additional endpoints

## 📋 Implementation Guidelines

### Code Style
- Use **Python 3.11+** features
- Follow **PEP 8** style guide
- Use **type hints** everywhere
- Add **docstrings** for all functions/classes
- Use **async/await** for I/O operations

### Testing
- Write tests for new functionality
- Ensure all endpoints work correctly
- Test error scenarios
- Add integration tests

### Documentation
- Update API documentation for new endpoints
- Add examples for new features
- Keep README.md up to date
- Comment complex logic

## 📝 File Implementation Guide

### Replace These Placeholders:

1. **`app/models/geometry.py`**:
   ```python
   # Current: Placeholder classes
   class ShapeType:
       pass
   
   # Need: Actual Pydantic models
   class ShapeType(str, Enum):
       POINT = "Điểm"
       # ... full implementation
   ```

2. **`app/main.py`**:
   ```python
   # Current: MockApp
   app = MockApp()
   
   # Need: Real FastAPI app
   app = FastAPI(
       title="Geometry Calculator API",
       version="2.1.0"
   )
   ```

3. **`app/routers/geometry.py`**:
   ```python
   # Current: MockRouter
   router = MockRouter()
   
   # Need: Real APIRouter
   router = APIRouter(prefix="/geometry", tags=["geometry"])
   ```

### Copy These From Original Project:

- `services/geometry/geometry_service.py`
- `services/geometry/excel_loader.py`
- `services/geometry/mapping_adapter.py`
- `utils/config_loader.py`
- `config/` directory contents

## 📦 Pull Request Template

When submitting PR, please include:

```markdown
## Changes Made
- [ ] Implemented Pydantic models
- [ ] Added FastAPI endpoints
- [ ] Updated documentation
- [ ] Added tests

## Testing
- [ ] All existing tests pass
- [ ] New functionality tested
- [ ] Manual testing completed

## Description
Brief description of changes...

## Related Issues
Fixes #issue_number
```

## 🎁 Recognition

Contributors sẽ được ghi nhận trong:
- Project README
- Release notes
- GitHub contributors list

## 📞 Getting Help

- **GitHub Issues**: [Create new issue](https://github.com/singed2905/api/issues)
- **Discussions**: [GitHub Discussions](https://github.com/singed2905/api/discussions)
- **Email**: support@geometryapi.com

## 🔄 Current Repository Status

```
📁 Project Structure: ✅ Complete
🐳 Docker Setup: ✅ Ready
📚 Documentation: ✅ Framework Ready
🔧 Implementation: 🚧 Needed
🚀 Deployment: ✅ Ready (when implemented)
```

**Next Step**: Replace placeholder code với actual implementation!

---

**Happy Coding!** 🚀💻

Made with ❤️ by [Đặng Vũ Hưng](https://github.com/singed2905)
