"""
Yuki Stress Test Suite
Rigorously tests the Yuki Orchestrator and Modules for stability, concurrency, and self-healing.

Features:
- Concurrent Workflow Execution: Run multiple workflows in parallel.
- Mock Mode: Simulate API calls to test orchestration logic without cost.
- Chaos Mode: Randomly inject failures to test self-healing.
- Performance Metrics: Track success rate, recovery time, and latency.
"""

import asyncio
import random
import time
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any
from pathlib import Path

# Import Yuki components
from yuki_orchestrator import YukiOrchestrator, WorkflowStatus, WorkflowExecution

@dataclass
class TestResult:
    workflow_id: str
    status: str
    duration: float
    retries: int
    errors: List[str]
    mode: str

class MockModule:
    """Simulates a Yuki module with artificial delays and errors"""
    
    def __init__(self, name: str, failure_rate: float = 0.0):
        self.name = name
        self.failure_rate = failure_rate
    
    async def execute(self, method: str, **kwargs):
        # Simulate processing time
        await asyncio.sleep(random.uniform(0.5, 2.0))
        
        # Simulate random failure
        if random.random() < self.failure_rate:
            raise RuntimeError(f"Simulated failure in {self.name}.{method}")
        
        return f"Mock output from {self.name}.{method}"

class StressTestRunner:
    def __init__(self, orchestrator: YukiOrchestrator):
        self.orchestrator = orchestrator
        self.results: List[TestResult] = []
        
    async def run_mock_workflow(self, test_id: int, chaos_rate: float = 0.0):
        """
        Runs a workflow using mocked tools to test orchestration logic.
        We inject a custom 'Mock' module into the orchestrator for this test.
        """
        workflow_id = f"mock_test_{test_id}"
        
        # Monkey patch the orchestrator's _load_module and _execute_action for this test
        
        original_execute_action = self.orchestrator._execute_action
        original_generate_content = self.orchestrator.client.models.generate_content
        
        async def mock_execute_action(decision, execution):
            action = decision['action']
            if random.random() < chaos_rate:
                # print(f"  🔥 Chaos Monkey struck {action}!")
                raise RuntimeError(f"Chaos Monkey error in {action}")
            
            await asyncio.sleep(random.uniform(0.1, 0.5))
            return {"mock_result": f"Success from {action}", "data": "dummy_data"}

        def mock_generate_content(*args, **kwargs):
            # Return a mock response object with a .text attribute containing JSON
            class MockResponse:
                text = json.dumps({
                    "action": "gemini_image.generate_image",
                    "parameters": {"prompt": "test prompt"},
                    "expected_output": "A test image",
                    "quality_check": "Check if image exists"
                })
            return MockResponse()

        # Temporarily replace the methods
        self.orchestrator._execute_action = mock_execute_action
        self.orchestrator.client.models.generate_content = mock_generate_content
        
        try:
            # We need a dummy directive for the mock test
            inputs = {"character_name": f"MockChar_{test_id}", "anime": "TestAnime"}
            
            execution = await self.orchestrator.execute_workflow(
                directive_name="cosplay_preview_generation",
                inputs=inputs
            )
            
            self.results.append(TestResult(
                workflow_id=execution.workflow_id,
                status=execution.status.value,
                duration=execution.total_duration or 0,
                retries=sum(sum(s.retries for s in e.steps) for e in [execution]), # Flatten retries
                errors=execution.errors_encountered,
                mode="Mock"
            ))
            
        finally:
            # Restore original methods
            self.orchestrator._execute_action = original_execute_action
            self.orchestrator.client.models.generate_content = original_generate_content

    async def run_stress_test(self, num_workflows: int = 10, concurrency: int = 5, chaos_rate: float = 0.1):
        """Run multiple workflows with concurrency"""
        print(f"\n🌪️ STARTING STRESS TEST")
        print(f"   Workflows: {num_workflows}")
        print(f"   Concurrency: {concurrency}")
        print(f"   Chaos Rate: {chaos_rate*100}%")
        
        start_time = time.time()
        semaphore = asyncio.Semaphore(concurrency)
        
        async def bounded_test(i):
            async with semaphore:
                print(f"Starting test {i+1}/{num_workflows}...")
                await self.run_mock_workflow(i, chaos_rate)
        
        tasks = [bounded_test(i) for i in range(num_workflows)]
        await asyncio.gather(*tasks)
        
        total_time = time.time() - start_time
        self._print_report(total_time)

    def _print_report(self, total_time: float):
        print(f"\n{'='*60}")
        print(f"📊 STRESS TEST REPORT")
        print(f"{'='*60}")
        
        total = len(self.results)
        passed = len([r for r in self.results if r.status == "completed"])
        failed = len([r for r in self.results if r.status == "failed"])
        total_retries = sum(r.retries for r in self.results)
        avg_duration = sum(r.duration for r in self.results) / total if total > 0 else 0
        
        print(f"Total Workflows: {total}")
        print(f"Passed: {passed} ({passed/total*100:.1f}%)")
        print(f"Failed: {failed} ({failed/total*100:.1f}%)")
        print(f"Total Retries (Self-Healing): {total_retries}")
        print(f"Avg Duration: {avg_duration:.2f}s")
        print(f"Total Test Time: {total_time:.2f}s")
        print(f"{'='*60}")
        
        if failed > 0:
            print("\nErrors Encountered:")
            for r in self.results:
                if r.status == "failed":
                    print(f"  - {r.workflow_id}: {r.errors}")

# Entry point
async def main():
    # Initialize orchestrator
    orchestrator = YukiOrchestrator(
        api_key="DUMMY_KEY_FOR_MOCK", # Key not used in mock mode
        enable_self_healing=True
    )
    
    runner = StressTestRunner(orchestrator)
    
    # Run a small batch first to warm up
    print("🔥 Warming up...")
    await runner.run_stress_test(num_workflows=2, concurrency=1, chaos_rate=0.0)
    
    # Run the main stress test with chaos
    print("\n🚀 Running Main Stress Test...")
    # 20 workflows, 5 concurrent, 20% chance of random failure per step
    await runner.run_stress_test(num_workflows=20, concurrency=5, chaos_rate=0.2)

if __name__ == "__main__":
    asyncio.run(main())
