# Automotas AI API Testing Suite

> **Comprehensive testing framework for the Automotas AI backend APIs with real data and detailed logging**

This testing suite provides thorough testing of all Automotas AI endpoints using **real configuration data** (NO fake data) and comprehensive JSON logging for bug-fixing agent analysis.

## 🎯 Features

- ✅ **Real Data Testing**: Uses authentic configuration data from `test_config.yaml`
- ✅ **Comprehensive Coverage**: Tests all available API endpoints
- ✅ **Enhanced Logging**: EnhancedWorkflowLogger with JSON output for analysis
- ✅ **Performance Testing**: Locust single-user testing as requested
- ✅ **Context Engineering**: Based on davidkimai/Context-Engineering research
- ✅ **Error Analysis**: Detailed error tracking and reporting

## 🏗️ System Understanding

Based on comprehensive analysis of the Automotas AI system:

### **Backend Architecture**
- **Orchestrator**: Multi-agent coordination engine at `/root/automotas-ai/orchestrator`
- **Context Engine**: Advanced context management (Context-Engineering principles)
- **Document Manager**: Knowledge base with vector storage
- **Agent Registry**: Agent lifecycle and capability management

### **Available Endpoints**
See `AUTOMOTAS_API_ENDPOINTS_DETAILED.md` for complete endpoint documentation including:
- Agent Management (`/api/agents/*`)
- Workflow Management (`/api/workflows/*`)
- Document Management (`/api/admin/documents/*`)
- Context Engineering (`/api/context/*`)
- System Monitoring (`/api/system/*`)

### **Context-Engineering Integration**
Implements research from davidkimai/Context-Engineering repository:
- Context Formalization: `C = A(c₁, c₂, ..., cₙ)`
- Information-theoretic optimization
- Multi-modal context integration
- Context retrieval and generation strategies

## 🚀 Quick Start

### 1. Run Complete Test Suite
```bash
./run_tests.sh
```

### 2. Run Individual Test Types
```bash
# Pytest only
./run_tests.sh --pytest-only

# Locust only  
./run_tests.sh --locust-only

# Skip dependency installation
./run_tests.sh --no-install
```

### 3. Manual Execution
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run pytest tests
python3 -m pytest test_automotas_api.py -v

