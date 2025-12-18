"""
Yuki Orchestrator - Agentic Workflow Engine
DO Framework: Directive → Orchestration → Execution

This is the brain that reads directives and autonomously executes workflows
using all available Yuki modules with self-healing capabilities.
"""

import asyncio
import json
import time
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Callable
from pathlib import Path
from enum import Enum
import traceback
import re

from google import genai
from google.genai import types


class WorkflowStatus(str, Enum):
    """Workflow execution status"""
    PENDING = "pending"
    RUNNING = "running"
    QUALITY_CHECK_FAILED = "quality_check_failed"
    RETRYING = "retrying"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ExecutionStep:
    """Single step in workflow execution"""
    step_number: int
    step_name: str
    status: WorkflowStatus
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    output: Any = None
    error: Optional[str] = None
    retries: int = 0
    max_retries: int = 2
    
    @property
    def duration(self) -> Optional[float]:
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None


@dataclass
class WorkflowExecution:
    """Complete workflow execution tracking"""
    workflow_id: str
    directive_path: str
    inputs: Dict[str, Any]
    steps: List[ExecutionStep] = field(default_factory=list)
    status: WorkflowStatus = WorkflowStatus.PENDING
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    total_cost: float = 0.0
    outputs: Dict[str, Any] = field(default_factory=dict)
    errors_encountered: List[str] = field(default_factory=list)
    
    @property
    def total_duration(self) -> Optional[float]:
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None


class YukiOrchestrator:
    """
    Autonomous workflow orchestrator with self-healing
    
    Reads directives, orchestrates execution, handles errors, retries failures
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        directives_dir: str = "directives",
        max_retries: int = 3,
        enable_self_healing: bool = True
    ):
        """
        Initialize orchestrator
        
        Args:
            api_key: Gemini API key
            directives_dir: Directory containing directive markdown files
            max_retries: Maximum retry attempts per step
            enable_self_healing: Enable automatic error recovery
        """
        self.client = genai.Client(api_key=api_key)
        self.directives_dir = Path(directives_dir)
        self.max_retries = max_retries
        self.enable_self_healing = enable_self_healing
        
        # Lazy-load modules to avoid import errors
        self._modules = {}
        
        # Execution history
        self.executions: List[WorkflowExecution] = []
        
        print("🦊 Yuki Orchestrator initialized")
        print(f"   Directives: {self.directives_dir.absolute()}")
        print(f"   Self-healing: {'✓' if enable_self_healing else '✗'}")
    
    def _load_module(self, module_name: str) -> Any:
        """Lazy-load modules only when needed"""
        if module_name in self._modules:
            return self._modules[module_name]
        
        try:
            if module_name == "gemini_image":
                from yuki_gemini_client import YukiGeminiImageClient
                self._modules[module_name] = YukiGeminiImageClient()
            elif module_name == "spatial":
                from yuki_spatial_analyzer import YukiSpatialAnalyzer
                self._modules[module_name] = YukiSpatialAnalyzer()
            elif module_name == "video_gen":
                from yuki_video_generator import YukiVideoGenerator
                self._modules[module_name] = YukiVideoGenerator()
            elif module_name == "video_analyze":
                from yuki_video_generator import YukiVideoAnalyzer
                self._modules[module_name] = YukiVideoAnalyzer()
            elif module_name == "knowledge":
                from yuki_knowledge_base import YukiKnowledgeBase
                self._modules[module_name] = YukiKnowledgeBase()
            elif module_name == "prompt_optimizer":
                from yuki_prompt_optimizer import YukiPromptOptimizer
                self._modules[module_name] = YukiPromptOptimizer()
            
            return self._modules.get(module_name)
        except ImportError as e:
            print(f"⚠️  Module {module_name} not available: {e}")
            return None
    
    async def execute_workflow(
        self,
        directive_name: str,
        inputs: Dict[str, Any]
    ) -> WorkflowExecution:
        """
        Execute a workflow from a directive
        
        Args:
            directive_name: Name of directive file (without .md)
            inputs: Input parameters for workflow
            
        Returns:
            WorkflowExecution with results and metrics
        """
        
        workflow_id = f"{directive_name}_{int(time.time())}"
        directive_path = self.directives_dir / f"{directive_name}.md"
        
        if not directive_path.exists():
            raise FileNotFoundError(f"Directive not found: {directive_path}")
        
        # Create execution tracker
        execution = WorkflowExecution(
            workflow_id=workflow_id,
            directive_path=str(directive_path),
            inputs=inputs,
            start_time=time.time()
        )
        
        print(f"\n{'='*60}")
        print(f"🚀 Starting Workflow: {directive_name}")
        print(f"{'='*60}\n")
        
        try:
            # Read directive
            directive_content = directive_path.read_text(encoding='utf-8')
            
            # Parse workflow steps
            steps = self._parse_directive_steps(directive_content)
            
            # Execute each step
            for i, step_info in enumerate(steps, 1):
                step = ExecutionStep(
                    step_number=i,
                    step_name=step_info['name'],
                    status=WorkflowStatus.PENDING
                )
                execution.steps.append(step)
                
                # Execute step with retries
                await self._execute_step_with_retry(
                    step,
                    step_info,
                    execution,
                    directive_content
                )
                
                # Check if step failed after retries
                if step.status == WorkflowStatus.FAILED:
                    execution.status = WorkflowStatus.FAILED
                    execution.errors_encountered.append(
                        f"Step {i} failed: {step.error}"
                    )
                    break
            
            # Mark as completed if no failures
            if execution.status != WorkflowStatus.FAILED:
                execution.status = WorkflowStatus.COMPLETED
        
        except Exception as e:
            execution.status = WorkflowStatus.FAILED
            execution.errors_encountered.append(f"Fatal error: {str(e)}")
            print(f"❌ Fatal error: {e}")
            traceback.print_exc()
        
        finally:
            execution.end_time = time.time()
            self.executions.append(execution)
            
            # Print summary
            self._print_execution_summary(execution)
        
        return execution
    
    async def _execute_step_with_retry(
        self,
        step: ExecutionStep,
        step_info: Dict[str, Any],
        execution: WorkflowExecution,
        directive_content: str
    ):
        """Execute a step with automatic retry on failure"""
        
        while step.retries <= step.max_retries:
            try:
                step.status = WorkflowStatus.RUNNING
                step.start_time = time.time()
                
                print(f"▶ Step {step.step_number}: {step.step_name}")
                if step.retries > 0:
                    print(f"  ↻ Retry {step.retries}/{step.max_retries}")
                
                # Execute the step
                result = await self._execute_step_logic(
                    step,
                    step_info,
                    execution,
                    directive_content
                )
                
                step.output = result
                step.end_time = time.time()
                step.status = WorkflowStatus.COMPLETED
                
                print(f"  ✓ Completed in {step.duration:.1f}s")
                break  # Success!
                
            except Exception as e:
                step.error = str(e)
                step.retries += 1
                
                print(f"  ✗ Error: {e}")
                
                if step.retries <= step.max_retries and self.enable_self_healing:
                    print(f"  🔧 Self-healing attempt {step.retries}...")
                    step.status = WorkflowStatus.RETRYING
                    await asyncio.sleep(2 ** step.retries)  # Exponential backoff
                else:
                    step.status = WorkflowStatus.FAILED
                    break
    
    async def _execute_step_logic(
        self,
        step: ExecutionStep,
        step_info: Dict[str, Any],
        execution: WorkflowExecution,
        directive_content: str
    ) -> Any:
        """
        Execute the actual logic of a step
        
        This uses Gemini to interpret the directive and execute it
        using available modules
        """
        
        # Build context from previous steps
        previous_outputs = {
            s.step_name: s.output 
            for s in execution.steps 
            if s.output is not None
        }
        
        # Ask Gemini to orchestrate this step
        orchestration_prompt = f"""
