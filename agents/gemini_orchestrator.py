"""
Yuki Multi-Agent Orchestrator
Gemini 3 Pro-powered agent orchestration for anime character processing
Inspired by Claude's sub-agent delegation pattern
"""

import os
import json
import asyncio
from typing import List, Dict, Optional
from pathlib import Path
from google import genai
from google.genai import types
from dataclasses import dataclass, asdict
import datetime

# Configuration
PROJECT_ID = "gifted-cooler-479623-r7"
ORCHESTRATOR_MODEL = "gemini-3-pro-preview"  # The "Opus equivalent"
WORKER_MODEL = "gemini-2.5-flash"  # The "Haiku equivalent" for sub-agents
LOCATION = "global"

@dataclass
class SubAgentTask:
    """Represents a task delegated to a sub-agent"""
    task_id: str
    task_type: str  # 'scrape', 'extract_schema', 'generate_cosplay', 'test'
    instructions: str
    context: Dict
    status: str = "pending"  # pending, running, completed, failed
    result: Optional[Dict] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    worker_model: str = WORKER_MODEL

@dataclass
class OrchestratorSession:
    """Tracks an orchestration session"""
    session_id: str
    objective: str
    total_tasks: int
    completed_tasks: int = 0
    failed_tasks: int = 0
    tasks: List[SubAgentTask] = None
    started_at: str = None
    completed_at: Optional[str] = None
    
    def __post_init__(self):
        if self.tasks is None:
            self.tasks = []
        if self.started_at is None:
            self.started_at = datetime.datetime.now().isoformat()

class GeminiOrchestrator:
    """
    Multi-agent orchestrator using Gemini 3 Pro Preview
    Delegates work to sub-agents (Gemini 2.5 Flash)
    
    Pattern: User → Orchestrator → N Sub-Agents → Orchestrator → User
    """
    
    def __init__(self):
        self.client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
        self.sessions_dir = Path("c:/Yuki_Local/orchestration_sessions")
        self.sessions_dir.mkdir(exist_ok=True)
        self.active_session: Optional[OrchestratorSession] = None
    
    def create_orchestration_plan(self, objective: str, context: Dict) -> OrchestratorSession:
        """
        Use Gemini 3 to create a plan for accomplishing an objective
        This is like Claude's delegation capability
        """
        print(f"\n[🧠 ORCHESTRATOR] Planning: {objective}")
        
        planning_prompt = f"""
        You are an orchestration agent using Gemini 3 Pro Preview.
        
        OBJECTIVE:
        {objective}
        
        CONTEXT:
        {json.dumps(context, indent=2)}
        
        TASK:
        Break this objective down into discrete sub-tasks that can be parallelized.
        Each sub-task should be:
        1. Independent (can run in parallel)
        2. Well-defined (clear success criteria)
        3. Delegatable (can be done by a sub-agent)
        
        Output a JSON array of tasks with this structure:
        {{
            "tasks": [
                {{
                    "task_id": "unique_id",
                    "task_type": "scrape|extract_schema|generate_cosplay|test",
                    "instructions": "Detailed instructions for the sub-agent",
                    "context": {{...relevant data...}}
                }}
            ]
        }}
        
        Optimize for parallel execution. Maximum 10 sub-agents.
        """
        
        response = self.client.models.generate_content(
            model=ORCHESTRATOR_MODEL,
            contents=planning_prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.3  # Low temp for structured planning
            )
        )
        
        plan_data = json.loads(response.text)
        
        # Create session
        session = OrchestratorSession(
            session_id=datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
            objective=objective,
            total_tasks=len(plan_data["tasks"])
        )
        
        # Create sub-agent tasks
        for task_data in plan_data["tasks"]:
            task = SubAgentTask(**task_data)
            session.tasks.append(task)
        
        self.active_session = session
        self._save_session(session)
        
        print(f"  ✓ Created plan with {session.total_tasks} sub-tasks")
        return session
    
    async def execute_sub_agent_task(self, task: SubAgentTask) -> Dict:
        """
        Execute a single sub-agent task
        Sub-agents use Gemini 2.5 Flash for speed
        """
        print(f"\n  [⚡ SUB-AGENT {task.task_id}] Starting: {task.task_type}")
        
        task.status = "running"
        task.started_at = datetime.datetime.now().isoformat()
        
        try:
            # Sub-agent prompt (prompted BY the orchestrator, not by the user)
            sub_agent_prompt = f"""
            You are a sub-agent working for an orchestrator.
            
            TASK TYPE: {task.task_type}
            TASK ID: {task.task_id}
            
            INSTRUCTIONS:
            {task.instructions}
            
            CONTEXT:
            {json.dumps(task.context, indent=2)}
            
            Execute this task and return results in JSON format.
            Be precise and thorough.
            """
            
            # Use the appropriate location for the worker model
            worker_location = "us-central1" if "2.5" in task.worker_model else "global"
            worker_client = genai.Client(vertexai=True, project=PROJECT_ID, location=worker_location)
            
            response = worker_client.models.generate_content(
                model=task.worker_model,
                contents=sub_agent_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            result = json.loads(response.text)
            
            task.status = "completed"
            task.result = result
            task.completed_at = datetime.datetime.now().isoformat()
            
            print(f"  [✓ SUB-AGENT {task.task_id}] Completed")
            return result
            
        except Exception as e:
            task.status = "failed"
            task.result = {"error": str(e)}
            task.completed_at = datetime.datetime.now().isoformat()
            print(f"  [❌ SUB-AGENT {task.task_id}] Failed: {e}")
            return {"error": str(e)}
    
    async def execute_plan_parallel(self, session: OrchestratorSession) -> Dict:
        """
        Execute all sub-agent tasks in parallel
        This is the "scale compute to scale impact" pattern
        """
        print(f"\n[🔄 ORCHESTRATOR] Executing {session.total_tasks} sub-agents in parallel...")
        
        # Execute all tasks concurrently
        tasks = [self.execute_sub_agent_task(task) for task in session.tasks]
        results = await asyncio.gather(*tasks)
        
        # Update session stats
        session.completed_tasks = sum(1 for t in session.tasks if t.status == "completed")
        session.failed_tasks = sum(1 for t in session.tasks if t.status == "failed")
        session.completed_at = datetime.datetime.now().isoformat()
        
        self._save_session(session)
        
        print(f"\n[✅ ORCHESTRATOR] Completed {session.completed_tasks}/{session.total_tasks} tasks")
        print(f"  Failed: {session.failed_tasks}")
        
        return {
            "session_id": session.session_id,
            "total_tasks": session.total_tasks,
            "completed": session.completed_tasks,
            "failed": session.failed_tasks,
            "results": results
        }
    
    def synthesize_results(self, session: OrchestratorSession) -> str:
        """
        Use Gemini 3 to synthesize sub-agent results into a final response
        """
        print(f"\n[🧠 ORCHESTRATOR] Synthesizing results...")
        
        synthesis_prompt = f"""
        You are an orchestration agent using Gemini 3 Pro Preview.
        
        ORIGINAL OBJECTIVE:
        {session.objective}
        
        SUB-AGENT RESULTS:
        {json.dumps([asdict(t) for t in session.tasks], indent=2)}
        
        TASK:
        Synthesize these sub-agent results into a cohesive response for the user.
        Highlight:
        1. What was accomplished
        2. Key findings or outputs
        3. Any failures or issues
        4. Next recommended steps
        
        Be concise but comprehensive.
        """
        
        response = self.client.models.generate_content(
            model=ORCHESTRATOR_MODEL,
            contents=synthesis_prompt
        )
        
        return response.text
    
    def _save_session(self, session: OrchestratorSession):
        """Save orchestration session to disk"""
        session_file = self.sessions_dir / f"{session.session_id}.json"
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(session), f, indent=2)

