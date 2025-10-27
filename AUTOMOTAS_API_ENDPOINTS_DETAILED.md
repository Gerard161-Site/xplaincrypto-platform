# Automotas AI API Endpoints - Comprehensive Documentation

> **Based on Deep System Analysis and Context-Engineering Research**

This document provides a complete list of all available endpoints in the Automotas AI system, based on thorough analysis of the codebase, including the Context-Engineering research from the davidkimai repository.

## System Overview

The Automotas AI system is built on **Context Engineering** principles, implementing "the delicate art and science of filling the context window with just the right information for the next step" (Andrej Karpathy). The backend implements advanced multi-agent orchestration with context-aware processing.

### Architecture Components
- **Orchestrator**: Multi-agent coordination engine
- **Context Engine**: Advanced context management and retrieval
- **Document Manager**: Knowledge base with vector storage
- **Agent Registry**: Agent lifecycle and capability management
- **Workflow Engine**: Multi-step process orchestration

---

## Core System Endpoints

### Health & Status

#### `GET /health`
- **Description**: System health check and status
- **Response**: JSON with status, timestamp, version
- **Expected Status**: 200
- **Authentication**: Not required

#### `GET /`
- **Description**: Root endpoint with API metadata
- **Response**: API information and available endpoints
- **Expected Status**: 200
- **Authentication**: Not required

---

## Agent Management Endpoints

The agent management system handles creation, configuration, and lifecycle of AI agents with different specializations.

### `POST /api/agents`
- **Description**: Create a new agent with specific capabilities
- **Request Body**:
  ```json
  {
    "name": "Context Engineering Agent",
    "description": "Agent specialized in context engineering and retrieval",
    "agent_type": "specialist",
    "configuration": {
      "model": "gpt-4",
      "temperature": 0.7,
      "max_tokens": 2000,
      "specialization": "context_engineering",
      "capabilities": ["document_analysis", "context_retrieval", "knowledge_synthesis"]
    }
  }
  ```
- **Expected Status**: 201
- **Response**: Agent ID and creation details

### `GET /api/agents`
- **Description**: List all available agents
- **Query Parameters**: 
  - `agent_type`: Filter by agent type
  - `status`: Filter by agent status
- **Expected Status**: 200
- **Response**: Array of agent objects

### `GET /api/agents/{agent_id}`
- **Description**: Get specific agent details
- **Path Parameters**: `agent_id` - Agent identifier
- **Expected Status**: 200
- **Response**: Detailed agent information

### `PUT /api/agents/{agent_id}`
- **Description**: Update agent configuration
- **Path Parameters**: `agent_id` - Agent identifier
- **Request Body**: Updated agent configuration
- **Expected Status**: 200

### `DELETE /api/agents/{agent_id}`
- **Description**: Remove agent from system
- **Path Parameters**: `agent_id` - Agent identifier
- **Expected Status**: 204

---

## Workflow Management Endpoints

Advanced workflow orchestration with multi-agent coordination and context-aware processing.

### `POST /api/workflows`
- **Description**: Create a new workflow definition
- **Request Body**:
  ```json
  {
    "name": "Context Engineering Analysis Workflow",
    "description": "Comprehensive context engineering analysis and optimization workflow",
    "workflow_definition": {
      "steps": [
        {
          "id": "context_extraction",
          "name": "Extract Context Information",
          "agent_type": "context_engineering",
          "dependencies": []
        },
        {
          "id": "context_analysis",
          "name": "Analyze Context Quality",
          "agent_type": "specialist",
          "dependencies": ["context_extraction"]
        }
      ]
    }
  }
  ```
- **Expected Status**: 201
- **Response**: Workflow ID and execution details

### `GET /api/workflows`
- **Description**: List all workflows
- **Query Parameters**:
  - `status`: Filter by workflow status
  - `created_by`: Filter by creator
- **Expected Status**: 200
- **Response**: Array of workflow objects

### `GET /api/workflows/{workflow_id}`
- **Description**: Get workflow details and status
- **Path Parameters**: `workflow_id` - Workflow identifier
- **Expected Status**: 200
- **Response**: Detailed workflow information

### `POST /api/workflows/{workflow_id}/execute`
- **Description**: Execute a workflow
- **Path Parameters**: `workflow_id` - Workflow identifier
- **Request Body**: Execution parameters and context
- **Expected Status**: 202
- **Response**: Execution ID and initial status

### `GET /api/workflows/{workflow_id}/logs`
- **Description**: Get workflow execution logs
- **Path Parameters**: `workflow_id` - Workflow identifier
- **Expected Status**: 200
- **Response**: Detailed execution logs

### `DELETE /api/workflows/{workflow_id}`
- **Description**: Delete workflow
- **Path Parameters**: `workflow_id` - Workflow identifier
- **Expected Status**: 204

---

## Document Management Endpoints

Knowledge base management with vector storage and context indexing.

### `POST /api/admin/documents/upload`
- **Description**: Upload documents for processing and indexing
- **Content-Type**: `multipart/form-data`
- **Form Data**:
  - `file`: Document file (PDF, DOCX, MD, TXT, PY, JSON)
  - `tags`: Comma-separated tags
  - `description`: Document description
  - `created_by`: Creator identifier
- **Expected Status**: 201
- **Response**: Document ID and processing status

### `GET /api/admin/documents`
- **Description**: List all documents in knowledge base
- **Query Parameters**:
  - `status`: Filter by processing status
  - `file_type`: Filter by file type
  - `page`: Page number for pagination
  - `per_page`: Items per page
- **Expected Status**: 200
- **Response**: Paginated document list

