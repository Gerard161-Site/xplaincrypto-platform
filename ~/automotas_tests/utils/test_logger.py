import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class WorkflowTestLogger:
    """Enhanced workflow testing logger that provides structured JSON logging for test journeys"""
    
    def __init__(self, journey_name: str, log_file: Optional[str] = None):
        self.journey_name = journey_name
        self.start_time = datetime.now()
        
        # Set up log file
        if log_file:
            self.log_file = log_file
        else:
            timestamp = self.start_time.strftime('%Y%m%d_%H%M%S')
            self.log_file = f"~/automotas_tests/logs/{journey_name}_{timestamp}.log"
        
        # Ensure log directory exists
        Path(self.log_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        self.logger = logging.getLogger(f"workflow_{journey_name}")
        self.logger.setLevel(logging.INFO)
        
        # Clear any existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.INFO)
        
        # Console handler  
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Initialize journey
        self.log_journey_start()
    
    def log_journey_start(self):
        """Log the start of a journey"""
        journey_info = {
            "event": "journey_start",
            "journey_name": self.journey_name,
            "start_time": self.start_time.isoformat(),
            "log_file": self.log_file
        }
        self.logger.info(f"🚀 JOURNEY STARTED: {self.journey_name}")
        self.logger.info(f"📁 Log file: {self.log_file}")
        self.logger.info(f"⏰ Start time: {self.start_time}")
    
    def log_step(self, step_id: str, step_name: str, status: str = "in_progress", 
                 response: Any = None, metadata: Optional[Dict[str, Any]] = None):
        """Log a journey step with structured data"""
        
        step_data = {
            "event": "journey_step",
            "journey_name": self.journey_name,
            "step_id": step_id,
            "step_name": step_name,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "response": response,
            "metadata": metadata or {}
        }
        
        # Determine log level and emoji based on status
        if status == "completed":
            emoji = "✅"
            level = logging.INFO
        elif status == "failed":
            emoji = "❌"
            level = logging.ERROR
        elif status == "warning":
            emoji = "⚠️"
            level = logging.WARNING
        else:
            emoji = "🔄"
            level = logging.INFO
        
        message = f"{emoji} STEP {status.upper()}: [{step_id}] {step_name}"
        
        # Log structured data as JSON for parsing
        self.logger.log(level, message)
        
        # Also log JSON data for automated processing
        json_data = json.dumps(step_data, indent=2, default=str)
        with open(self.log_file, 'a') as f:
            f.write(f"JSON_DATA: {json_data}\n")
    
    def log_api_call(self, method: str, endpoint: str, status_code: int, 
                     response_time_ms: float, response_data: Any = None,
                     request_data: Any = None):
        """Log API call details"""
        
        api_data = {
            "event": "api_call",
            "method": method,
            "endpoint": endpoint,
            "status_code": status_code,
            "response_time_ms": response_time_ms,
            "timestamp": datetime.now().isoformat(),
            "request_data": request_data,
            "response_data": response_data
        }
        
        status_emoji = "✅" if status_code < 400 else "❌"
        message = f"{status_emoji} API {method} {endpoint} - HTTP {status_code} ({response_time_ms:.1f}ms)"
        
        if status_code < 400:
            self.logger.info(message)
        else:
            self.logger.error(message)
        
        # Log JSON data
        json_data = json.dumps(api_data, indent=2, default=str)
        with open(self.log_file, 'a') as f:
            f.write(f"JSON_DATA: {json_data}\n")
    
    def log_validation(self, validation_name: str, expected: Any, actual: Any, passed: bool):
        """Log validation results"""
        
        validation_data = {
            "event": "validation",
            "validation_name": validation_name,
            "expected": expected,
            "actual": actual,
            "passed": passed,
            "timestamp": datetime.now().isoformat()
        }
        
        emoji = "✅" if passed else "❌"
        status = "PASSED" if passed else "FAILED"
        message = f"{emoji} VALIDATION {status}: {validation_name}"
        
        if passed:
            self.logger.info(message)
        else:
            self.logger.error(message)
            self.logger.error(f"  Expected: {expected}")
            self.logger.error(f"  Actual: {actual}")
        
        # Log JSON data
        json_data = json.dumps(validation_data, indent=2, default=str)
        with open(self.log_file, 'a') as f:
            f.write(f"JSON_DATA: {json_data}\n")
    
    def log_journey_end(self, status: str = "completed", summary: Optional[Dict[str, Any]] = None):
        """Log the end of a journey"""
        
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        journey_summary = {
            "event": "journey_end",
            "journey_name": self.journey_name,
            "status": status,
            "start_time": self.start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": duration,
            "summary": summary or {}
        }
        
        emoji = "🎉" if status == "completed" else "💥"
        self.logger.info(f"{emoji} JOURNEY {status.upper()}: {self.journey_name}")
        self.logger.info(f"⏱️ Duration: {duration:.2f} seconds")
        
        if summary:
            self.logger.info("📊 Summary:")
            for key, value in summary.items():
                self.logger.info(f"  {key}: {value}")
        
        # Log JSON data
        json_data = json.dumps(journey_summary, indent=2, default=str)
        with open(self.log_file, 'a') as f:
            f.write(f"JSON_DATA: {json_data}\n")
    
    def log_error(self, error_message: str, exception: Optional[Exception] = None):
        """Log error with details"""
        
        error_data = {
            "event": "error",
            "journey_name": self.journey_name,
            "error_message": error_message,
            "exception": str(exception) if exception else None,
            "timestamp": datetime.now().isoformat()
        }
        
        self.logger.error(f"💥 ERROR: {error_message}")
        if exception:
            self.logger.error(f"Exception details: {exception}")
        
        # Log JSON data
        json_data = json.dumps(error_data, indent=2, default=str)
        with open(self.log_file, 'a') as f:
            f.write(f"JSON_DATA: {json_data}\n")