# =============================================================================
# HIGH-LEVEL ORCHESTRATION FUNCTIONS
# =============================================================================

async def orchestrate_character_extraction(
    character_names: List[str],
    anime_database_path: str = "c:/Yuki_Local/anime_database.json"
) -> Dict:
    """
    Orchestrate face schema extraction for multiple characters in parallel
    
    Pattern:
    User → Orchestrator (Gemini 3) → N Sub-Agents (Gemini 2.5 Flash) → Results
    """
    orchestrator = GeminiOrchestrator()
    
    # Create plan
    session = orchestrator.create_orchestration_plan(
        objective=f"Extract face schemas for {len(character_names)} anime characters",
        context={
            "character_names": character_names,
            "database_path": anime_database_path,
            "operation": "face_schema_extraction"
        }
    )
    
    # Execute in parallel
    results = await orchestrator.execute_plan_parallel(session)
    
    # Synthesize
    summary = orchestrator.synthesize_results(session)
    
    return {
        "session": session,
        "results": results,
        "summary": summary
    }

async def orchestrate_batch_cosplay_generation(
    source_character_ids: List[str],
    target_characters: List[str],
    source_image_path: str
) -> Dict:
    """
    Orchestrate batch cosplay generation
    Each sub-agent handles one source→target pair
    """
    orchestrator = GeminiOrchestrator()
    
    session = orchestrator.create_orchestration_plan(
        objective=f"Generate {len(source_character_ids) * len(target_characters)} cosplay variations",
        context={
            "source_character_ids": source_character_ids,
            "target_characters": target_characters,
            "source_image_path": source_image_path,
            "operation": "batch_cosplay_generation"
        }
    )
    
    results = await orchestrator.execute_plan_parallel(session)
    summary = orchestrator.synthesize_results(session)
    
    return {
        "session": session,
        "results": results,
        "summary": summary
    }

# =============================================================================
# CLI INTERFACE
# =============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("""
        Yuki Multi-Agent Orchestrator
        
        Usage:
            python gemini_orchestrator.py extract Edward,Alphonse,Roy
            python gemini_orchestrator.py cosplay char_001,char_002 Dante,Cloud path.png
        """)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "extract":
        characters = sys.argv[2].split(",")
        result = asyncio.run(orchestrate_character_extraction(characters))
        print(f"\n{result['summary']}")
    
    elif command == "cosplay":
        sources = sys.argv[2].split(",")
        targets = sys.argv[3].split(",")
        image = sys.argv[4]
        result = asyncio.run(orchestrate_batch_cosplay_generation(sources, targets, image))
        print(f"\n{result['summary']}")