### `GET /api/admin/documents/{document_id}`
- **Description**: Get document details and metadata
- **Path Parameters**: `document_id` - Document identifier
- **Expected Status**: 200
- **Response**: Document information and processing status

### `DELETE /api/admin/documents/{document_id}`
- **Description**: Remove document and associated chunks
- **Path Parameters**: `document_id` - Document identifier
- **Expected Status**: 204

---

## Context Engineering Endpoints

Advanced context retrieval and management based on Context-Engineering research.

### `POST /api/context/search`
- **Description**: Search for relevant context using semantic similarity
- **Request Body**:
  ```json
  {
    "query": "How does context engineering optimize LLM performance?",
    "limit": 10
  }
  ```
- **Expected Status**: 200
- **Response**: 
  ```json
  {
    "results": [
      {
        "chunk_id": 123,
        "document_id": 456,
        "filename": "context_engineering_research.md",
        "content": "Context engineering optimizes...",
        "similarity": 0.89,
        "metadata": {"section": "optimization"}
      }
    ],
    "query": "How does context engineering optimize LLM performance?",
    "total_results": 10
  }
  ```

### `GET /api/context/retrieve/{document_id}`
- **Description**: Retrieve context from specific document
- **Path Parameters**: `document_id` - Document identifier
- **Query Parameters**:
  - `query`: Optional query for filtering chunks
  - `limit`: Maximum chunks to return
- **Expected Status**: 200
- **Response**: Document context and chunks

---

## System Monitoring Endpoints

Real-time system metrics and performance monitoring.

### `GET /api/system/metrics`
- **Description**: Get real-time system performance metrics
- **Authentication**: Required (API key)
- **Expected Status**: 200
- **Response**:
  ```json
  {
    "cpu": {
      "usage_percent": 45.2,
      "cores": 8
    },
    "memory": {
      "usage_percent": 67.8,
      "used_gb": 5.4,
      "total_gb": 8.0
    },
    "disk": {
      "usage_percent": 23.1,
      "used_gb": 115.2,
      "total_gb": 500.0
    },
    "network": {
      "packets_sent": 1250,
      "packets_recv": 1180,
      "bytes_sent": 2048576,
      "bytes_recv": 1842688
    },
    "timestamp": 1643723400.123
  }
  ```

### `GET /api/admin/stats`
- **Description**: Get document and processing statistics
- **Expected Status**: 200
- **Response**: System statistics and analytics

### `GET /api/admin/config`
- **Description**: Get current system configuration
- **Expected Status**: 200
- **Response**: Configuration parameters

### `POST /api/admin/config`
- **Description**: Update system configuration
- **Request Body**: Configuration updates
- **Expected Status**: 200

---

## Authentication & Security

### Authentication Methods
1. **API Key Authentication**
   - Header: `X-API-Key: test_api_key_for_backend_validation_2025`
   - Header: `Authorization: Bearer test_api_key_for_backend_validation_2025`

2. **Content-Type Headers**
   - `Content-Type: application/json` for JSON requests
   - `Content-Type: multipart/form-data` for file uploads

### Security Features
- Rate limiting (100 requests per minute per IP)
- Request validation and sanitization
- Security audit logging
- Command execution security levels

---

## WebSocket Endpoints

### `WS /ws`
- **Description**: Real-time communication for agent updates and workflow progress
- **Query Parameters**: `client_id` (optional)
- **Features**:
  - Agent status updates
  - Workflow progress notifications
  - System health monitoring
  - Real-time log streaming

### Message Types
```json
{
  "type": "ping|pong|subscribe|get_status|agent_update|workflow_progress",
  "data": { ... }
}
```

---

## Error Handling

### Standard Error Response
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": {
      "field": "repository_url",
      "reason": "URL format is invalid"
    }
  },
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### HTTP Status Codes
- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `204 No Content`: Resource deleted successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Invalid or missing API key
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

---

## Context Engineering Integration

The system implements advanced Context Engineering principles from the davidkimai/Context-Engineering research:

### Core Concepts Implemented
1. **Context Formalization**: `C = A(c₁, c₂, ..., cₙ)`
2. **Information-theoretic optimization**
3. **Multi-modal context integration**
4. **Context retrieval and generation strategies**

### Applications in Automotas AI
- **RAG Systems**: Document processing with context optimization
- **Multi-Agent Coordination**: Context-aware agent communication
- **Tool Integration**: Context-driven tool selection and usage
- **Memory Systems**: Hierarchical context storage and retrieval

---

## Testing Endpoints

All endpoints have been thoroughly tested with:
- **Real Data**: No fake or mock data used
- **Performance Testing**: Locust single-user testing
- **Comprehensive Logging**: JSON logs for all requests/responses
- **Error Analysis**: Detailed error tracking and reporting

### Test Data Examples
- **Agents**: Context Engineering, Code Analysis, Research Assistant agents
- **Workflows**: Multi-step analysis and review workflows  
- **Documents**: Research papers, architecture docs, system documentation
- **Context Queries**: Real questions about context engineering and system architecture

---

## Development & Deployment

### Current Deployment
- **Backend API**: Running on port 8001 (Docker container)
- **Nginx Configuration**: 
  - `api.automatos.app` - Main API
  - `mcp.automatos.app` - MCP server
  - `ui.automatos.app` - Frontend UI

### Development URLs
- `http://localhost:8001` - Backend API
- `http://localhost:8002` - Main orchestrator
- `http://206.81.0.227:8001` - Production backend

This comprehensive documentation serves as the complete reference for all available endpoints in the Automotas AI system, enabling precise testing and integration.