You are executing Step {step.step_number} of a workflow.

**Directive Context:**
{directive_content}

**Current Step:**
{step_info['name']}
{step_info.get('description', '')}

**Input Parameters:**
{json.dumps(execution.inputs, indent=2)}

**Previous Step Outputs:**
{json.dumps(previous_outputs, indent=2) if previous_outputs else "None (first step)"}

**Available Tools:**
- YukiGeminiImageClient: Image generation with multi-reference
- YukiSpatialAnalyzer: Object detection, color extraction, costume analysis
- YukiVideoGenerator: Video generation (Veo 3.1)
- YukiVideoAnalyzer: Video analysis and tutorial extraction
- YukiKnowledgeBase: RAG search for character/cosplay knowledge
- YukiPromptOptimizer: Advanced prompt engineering

**Task:**
Based on the directive and current step, return a JSON object with:
{{
  "action": "tool_name.method_name",
  "parameters": {{"param1": "value1", ...}},
  "expected_output": "description of what this produces",
  "quality_check": "how to validate success"
}}

If this is a research/search step, use knowledge_base or google_search.
If this is image generation, use gemini_image.
If this is analysis, use spatial_analyzer.

Be specific with parameters. Use actual values from inputs/previous outputs.
"""
        
        # Get orchestration decision from Gemini
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=orchestration_prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,  # Lower for consistent decisions
                response_mime_type="application/json"
            )
        )
        
        # Parse orchestration decision
        decision = json.loads(response.text)
        
        print(f"  → Action: {decision['action']}")
        
        # Execute the action
        result = await self._execute_action(decision, execution)
        
        # Validate with quality check if specified
        if decision.get('quality_check'):
            is_valid = await self._validate_output(result, decision['quality_check'])
            if not is_valid:
                raise ValueError(f"Quality check failed: {decision['quality_check']}")
        
        return result
    
    async def _execute_action(
        self,
        decision: Dict[str, Any],
        execution: WorkflowExecution
    ) -> Any:
        """Execute the actual tool action"""
        
        action = decision['action']
        params = decision.get('parameters', {})
        
        # Parse module and method
        if '.' in action:
            module_name, method_name = action.split('.', 1)
        else:
            raise ValueError(f"Invalid action format: {action}")
        
        # Load module
        module = self._load_module(module_name)
        if not module:
            raise ImportError(f"Module {module_name} not available")
        
        # Call method
        if not hasattr(module, method_name):
            raise AttributeError(f"{module_name} has no method {method_name}")
        
        method = getattr(module, method_name)
        
        # Execute
        if asyncio.iscoroutinefunction(method):
            result = await method(**params)
        else:
            result = method(**params)
        
        return result
    
    async def _validate_output(
        self,
        output: Any,
        quality_check: str
    ) -> bool:
        """Validate output meets quality criteria"""
        
        # Use Gemini to evaluate quality
        validation_prompt = f"""