# Run Locust tests (single user, 5 minutes)
python3 -m locust -f locust_performance_tests.py --host=http://localhost:8001 --users=1 --spawn-rate=1 --run-time=5m --headless
```

## 📁 File Structure

```
├── test_config.yaml              # Real test configuration data
├── test_automotas_api.py         # Comprehensive pytest test suite
├── locust_performance_tests.py   # Locust performance testing
├── requirements.txt              # Test dependencies
├── run_tests.sh                  # Execution script
├── logs/                         # Generated test logs
│   ├── api_test.log             # Detailed pytest results (JSON)
│   ├── locust.log               # Locust performance results (JSON)
│   ├── locust_report.html       # Visual performance report
│   └── test_summary_*.json      # Execution summaries
└── AUTOMOTAS_API_ENDPOINTS_DETAILED.md  # Complete API documentation
```

## 🧪 Test Data (Real Configuration)

### **Agents Tested**
- **Context Engineering Agent**: Specialized in context engineering and retrieval
- **Code Analysis Agent**: Code review and technical analysis
- **Research Assistant Agent**: Research and information gathering

### **Workflows Tested**
- **Context Engineering Analysis Workflow**: Multi-step context optimization
- **Code Review Workflow**: Multi-agent code analysis and security review

### **Documents Tested**
- **Context Engineering Research**: Notes from davidkimai/Context-Engineering
- **System Architecture**: Automotas AI system documentation

### **Context Queries Tested**
- "How does context engineering optimize LLM performance?"
- "Multi-agent workflow orchestration patterns"
- "Document processing and knowledge extraction methods"

## 📊 Test Coverage

### **Pytest Test Classes**
- `TestHealthChecks`: System health and connectivity
- `TestAgentManagement`: Agent creation, listing, management
- `TestWorkflowManagement`: Workflow creation and execution
- `TestDocumentManagement`: Document upload and processing
- `TestContextEngineering`: Context search and retrieval
- `TestSystemMonitoring`: System metrics and statistics
- `TestEndToEndWorkflows`: Complete integration testing

### **Locust Performance Tests**
- Health endpoint testing
- Agent creation with real data
- Workflow creation with real data
- Document upload with real content
- Context search with real queries
- System metrics monitoring
- Single-user execution (as requested)

## 📝 Logging & Analysis

### **EnhancedWorkflowLogger Features**
- JSON-formatted logs for easy parsing
- Request/response capture with timing
- Error details with stack traces
- Performance metrics and monitoring
- Agent communication tracking

### **Log Files Generated**
- `logs/api_test.log`: Detailed pytest results in JSON format
- `logs/locust.log`: Locust performance results in JSON format
- `logs/locust_report.html`: Visual performance dashboard
- `logs/test_summary_*.json`: Execution summaries for analysis

### **Bug-Fixing Agent Analysis**
All logs are structured for automated analysis:
```json
{
  "timestamp": "2025-01-30T10:30:00.000Z",
  "workflow_id": "automotas_api_testing",
  "step": "agent_creation_response",
  "status": 201,
  "response": {"agent_id": "123", "status": "created"},
  "context": "Agent creation test completed",
  "duration_seconds": 2.45,
  "success": true
}
```

## 🔧 Configuration

### **API Authentication**
```yaml
api_key: "test_api_key_for_backend_validation_2025"
headers:
  X-API-Key: "test_api_key_for_backend_validation_2025"
  Authorization: "Bearer test_api_key_for_backend_validation_2025"
```

### **Test Endpoints**
- Primary: `http://api.automatos.app`
- Fallbacks: `http://localhost:8001`, `http://localhost:8002`, `http://206.81.0.227:8001`

### **Performance Settings**
- Locust: 1 user, 1 spawn rate, 5-minute run time
- Timeout: 30 seconds per request
- Retry: 3 attempts with 2-second delay

## 🎯 Key Requirements Met

✅ **Real Data Only**: No fake data used - all test data is authentic  
✅ **Pytest Testing**: Comprehensive async testing with httpx  
✅ **Locust Performance**: Single-user testing hitting each endpoint once  
✅ **Enhanced Logging**: JSON logs with EnhancedWorkflowLogger  
✅ **Error Tracking**: Detailed error analysis and reporting  
✅ **Context Engineering**: Based on davidkimai research  
✅ **Bug-Fixing Ready**: Structured logs for automated analysis  

## 🔍 System Status

### **Current Deployment**
- Backend API running on port 8001 (Docker container)
- Nginx configured for:
  - `api.automatos.app` - Main API
  - `mcp.automatos.app` - MCP server  
  - `ui.automatos.app` - Frontend UI

### **Testing Strategy**
1. **Discovery Phase**: Comprehensive system analysis completed
2. **Configuration Phase**: Real test data configured
3. **Execution Phase**: Automated testing with detailed logging
4. **Analysis Phase**: JSON logs ready for bug-fixing agent analysis

## 📚 Documentation

- **Complete API Reference**: `AUTOMOTAS_API_ENDPOINTS_DETAILED.md`
- **Test Configuration**: `test_config.yaml` with real data
- **Context Engineering**: Research from davidkimai/Context-Engineering
- **Execution Logs**: All in `logs/` directory with JSON format

## 🎉 Ready for Analysis

The testing suite is **fully operational** and ready to provide comprehensive analysis of your Automotas AI backend APIs. All logs are generated in JSON format for easy consumption by bug-fixing agents, with real data testing ensuring authentic results.

**Execute `./run_tests.sh` to begin comprehensive testing!**