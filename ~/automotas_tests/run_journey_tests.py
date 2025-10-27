#!/usr/bin/env python3
"""
Automotas AI Journey Test Runner

This script runs individual journey tests or all available journey tests.
"""

import os
import sys
import argparse
import time
from datetime import datetime
from typing import List, Dict, Any

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from test_logger import WorkflowTestLogger

class JourneyTestRunner:
    """Master test runner for all journey tests"""
    
    def __init__(self):
        self.available_journeys = {
            "agent_management": {
                "module": "journey_tests.agent_management_journey",
                "class": "AgentManagementJourney",
                "description": "Complete agent lifecycle testing"
            },
            # Future journeys will be added here
            # "workflow_orchestration": {...},
            # "document_management": {...},
            # "context_engineering": {...},
            # "performance_analytics": {...}
        }
        
        self.logger = WorkflowTestLogger("journey_test_runner")
        self.results = {}
    
    def list_available_journeys(self):
        """List all available journey tests"""
        print("\n🚀 Available Journey Tests:")
        print("=" * 50)
        
        for journey_name, info in self.available_journeys.items():
            print(f"  📋 {journey_name}")
            print(f"     Description: {info['description']}")
            print()
    
    def run_journey(self, journey_name: str) -> bool:
        """Run a specific journey test"""
        
        if journey_name not in self.available_journeys:
            print(f"❌ Journey '{journey_name}' not found!")
            self.list_available_journeys()
            return False
        
        journey_info = self.available_journeys[journey_name]
        
        print(f"\n🔬 Running Journey: {journey_name}")
        print(f"📖 Description: {journey_info['description']}")
        print("=" * 60)
        
        try:
            # Import and instantiate the journey class
            module_path = journey_info["module"]
            class_name = journey_info["class"]
            
            # Dynamic import
            module = __import__(module_path, fromlist=[class_name])
            journey_class = getattr(module, class_name)
            
            # Run the journey
            start_time = time.time()
            journey_instance = journey_class()
            success = journey_instance.run_full_journey()
            duration = time.time() - start_time
            
            # Record results
            self.results[journey_name] = {
                "success": success,
                "duration": duration,
                "timestamp": datetime.now().isoformat()
            }
            
            # Log results
            self.logger.log_step(
                f"journey_{journey_name}",
                f"Journey {journey_name} completed",
                "completed" if success else "failed",
                metadata={
                    "duration_seconds": duration,
                    "success": success
                }
            )
            
            if success:
                print(f"\n✅ Journey '{journey_name}' completed successfully!")
                print(f"⏱️  Duration: {duration:.2f} seconds")
            else:
                print(f"\n❌ Journey '{journey_name}' failed!")
                print(f"⏱️  Duration: {duration:.2f} seconds")
            
            return success
            
        except Exception as e:
            print(f"\n💥 Error running journey '{journey_name}': {str(e)}")
            self.logger.log_error(f"Journey {journey_name} failed with exception", e)
            
            self.results[journey_name] = {
                "success": False,
                "duration": 0,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            
            return False
    
    def run_all_journeys(self) -> Dict[str, bool]:
        """Run all available journey tests"""
        
        print("\n🚀 Running ALL Journey Tests")
        print("=" * 60)
        
        results = {}
        
        for journey_name in self.available_journeys.keys():
            print(f"\n{'='*20} JOURNEY {len(results)+1}/{len(self.available_journeys)} {'='*20}")
            success = self.run_journey(journey_name)
            results[journey_name] = success
            
            # Brief pause between journeys
            if len(results) < len(self.available_journeys):
                print("\n⏸️  Pausing 3 seconds before next journey...")
                time.sleep(3)
        
        return results
    
    def generate_summary_report(self):
        """Generate a summary report of all test results"""
        
        if not self.results:
            print("\n📊 No test results to report.")
            return
        
        print("\n" + "="*60)
        print("📊 JOURNEY TESTING SUMMARY REPORT")
        print("="*60)
        
        successful_journeys = [name for name, result in self.results.items() if result["success"]]
        failed_journeys = [name for name, result in self.results.items() if not result["success"]]
        
        total_duration = sum(result["duration"] for result in self.results.values())
        
        print(f"\n📈 OVERALL RESULTS:")
        print(f"   Total Journeys: {len(self.results)}")
        print(f"   ✅ Successful: {len(successful_journeys)}")
        print(f"   ❌ Failed: {len(failed_journeys)}")
        print(f"   📊 Success Rate: {(len(successful_journeys)/len(self.results)*100):.1f}%")
        print(f"   ⏱️  Total Duration: {total_duration:.2f} seconds")
        
        if successful_journeys:
            print(f"\n✅ SUCCESSFUL JOURNEYS:")
            for journey in successful_journeys:
                duration = self.results[journey]["duration"]
                print(f"   🟢 {journey} ({duration:.2f}s)")
        
        if failed_journeys:
            print(f"\n❌ FAILED JOURNEYS:")
            for journey in failed_journeys:
                duration = self.results[journey]["duration"]
                error = self.results[journey].get("error", "Unknown error")
                print(f"   🔴 {journey} ({duration:.2f}s) - {error}")
        
        print(f"\n📁 Detailed logs available in: ~/automotas_tests/logs/")
        print("="*60)
        
        # Log the summary
        self.logger.log_journey_end(
            "completed" if len(failed_journeys) == 0 else "completed_with_failures",
            {
                "total_journeys": len(self.results),
                "successful_journeys": len(successful_journeys),
                "failed_journeys": len(failed_journeys),
                "success_rate": f"{(len(successful_journeys)/len(self.results)*100):.1f}%",
                "total_duration": total_duration
            }
        )


def main():
    """Main entry point"""
    
    parser = argparse.ArgumentParser(description="Automotas AI Journey Test Runner")
    parser.add_argument(
        "journey", 
        nargs="?", 
        help="Specific journey to run (use 'list' to see available journeys, 'all' to run all)"
    )
    parser.add_argument(
        "--list", 
        action="store_true", 
        help="List available journey tests"
    )
    
    args = parser.parse_args()
    
    runner = JourneyTestRunner()
    
    # Handle command line arguments
    if args.list or args.journey == "list":
        runner.list_available_journeys()
        return 0
    
    if args.journey == "all":
        # Run all journeys
        runner.run_all_journeys()
        runner.generate_summary_report()
        
        # Return appropriate exit code
        failed_count = len([r for r in runner.results.values() if not r["success"]])
        return 1 if failed_count > 0 else 0
    
    elif args.journey:
        # Run specific journey
        success = runner.run_journey(args.journey)
        runner.generate_summary_report()
        return 0 if success else 1
    
    else:
        # No arguments provided, show help
        print("🤖 Automotas AI Journey Test Runner")
        print("\nUsage:")
        print("  python run_journey_tests.py list                    # List available journeys")
        print("  python run_journey_tests.py all                     # Run all journeys")
        print("  python run_journey_tests.py agent_management        # Run specific journey")
        print()
        
        runner.list_available_journeys()
        return 0


if __name__ == "__main__":
    exit(main())