Evaluate if this output meets the quality criteria.

**Output:**
{json.dumps(str(output)[:500], indent=2)}

**Quality Criteria:**
{quality_check}

Return JSON:
{{
  "passed": true/false,
  "reason": "explanation"
}}
"""
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=validation_prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        validation = json.loads(response.text)
        
        if not validation['passed']:
            print(f"  ⚠ Quality check failed: {validation['reason']}")
        
        return validation['passed']
    
    def _parse_directive_steps(self, directive_content: str) -> List[Dict[str, Any]]:
        """Parse workflow steps from directive markdown"""
        
        steps = []
        
        # Find all step headers (### N. Step Name)
        step_pattern = r'###\s+(\d+)\.\s+(.+?)(?=\n|$)'
        matches = re.finditer(step_pattern, directive_content)
        
        for match in matches:
            step_num = int(match.group(1))
            step_name = match.group(2).strip()
            
            # Extract description (everything until next ### or ---)
            start = match.end()
            next_section = directive_content.find('###', start)
            next_divider = directive_content.find('---', start)
            
            end = len(directive_content)
            if next_section > 0:
                end = min(end, next_section)
            if next_divider > 0:
                end = min(end, next_divider)
            
            description = directive_content[start:end].strip()
            
            steps.append({
                'number': step_num,
                'name': step_name,
                'description': description
            })
        
        return steps
    
    def _print_execution_summary(self, execution: WorkflowExecution):
        """Print execution summary"""
        
        print(f"\n{'='*60}")
        print(f"📊 Workflow Summary: {execution.workflow_id}")
        print(f"{'='*60}")
        print(f"Status: {execution.status.value.upper()}")
        print(f"Duration: {execution.total_duration:.1f}s" if execution.total_duration else "Duration: N/A")
        print(f"Cost: ${execution.total_cost:.2f}")
        print(f"\nSteps Completed: {sum(1 for s in execution.steps if s.status == WorkflowStatus.COMPLETED)}/{len(execution.steps)}")
        
        for step in execution.steps:
            status_icon = {
                WorkflowStatus.COMPLETED: "✓",
                WorkflowStatus.FAILED: "✗",
                WorkflowStatus.RETRYING: "↻",
                WorkflowStatus.RUNNING: "▶",
                WorkflowStatus.PENDING: "○"
            }.get(step.status, "?")
            
            retry_info = f" ({step.retries} retries)" if step.retries > 0 else ""
            duration_info = f" - {step.duration:.1f}s" if step.duration else ""
            
            print(f"  {status_icon} Step {step.step_number}: {step.step_name}{retry_info}{duration_info}")
        
        if execution.errors_encountered:
            print(f"\n⚠️  Errors:")
            for error in execution.errors_encountered:
                print(f"  - {error}")
        
        print(f"{'='*60}\n")
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """Get statistics across all executions"""
        
        if not self.executions:
            return {"total_executions": 0}
        
        completed = [e for e in self.executions if e.status == WorkflowStatus.COMPLETED]
        failed = [e for e in self.executions if e.status == WorkflowStatus.FAILED]
        
        total_cost = sum(e.total_cost for e in self.executions)
        avg_duration = sum(e.total_duration or 0 for e in self.executions) / len(self.executions)
        
        return {
            "total_executions": len(self.executions),
            "completed": len(completed),
            "failed": len(failed),
            "success_rate": len(completed) / len(self.executions) * 100,
            "total_cost": total_cost,
            "avg_duration_seconds": avg_duration,
            "total_retries": sum(
                sum(s.retries for s in e.steps) 
                for e in self.executions
            )
        }


# Example usage
async def demo():
    """Demonstrate orchestrator"""
    print("🦊 Yuki Orchestrator Demo\n")
    
    orchestrator = YukiOrchestrator(
        api_key="YOUR_API_KEY",
        enable_self_healing=True
    )
    
    # Execute cosplay preview workflow
    execution = await orchestrator.execute_workflow(
        directive_name="cosplay_preview_generation",
        inputs={
            "character_name": "Makima",
            "anime_title": "Chainsaw Man",
            "user_selfie_path": "path/to/selfie.jpg"
        }
    )
    
    # Get stats
    stats = orchestrator.get_execution_stats()
    print(f"\n📈 Orchestrator Stats:")
    print(f"   Success Rate: {stats['success_rate']:.1f}%")
    print(f"   Total Cost: ${stats['total_cost']:.2f}")
    print(f"   Avg Duration: {stats['avg_duration_seconds']:.1f}s")


if __name__ == "__main__":
    asyncio.run(demo())
