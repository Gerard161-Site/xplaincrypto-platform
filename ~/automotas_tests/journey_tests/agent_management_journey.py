#!/usr/bin/env python3
"""
Agent Management Journey Test

This test covers the complete agent lifecycle:
1. Agent Creation
2. Skills Assignment  
3. Agent Execution
4. Performance Monitoring
5. Agent Updates/Configuration
6. Agent Cloning
7. Error Handling & Recovery
8. Agent Cleanup/Deletion

Includes both positive and negative test scenarios.
"""

import sys
import os
import time
from typing import Dict, Any, List, Optional

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from test_logger import WorkflowTestLogger
from api_client import AutomotasAPIClient
from data_generators import TestData

class AgentManagementJourney:
    """Complete agent management workflow testing"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.logger = WorkflowTestLogger("agent_management_journey")
        self.api = AutomotasAPIClient(base_url, self.logger)
        
        # Track created resources for cleanup
        self.created_agents: List[str] = []
        self.created_skills: List[str] = []
        
        # Journey metrics
        self.journey_stats = {
            "steps_completed": 0,
            "steps_failed": 0,
            "agents_created": 0,
            "skills_created": 0,
            "api_calls_made": 0,
            "errors_encountered": 0
        }
    
    def run_full_journey(self) -> bool:
        """Run the complete agent management journey"""
        
        try:
            self.logger.log_step("journey_start", "Starting Agent Management Journey", "in_progress")
            
            # Phase 1: Environment Setup & Validation
            if not self._phase1_setup():
                return False
            
            # Phase 2: Agent Creation & Basic Operations
            if not self._phase2_agent_creation():
                return False
            
            # Phase 3: Skills Management
            if not self._phase3_skills_management():
                return False
            
            # Phase 4: Agent Execution & Monitoring
            if not self._phase4_execution_monitoring():
                return False
            
            # Phase 5: Advanced Operations
            if not self._phase5_advanced_operations():
                return False
            
            # Phase 6: Error Handling & Edge Cases
            if not self._phase6_error_handling():
                return False
            
            # Phase 7: Performance Validation
            if not self._phase7_performance_validation():
                return False
            
            # Phase 8: Cleanup
            self._phase8_cleanup()
            
            # Journey completed successfully
            self._log_journey_success()
            return True
            
        except Exception as e:
            self.logger.log_error(f"Journey failed with exception: {str(e)}", e)
            self._phase8_cleanup()  # Ensure cleanup even on failure
            self._log_journey_failure()
            return False
    
    def _phase1_setup(self) -> bool:
        """Phase 1: Environment Setup & Validation"""
        
        self.logger.log_step("phase1_start", "Phase 1: Environment Setup & Validation", "in_progress")
        
        # 1.1 Health Check
        self.logger.log_step("health_check", "System Health Check", "in_progress")
        health_response = self.api.health_check()
        
        if not self.api.validate_response(health_response, 200):
            self.logger.log_step("health_check", "System Health Check", "failed")
            return False
        
        self.logger.log_step("health_check", "System Health Check", "completed")
        
        # 1.2 API System Health
        self.logger.log_step("system_health", "API System Health Check", "in_progress")
        system_health = self.api.get("/api/system/health")
        
        if not self.api.validate_response(system_health, 200):
            self.logger.log_step("system_health", "API System Health Check", "failed")
            return False
        
        self.logger.log_step("system_health", "API System Health Check", "completed")
        
        # 1.3 Agent System Availability
        self.logger.log_step("agent_system_check", "Agent System Availability", "in_progress")
        agents_list = self.api.get("/api/agents/")
        
        if not self.api.validate_response(agents_list, 200):
            self.logger.log_step("agent_system_check", "Agent System Availability", "failed")
            return False
        
        self.logger.log_step("agent_system_check", "Agent System Availability", "completed")
        
        # 1.4 Skills System Availability
        self.logger.log_step("skills_system_check", "Skills System Availability", "in_progress")
        skills_list = self.api.get("/api/agents/skills")
        
        if not self.api.validate_response(skills_list, 200):
            self.logger.log_step("skills_system_check", "Skills System Availability", "failed")
            return False
        
        self.logger.log_step("skills_system_check", "Skills System Availability", "completed")
        
        self.logger.log_step("phase1_complete", "Phase 1: Environment Setup Complete", "completed")
        self.journey_stats["steps_completed"] += 4
        return True
    
    def _phase2_agent_creation(self) -> bool:
        """Phase 2: Agent Creation & Basic Operations"""
        
        self.logger.log_step("phase2_start", "Phase 2: Agent Creation & Basic Operations", "in_progress")
        
        # 2.1 Create Primary Test Agent
        self.logger.log_step("create_primary_agent", "Create Primary Test Agent", "in_progress")
        
        agent_data = TestData.Agent.create_agent_data(
            agent_type="code_architect",
            name="PrimaryTestAgent_Journey"
        )
        
        create_response = self.api.post("/api/agents/", agent_data)
        
        if not self.api.validate_response(create_response, 200):
            self.logger.log_step("create_primary_agent", "Create Primary Test Agent", "failed")
            return False
        
        # Extract agent ID
        primary_agent_id = self.api.extract_id(create_response)
        if not primary_agent_id:
            self.logger.log_step("create_primary_agent", "Failed to extract agent ID", "failed")
            return False
        
        self.created_agents.append(str(primary_agent_id))
        self.journey_stats["agents_created"] += 1
        
        # Validate agent data
        if not self.api.validate_data_contains(create_response, "name"):
            self.logger.log_step("create_primary_agent", "Agent name validation failed", "failed")
            return False
        
        self.logger.log_step("create_primary_agent", "Create Primary Test Agent", "completed",
                           metadata={"agent_id": primary_agent_id})
        
        # 2.2 Verify Agent Creation
        self.logger.log_step("verify_agent_creation", "Verify Agent Creation", "in_progress")
        
        get_agent_response = self.api.get(f"/api/agents/{primary_agent_id}")
        
        if not self.api.validate_response(get_agent_response, 200):
            self.logger.log_step("verify_agent_creation", "Verify Agent Creation", "failed")
            return False
        
        if not self.api.validate_data_contains(get_agent_response, "name", agent_data["name"]):
            self.logger.log_step("verify_agent_creation", "Agent name mismatch", "failed")
            return False
        
        self.logger.log_step("verify_agent_creation", "Verify Agent Creation", "completed")
        
        # 2.3 List All Agents (Verify Listing)
        self.logger.log_step("list_agents", "List All Agents", "in_progress")
        
        list_response = self.api.get("/api/agents/")
        
        if not self.api.validate_response(list_response, 200):
            self.logger.log_step("list_agents", "List All Agents", "failed")
            return False
        
        # Verify our agent is in the list
        agents_data = list_response.get("data", [])
        agent_found = False
        
        if isinstance(agents_data, list):
            for agent in agents_data:
                if str(agent.get("id")) == str(primary_agent_id):
                    agent_found = True
                    break
        
        if not agent_found:
            self.logger.log_step("list_agents", "Created agent not found in list", "failed")
            return False
        
        self.logger.log_step("list_agents", "List All Agents", "completed",
                           metadata={"total_agents": len(agents_data) if isinstance(agents_data, list) else 0})
        
        # 2.4 Create Secondary Agent (Different Type)
        self.logger.log_step("create_secondary_agent", "Create Secondary Test Agent", "in_progress")
        
        secondary_agent_data = TestData.Agent.create_agent_data(
            agent_type="security_expert",
            name="SecondaryTestAgent_Journey"
        )
        
        secondary_response = self.api.post("/api/agents/", secondary_agent_data)
        
        if self.api.validate_response(secondary_response, 200):
            secondary_agent_id = self.api.extract_id(secondary_response)
            if secondary_agent_id:
                self.created_agents.append(str(secondary_agent_id))
                self.journey_stats["agents_created"] += 1
                self.logger.log_step("create_secondary_agent", "Create Secondary Test Agent", "completed",
                                   metadata={"agent_id": secondary_agent_id})
            else:
                self.logger.log_step("create_secondary_agent", "Failed to extract secondary agent ID", "warning")
        else:
            self.logger.log_step("create_secondary_agent", "Create Secondary Test Agent", "warning")
        
        self.logger.log_step("phase2_complete", "Phase 2: Agent Creation Complete", "completed")
        self.journey_stats["steps_completed"] += 4
        return True
    
    def _phase3_skills_management(self) -> bool:
        """Phase 3: Skills Management"""
        
        self.logger.log_step("phase3_start", "Phase 3: Skills Management", "in_progress")
        
        if not self.created_agents:
            self.logger.log_step("phase3_prereq", "No agents available for skills testing", "failed")
            return False
        
        primary_agent_id = self.created_agents[0]
        
        # 3.1 List Available Skills
        self.logger.log_step("list_skills", "List Available Skills", "in_progress")
        
        skills_response = self.api.get("/api/agents/skills")
        
        if not self.api.validate_response(skills_response, 200):
            self.logger.log_step("list_skills", "List Available Skills", "failed")
            return False
        
        self.logger.log_step("list_skills", "List Available Skills", "completed")
        
        # 3.2 Create Test Skill
        self.logger.log_step("create_skill", "Create Test Skill", "in_progress")
        
        skill_data = TestData.Skill.create_skill_data(
            name="TestSkill_Journey",
            category="development"
        )
        
        skill_response = self.api.post("/api/agents/skills", skill_data)
        
        if self.api.validate_response(skill_response, 200):
            skill_id = self.api.extract_id(skill_response)
            if skill_id:
                self.created_skills.append(str(skill_id))
                self.journey_stats["skills_created"] += 1
                self.logger.log_step("create_skill", "Create Test Skill", "completed",
                                   metadata={"skill_id": skill_id})
            else:
                self.logger.log_step("create_skill", "Failed to extract skill ID", "warning")
                skill_id = None
        else:
            self.logger.log_step("create_skill", "Create Test Skill", "warning")
            skill_id = None
        
        # 3.3 Get Skills Categories
        self.logger.log_step("get_skills_categories", "Get Skills Categories", "in_progress")
        
        categories_response = self.api.get("/api/agents/skills/categories")
        
        if self.api.validate_response(categories_response, 200):
            self.logger.log_step("get_skills_categories", "Get Skills Categories", "completed")
        else:
            self.logger.log_step("get_skills_categories", "Get Skills Categories", "warning")
        
        # 3.4 Assign Skill to Agent (if skill was created)
        if skill_id:
            self.logger.log_step("assign_skill", "Assign Skill to Agent", "in_progress")
            
            assign_response = self.api.post(f"/api/agents/{primary_agent_id}/skills", {
                "skill_ids": [skill_id]
            })
            
            if self.api.validate_response(assign_response, 200):
                self.logger.log_step("assign_skill", "Assign Skill to Agent", "completed")
            else:
                self.logger.log_step("assign_skill", "Assign Skill to Agent", "warning")
        
        # 3.5 Get Agent Skills
        self.logger.log_step("get_agent_skills", "Get Agent Skills", "in_progress")
        
        agent_skills_response = self.api.get(f"/api/agents/{primary_agent_id}/skills")
        
        if self.api.validate_response(agent_skills_response, 200):
            self.logger.log_step("get_agent_skills", "Get Agent Skills", "completed")
        else:
            self.logger.log_step("get_agent_skills", "Get Agent Skills", "warning")
        
        self.logger.log_step("phase3_complete", "Phase 3: Skills Management Complete", "completed")
        self.journey_stats["steps_completed"] += 5
        return True
    
    def _phase4_execution_monitoring(self) -> bool:
        """Phase 4: Agent Execution & Monitoring"""
        
        self.logger.log_step("phase4_start", "Phase 4: Agent Execution & Monitoring", "in_progress")
        
        if not self.created_agents:
            self.logger.log_step("phase4_prereq", "No agents available for execution testing", "failed")
            return False
        
        primary_agent_id = self.created_agents[0]
        
        # 4.1 Start Agent
        self.logger.log_step("start_agent", "Start Agent", "in_progress")
        
        start_response = self.api.post(f"/api/agents/{primary_agent_id}/start")
        
        if self.api.validate_response(start_response, 200):
            self.logger.log_step("start_agent", "Start Agent", "completed")
        else:
            self.logger.log_step("start_agent", "Start Agent", "warning")
        
        # 4.2 Get Agent Performance
        self.logger.log_step("get_performance", "Get Agent Performance", "in_progress")
        
        performance_response = self.api.get(f"/api/agents/{primary_agent_id}/performance")
        
        if self.api.validate_response(performance_response, 200):
            self.logger.log_step("get_performance", "Get Agent Performance", "completed")
        else:
            self.logger.log_step("get_performance", "Get Agent Performance", "warning")
        
        # 4.3 Stop Agent
        self.logger.log_step("stop_agent", "Stop Agent", "in_progress")
        
        stop_response = self.api.post(f"/api/agents/{primary_agent_id}/stop")
        
        if self.api.validate_response(stop_response, 200):
            self.logger.log_step("stop_agent", "Stop Agent", "completed")
        else:
            self.logger.log_step("stop_agent", "Stop Agent", "warning")
        
        self.logger.log_step("phase4_complete", "Phase 4: Execution & Monitoring Complete", "completed")
        self.journey_stats["steps_completed"] += 3
        return True
    
    def _phase5_advanced_operations(self) -> bool:
        """Phase 5: Advanced Operations"""
        
        self.logger.log_step("phase5_start", "Phase 5: Advanced Operations", "in_progress")
        
        if not self.created_agents:
            self.logger.log_step("phase5_prereq", "No agents available for advanced operations", "failed")
            return False
        
        primary_agent_id = self.created_agents[0]
        
        # 5.1 Update Agent Configuration
        self.logger.log_step("update_agent", "Update Agent Configuration", "in_progress")
        
        # Get current agent data first
        current_agent_response = self.api.get(f"/api/agents/{primary_agent_id}")
        
        if self.api.validate_response(current_agent_response, 200):
            current_agent_data = current_agent_response.get("data", {})
            update_data = TestData.Agent.update_agent_data(current_agent_data)
            
            update_response = self.api.put(f"/api/agents/{primary_agent_id}", update_data)
            
            if self.api.validate_response(update_response, 200):
                self.logger.log_step("update_agent", "Update Agent Configuration", "completed")
            else:
                self.logger.log_step("update_agent", "Update Agent Configuration", "warning")
        else:
            self.logger.log_step("update_agent", "Failed to get current agent data", "warning")
        
        # 5.2 Clone Agent
        self.logger.log_step("clone_agent", "Clone Agent", "in_progress")
        
        clone_name = f"ClonedAgent_{TestData.random_string(6)}"
        clone_response = self.api.post(f"/api/agents/{primary_agent_id}/clone", {
            "new_name": clone_name
        })
        
        if self.api.validate_response(clone_response, 200):
            cloned_agent_id = self.api.extract_id(clone_response)
            if cloned_agent_id:
                self.created_agents.append(str(cloned_agent_id))
                self.journey_stats["agents_created"] += 1
                self.logger.log_step("clone_agent", "Clone Agent", "completed",
                                   metadata={"cloned_agent_id": cloned_agent_id})
            else:
                self.logger.log_step("clone_agent", "Failed to extract cloned agent ID", "warning")
        else:
            self.logger.log_step("clone_agent", "Clone Agent", "warning")
        
        self.logger.log_step("phase5_complete", "Phase 5: Advanced Operations Complete", "completed")
        self.journey_stats["steps_completed"] += 2
        return True
    
    def _phase6_error_handling(self) -> bool:
        """Phase 6: Error Handling & Edge Cases"""
        
        self.logger.log_step("phase6_start", "Phase 6: Error Handling & Edge Cases", "in_progress")
        
        # 6.1 Test Invalid Agent ID
        self.logger.log_step("test_invalid_agent_id", "Test Invalid Agent ID", "in_progress")
        
        invalid_id = "invalid_agent_999999"
        invalid_response = self.api.get(f"/api/agents/{invalid_id}")
        
        # We expect this to fail with 422 or 404
        if invalid_response["status_code"] in [404, 422]:
            self.logger.log_step("test_invalid_agent_id", "Test Invalid Agent ID", "completed",
                               metadata={"expected_error_received": True})
        else:
            self.logger.log_step("test_invalid_agent_id", "Unexpected response for invalid ID", "warning")
        
        # 6.2 Test Invalid Agent Creation Data
        self.logger.log_step("test_invalid_agent_data", "Test Invalid Agent Creation Data", "in_progress")
        
        invalid_agent_data = {
            "name": "",  # Empty name should fail
            "agent_type": "invalid_type"  # Invalid type should fail
        }
        
        invalid_create_response = self.api.post("/api/agents/", invalid_agent_data)
        
        # We expect this to fail with 422
        if invalid_create_response["status_code"] == 422:
            self.logger.log_step("test_invalid_agent_data", "Test Invalid Agent Creation Data", "completed",
                               metadata={"validation_error_received": True})
        else:
            self.logger.log_step("test_invalid_agent_data", "Validation error not received", "warning")
        
        # 6.3 Test Non-existent Skill Assignment
        if self.created_agents:
            self.logger.log_step("test_invalid_skill", "Test Invalid Skill Assignment", "in_progress")
            
            primary_agent_id = self.created_agents[0]
            invalid_skill_response = self.api.post(f"/api/agents/{primary_agent_id}/skills", {
                "skill_ids": [999999]  # Non-existent skill ID
            })
            
            # We expect this to fail
            if invalid_skill_response["status_code"] >= 400:
                self.logger.log_step("test_invalid_skill", "Test Invalid Skill Assignment", "completed",
                                   metadata={"error_handling_working": True})
            else:
                self.logger.log_step("test_invalid_skill", "Error handling needs improvement", "warning")
        
        self.logger.log_step("phase6_complete", "Phase 6: Error Handling Complete", "completed")
        self.journey_stats["steps_completed"] += 3
        return True
    
    def _phase7_performance_validation(self) -> bool:
        """Phase 7: Performance Validation"""
        
        self.logger.log_step("phase7_start", "Phase 7: Performance Validation", "in_progress")
        
        # 7.1 Measure Agent Listing Performance
        self.logger.log_step("measure_listing_performance", "Measure Agent Listing Performance", "in_progress")
        
        start_time = time.time()
        list_response = self.api.get("/api/agents/")
        response_time = (time.time() - start_time) * 1000
        
        if self.api.validate_response(list_response, 200):
            performance_acceptable = response_time < 5000  # 5 seconds threshold
            self.logger.log_step("measure_listing_performance", "Measure Agent Listing Performance", 
                               "completed" if performance_acceptable else "warning",
                               metadata={"response_time_ms": response_time, "acceptable": performance_acceptable})
        else:
            self.logger.log_step("measure_listing_performance", "Agent listing failed", "warning")
        
        # 7.2 Check System Statistics
        self.logger.log_step("check_system_stats", "Check Agent System Statistics", "in_progress")
        
        stats_response = self.api.get("/api/system/agents/statistics")
        
        if self.api.validate_response(stats_response, 200):
            self.logger.log_step("check_system_stats", "Check Agent System Statistics", "completed")
        else:
            self.logger.log_step("check_system_stats", "Agent statistics unavailable", "warning")
        
        self.logger.log_step("phase7_complete", "Phase 7: Performance Validation Complete", "completed")
        self.journey_stats["steps_completed"] += 2
        return True
    
    def _phase8_cleanup(self):
        """Phase 8: Cleanup (Always runs)"""
        
        self.logger.log_step("phase8_start", "Phase 8: Cleanup", "in_progress")
        
        cleanup_success = True
        
        # 8.1 Remove Skills from Agents
        for agent_id in self.created_agents:
            for skill_id in self.created_skills:
                try:
                    self.api.delete(f"/api/agents/{agent_id}/skills/{skill_id}")
                except:
                    pass
        
        # 8.2 Delete Created Skills
        for skill_id in self.created_skills:
            self.logger.log_step("cleanup_skill", f"Delete Skill {skill_id}", "in_progress")
            
            delete_response = self.api.delete(f"/api/agents/skills/{skill_id}")
            
            if self.api.validate_response(delete_response, 200):
                self.logger.log_step("cleanup_skill", f"Delete Skill {skill_id}", "completed")
            else:
                self.logger.log_step("cleanup_skill", f"Failed to delete Skill {skill_id}", "warning")
                cleanup_success = False
        
        # 8.3 Delete Created Agents
        for agent_id in self.created_agents:
            self.logger.log_step("cleanup_agent", f"Delete Agent {agent_id}", "in_progress")
            
            delete_response = self.api.delete(f"/api/agents/{agent_id}")
            
            if self.api.validate_response(delete_response, 200):
                self.logger.log_step("cleanup_agent", f"Delete Agent {agent_id}", "completed")
            else:
                self.logger.log_step("cleanup_agent", f"Failed to delete Agent {agent_id}", "warning")
                cleanup_success = False
        
        status = "completed" if cleanup_success else "warning"
        self.logger.log_step("phase8_complete", "Phase 8: Cleanup Complete", status)
        
        if cleanup_success:
            self.journey_stats["steps_completed"] += 1
    
    def _log_journey_success(self):
        """Log successful journey completion"""
        
        summary = {
            "status": "SUCCESS",
            "total_steps": self.journey_stats["steps_completed"],
            "failed_steps": self.journey_stats["steps_failed"],
            "agents_created": self.journey_stats["agents_created"],
            "skills_created": self.journey_stats["skills_created"],
            "success_rate": f"{(self.journey_stats['steps_completed'] / (self.journey_stats['steps_completed'] + self.journey_stats['steps_failed']) * 100):.1f}%" if (self.journey_stats['steps_completed'] + self.journey_stats['steps_failed']) > 0 else "100%"
        }
        
        self.logger.log_journey_end("completed", summary)
    
    def _log_journey_failure(self):
        """Log failed journey completion"""
        
        summary = {
            "status": "FAILED",
            "total_steps": self.journey_stats["steps_completed"],
            "failed_steps": self.journey_stats["steps_failed"],
            "agents_created": self.journey_stats["agents_created"],
            "skills_created": self.journey_stats["skills_created"]
        }
        
        self.logger.log_journey_end("failed", summary)


def main():
    """Run the Agent Management Journey Test"""
    
    print("🚀 Starting Agent Management Journey Test")
    
    # Initialize and run journey
    journey = AgentManagementJourney()
    success = journey.run_full_journey()
    
    if success:
        print("✅ Agent Management Journey completed successfully!")
        return 0
    else:
        print("❌ Agent Management Journey failed!")
        return 1


if __name__ == "__main__":
    exit(main())