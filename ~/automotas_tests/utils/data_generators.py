import random
import string
from datetime import datetime, timedelta
from typing import Dict, Any, List
import uuid

class TestDataGenerator:
    """Generate realistic test data for Automotas AI workflow testing"""
    
    @staticmethod
    def random_string(length: int = 8, prefix: str = "") -> str:
        """Generate random string for unique identifiers"""
        chars = string.ascii_lowercase + string.digits
        random_part = ''.join(random.choices(chars, k=length))
        return f"{prefix}{random_part}" if prefix else random_part
    
    @staticmethod
    def random_email() -> str:
        """Generate random email"""
        username = TestDataGenerator.random_string(8)
        domains = ["test.com", "example.org", "automotas.dev"]
        return f"{username}@{random.choice(domains)}"
    
    @staticmethod
    def timestamp() -> str:
        """Generate current timestamp"""
        return datetime.now().isoformat()

class AgentDataGenerator:
    """Generate test data for agent management"""
    
    AGENT_TYPES = [
        "code_architect",
        "security_expert", 
        "performance_optimizer",
        "data_analyst",
        "infrastructure_manager",
        "custom",
        "system",
        "specialized"
    ]
    
    PRIORITY_LEVELS = ["low", "medium", "high", "critical"]
    
    AGENT_STATUSES = ["active", "inactive", "training"]
    
    @classmethod
    def create_agent_data(cls, agent_type: str = None, name: str = None) -> Dict[str, Any]:
        """Generate data for creating an agent"""
        
        if not agent_type:
            agent_type = random.choice(cls.AGENT_TYPES)
        
        if not name:
            name = f"TestAgent_{TestDataGenerator.random_string(6)}"
        
        return {
            "name": name,
            "description": f"Test agent for {agent_type} operations - created for journey testing",
            "agent_type": agent_type,
            "configuration": {
                "test_mode": True,
                "created_by": "journey_test",
                "environment": "testing"
            },
            "skill_ids": [],  # Will be populated when skills are created
            "priority_level": random.choice(cls.PRIORITY_LEVELS),
            "max_concurrent_tasks": random.randint(1, 10),
            "auto_start": False  # For testing, we want manual control
        }
    
    @classmethod
    def update_agent_data(cls, existing_agent: Dict[str, Any]) -> Dict[str, Any]:
        """Generate data for updating an agent"""
        return {
            "description": f"Updated description at {TestDataGenerator.timestamp()}",
            "priority_level": random.choice(cls.PRIORITY_LEVELS),
            "max_concurrent_tasks": random.randint(5, 15),
            "configuration": {
                **existing_agent.get("configuration", {}),
                "last_updated": TestDataGenerator.timestamp(),
                "test_update": True
            }
        }
    
    @classmethod
    def agent_task_data(cls) -> Dict[str, Any]:
        """Generate data for agent task execution"""
        tasks = [
            "analyze_code_quality",
            "security_scan",
            "performance_optimization",
            "data_analysis",
            "infrastructure_check"
        ]
        
        return {
            "task": random.choice(tasks),
            "priority": random.choice(cls.PRIORITY_LEVELS),
            "parameters": {
                "test_execution": True,
                "timeout_seconds": 30,
                "notify_completion": False
            },
            "metadata": {
                "created_by": "journey_test",
                "timestamp": TestDataGenerator.timestamp()
            }
        }

class SkillDataGenerator:
    """Generate test data for skills management"""
    
    SKILL_CATEGORIES = ["development", "security", "infrastructure", "analytics"]
    SKILL_TYPES = ["cognitive", "technical", "communication"]
    
    @classmethod
    def create_skill_data(cls, name: str = None, category: str = None) -> Dict[str, Any]:
        """Generate data for creating a skill"""
        
        if not name:
            name = f"TestSkill_{TestDataGenerator.random_string(6)}"
        
        if not category:
            category = random.choice(cls.SKILL_CATEGORIES)
        
        return {
            "name": name,
            "description": f"Test skill for {category} - created during journey testing",
            "skill_type": random.choice(cls.SKILL_TYPES),
            "category": category,
            "implementation": f"test_implementation_{TestDataGenerator.random_string(4)}",
            "parameters": {
                "test_mode": True,
                "complexity": random.choice(["beginner", "intermediate", "advanced"]),
                "estimated_time_minutes": random.randint(5, 60)
            }
        }
    
    @classmethod
    def update_skill_data(cls) -> Dict[str, Any]:
        """Generate data for updating a skill"""
        return {
            "description": f"Updated skill description at {TestDataGenerator.timestamp()}",
            "parameters": {
                "test_mode": True,
                "last_updated": TestDataGenerator.timestamp(),
                "version": f"1.{random.randint(1, 10)}"
            }
        }

