#!/usr/bin/env python3
"""
COMPREHENSIVE AUTOMOTAS AI TESTING - MASTER TEST RUNNER
Executes all three phases of testing with full logging and reporting
"""

import sys
import os
import subprocess
import time
import json
from datetime import datetime
from pathlib import Path

class MasterTestRunner:
    """
    Master test runner for all comprehensive testing phases
    """
    
    def __init__(self):
        self.test_dir = Path(__file__).parent
        self.phases = [
            {
                "name": "Phase 1: Agent Management",
                "script": "phase1_agent_management/scripts/comprehensive_agent_test.py",
                "description": "Complete agent lifecycle, skills, and execution testing"
            },
            {
                "name": "Phase 2: Workflow Orchestration",
                "script": "phase2_workflow_orchestration/scripts/comprehensive_workflow_test.py",
                "description": "Pattern management, templates, and workflow analytics"
            },
            {
                "name": "Phase 3: Document Management",
                "script": "phase3_document_management/scripts/comprehensive_document_test.py",
                "description": "Document processing, analytics, and system integration"
            }
        ]
        
        self.results = {}
        self.master_log = []
        
    def run_all_phases(self):
        """
        Execute all testing phases sequentially
        """
        print("🚀 AUTOMOTAS AI COMPREHENSIVE TESTING - MASTER EXECUTION")
        print("=" * 70)
        print(f"⏰ Started at: {datetime.now().isoformat()}")
        print()
        
        start_time = time.time()
        overall_success = True
        
        for i, phase in enumerate(self.phases, 1):
            print(f"\n{'='*20} {phase['name'].upper()} {'='*20}")
            print(f"📋 Description: {phase['description']}")
            print(f"📄 Script: {phase['script']}")
            print()
            
            # Log phase start
            phase_start = time.time()
            self.log_event("phase_start", phase['name'], {"script": phase['script']})
            
            # Execute phase
            success = self.run_phase(phase)
            phase_duration = time.time() - phase_start
            
            # Log phase completion
            self.log_event("phase_complete", phase['name'], {
                "success": success,
                "duration_seconds": round(phase_duration, 2)
            })
            
            # Store results
            self.results[f"phase_{i}"] = {
                "name": phase['name'],
                "success": success,
                "duration": phase_duration,
                "script": phase['script']
            }
            
            if not success:
                overall_success = False
                print(f"❌ {phase['name']} FAILED!")
                # Continue with other phases even if one fails
            else:
                print(f"✅ {phase['name']} COMPLETED SUCCESSFULLY!")
        
        # Generate master report
        total_duration = time.time() - start_time
        self.generate_master_report(overall_success, total_duration)
        
        print(f"\n{'='*70}")
        print(f"🏁 MASTER TESTING COMPLETED")
        print(f"⏱️ Total Duration: {round(total_duration, 2)} seconds")
        print(f"📊 Overall Success: {'✅ YES' if overall_success else '❌ NO'}")
        
        return overall_success
    
    def run_phase(self, phase):
        """
        Execute a single testing phase
        """
        script_path = self.test_dir / phase['script']
        
        if not script_path.exists():
            print(f"❌ Script not found: {script_path}")
            return False
        
        try:
            # Make script executable
            script_path.chmod(0o755)
            
            # Execute the test script
            print(f"🚀 Executing: {script_path}")
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(script_path.parent),
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout per phase
            )
            
            # Log output
            self.log_event("phase_output", phase['name'], {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            })
            
            # Print output
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            print(f"❌ {phase['name']} timed out after 10 minutes")
            return False
        except Exception as e:
            print(f"❌ {phase['name']} failed with exception: {str(e)}")
            return False
    
    def log_event(self, event_type, phase_name, data):
        """
        Log an event to the master log
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "phase_name": phase_name,
            "data": data
        }
        self.master_log.append(log_entry)
    
    def generate_master_report(self, overall_success, total_duration):
        """
        Generate comprehensive master report
        """
        report = {
            "test_execution": {
                "timestamp": datetime.now().isoformat(),
                "overall_success": overall_success,
                "total_duration_seconds": round(total_duration, 2),
                "phases_executed": len(self.phases)
            },
            "phase_results": self.results,
            "summary": {
                "successful_phases": len([r for r in self.results.values() if r['success']]),
                "failed_phases": len([r for r in self.results.values() if not r['success']]),
                "success_rate": round((len([r for r in self.results.values() if r['success']]) / len(self.phases)) * 100, 2)
            },
            "detailed_log": self.master_log
        }
        
        # Save master report
        report_file = self.test_dir / f"MASTER_TEST_REPORT_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Create summary report
        summary_file = self.test_dir / f"MASTER_SUMMARY_{int(time.time())}.md"
        with open(summary_file, 'w') as f:
            f.write(f"# AUTOMOTAS AI COMPREHENSIVE TESTING - MASTER REPORT\n\n")
            f.write(f"**Execution Time:** {datetime.now().isoformat()}\n")
            f.write(f"**Overall Success:** {'✅ YES' if overall_success else '❌ NO'}\n")
            f.write(f"**Total Duration:** {round(total_duration, 2)} seconds\n\n")
            
            f.write(f"## Phase Results\n\n")
            for phase_key, phase_result in self.results.items():
                status = "✅ SUCCESS" if phase_result['success'] else "❌ FAILED"
                f.write(f"### {phase_result['name']}\n")
                f.write(f"- **Status:** {status}\n")
                f.write(f"- **Duration:** {round(phase_result['duration'], 2)} seconds\n")
                f.write(f"- **Script:** `{phase_result['script']}`\n\n")
            
            f.write(f"## Summary Statistics\n\n")
            f.write(f"- **Successful Phases:** {report['summary']['successful_phases']}/{len(self.phases)}\n")
            f.write(f"- **Success Rate:** {report['summary']['success_rate']}%\n")
            f.write(f"- **Failed Phases:** {report['summary']['failed_phases']}\n\n")
        
        print(f"\n📊 Master report saved to: {report_file}")
        print(f"📄 Summary report saved to: {summary_file}")
        
        return report

def main():
    """
    Main execution function
    """
    print("🚀 AUTOMOTAS AI COMPREHENSIVE TESTING SUITE")
    print("===========================================")
    
    runner = MasterTestRunner()
    success = runner.run_all_phases()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())