class WorkflowDataGenerator:
    """Generate test data for workflow management"""
    
    @classmethod
    def create_workflow_data(cls, name: str = None) -> Dict[str, Any]:
        """Generate data for creating a workflow"""
        
        if not name:
            name = f"TestWorkflow_{TestDataGenerator.random_string(6)}"
        
        return {
            "name": name,
            "description": f"Test workflow created for journey testing at {TestDataGenerator.timestamp()}",
            "configuration": {
                "test_mode": True,
                "auto_execute": False,
                "timeout_minutes": 30
            },
            "steps": [
                {
                    "step_id": "init",
                    "step_name": "Initialize workflow",
                    "step_type": "initialization"
                },
                {
                    "step_id": "process",
                    "step_name": "Process data",
                    "step_type": "processing"
                },
                {
                    "step_id": "finalize",
                    "step_name": "Finalize workflow",
                    "step_type": "finalization"
                }
            ],
            "metadata": {
                "created_by": "journey_test",
                "environment": "testing"
            }
        }
    
    @classmethod
    def workflow_execution_data(cls) -> Dict[str, Any]:
        """Generate data for workflow execution"""
        return {
            "execution_mode": "test",
            "parameters": {
                "test_run": True,
                "notify_completion": False,
                "timeout_seconds": 60
            },
            "metadata": {
                "triggered_by": "journey_test",
                "execution_time": TestDataGenerator.timestamp()
            }
        }

class DocumentDataGenerator:
    """Generate test data for document management"""
    
    DOCUMENT_TYPES = ["pdf", "txt", "md", "docx", "json"]
    
    @classmethod
    def document_upload_data(cls, doc_type: str = None) -> Dict[str, Any]:
        """Generate data for document upload"""
        
        if not doc_type:
            doc_type = random.choice(cls.DOCUMENT_TYPES)
        
        doc_name = f"test_document_{TestDataGenerator.random_string(6)}.{doc_type}"
        
        return {
            "title": f"Test Document - {doc_name}",
            "filename": doc_name,
            "content_type": f"application/{doc_type}",
            "description": f"Test document uploaded during journey testing",
            "tags": ["test", "journey", "automation"],
            "metadata": {
                "uploaded_by": "journey_test",
                "test_document": True,
                "upload_time": TestDataGenerator.timestamp()
            }
        }
    
    @classmethod
    def document_content(cls) -> str:
        """Generate sample document content"""
        content_samples = [
            "This is a test document created for Automotas AI journey testing.",
            "Sample content for document processing and analysis workflows.",
            "Technical documentation example for vector embedding and retrieval testing.",
            "Test data for validating document processing pipeline functionality."
        ]
        
        return f"{random.choice(content_samples)} Generated at {TestDataGenerator.timestamp()}"

class ConfigDataGenerator:
    """Generate test data for configuration management"""
    
    @classmethod
    def system_config_data(cls, config_key: str = None) -> Dict[str, Any]:
        """Generate data for system configuration"""
        
        if not config_key:
            config_key = f"test_config_{TestDataGenerator.random_string(6)}"
        
        return {
            "config_key": config_key,
            "config_value": {
                "test_setting": True,
                "environment": "testing",
                "value": random.randint(1, 100),
                "updated_at": TestDataGenerator.timestamp()
            },
            "description": f"Test configuration created during journey testing"
        }
    
    @classmethod
    def rag_config_data(cls, name: str = None) -> Dict[str, Any]:
        """Generate data for RAG configuration"""
        
        if not name:
            name = f"TestRAG_{TestDataGenerator.random_string(6)}"
        
        return {
            "name": name,
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "chunk_size": random.choice([500, 1000, 1500]),
            "chunk_overlap": random.choice([100, 200, 300]),
            "retrieval_strategy": "similarity",
            "top_k": random.randint(3, 10),
            "similarity_threshold": round(random.uniform(0.5, 0.9), 2),
            "configuration": {
                "test_mode": True,
                "created_by": "journey_test",
                "environment": "testing"
            }
        }

class PatternDataGenerator:
    """Generate test data for pattern management"""
    
    PATTERN_TYPES = [
        "workflow_optimization",
        "agent_behavior",
        "performance_pattern",
        "error_recovery",
        "resource_usage"
    ]
    
    @classmethod
    def create_pattern_data(cls, name: str = None, pattern_type: str = None) -> Dict[str, Any]:
        """Generate data for creating a pattern"""
        
        if not name:
            name = f"TestPattern_{TestDataGenerator.random_string(6)}"
        
        if not pattern_type:
            pattern_type = random.choice(cls.PATTERN_TYPES)
        
        return {
            "name": name,
            "description": f"Test pattern for {pattern_type} analysis",
            "pattern_type": pattern_type,
            "pattern_data": {
                "test_pattern": True,
                "complexity": random.choice(["simple", "moderate", "complex"]),
                "effectiveness_threshold": round(random.uniform(0.6, 0.95), 2),
                "created_at": TestDataGenerator.timestamp()
            }
        }

# Convenience class for easy access to all generators
class TestData:
    """Convenience class providing access to all data generators"""
    
    Agent = AgentDataGenerator
    Skill = SkillDataGenerator
    Workflow = WorkflowDataGenerator
    Document = DocumentDataGenerator
    Config = ConfigDataGenerator
    Pattern = PatternDataGenerator
    
    @staticmethod
    def random_string(length: int = 8, prefix: str = "") -> str:
        return TestDataGenerator.random_string(length, prefix)
    
    @staticmethod
    def random_email() -> str:
        return TestDataGenerator.random_email()
    
    @staticmethod
    def timestamp() -> str:
        return TestDataGenerator.timestamp()