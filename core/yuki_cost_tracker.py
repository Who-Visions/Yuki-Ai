"""
Yuki Cost Tracker Integration
Monitors image generation costs using Who Visions LLC contract pricing

NOTE: Yuki and Unk have SEPARATE project IDs but SHARE the billing account
- Yuki Project: gifted-cooler-479623-r7
- Unk Project: Different project ID
- Billing: Same billing account (all costs pool together)
- Quotas: Separate per project
"""

import logging
from datetime import datetime
from pathlib import Path
import json

logger = logging.getLogger("YukiCostTracker")

class YukiCostTracker:
    """
    Tracks Yuki's image generation costs
    Uses Who Visions LLC contract pricing (shared with Unk via billing account)
    """
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.cost_log_path = Path("data/yuki_costs.json")
        self.cost_log_path.parent.mkdir(exist_ok=True)
        
        # OFFICIAL GEMINI 3 PRICING (December 2025)
        self.pricing = {
            "gemini_3_flash": {
                "input_per_1m": 0.50,           # $0.50/1M (text/image/video)
                "input_audio_per_1m": 1.00,     # $1.00/1M (audio)
                "output_per_1m": 3.00,          # $3.00/1M (includes thinking)
                "caching_input_per_1m": 0.05,
                "cache_storage_per_1m_hr": 1.00,
                "service": "Vertex AI"
            },
            "gemini_3_pro": {
                "input_per_1m": 2.00,            # $2.00/1M (<200k)
                "input_per_1m_long": 4.00,       # $4.00/1M (>200k)
                "output_per_1m": 12.00,          # $12.00/1M (<200k)
                "output_per_1m_long": 18.00,     # $18.00/1M (>200k)
                "caching_input_per_1m": 0.20,
                "caching_input_per_1m_long": 0.40,
                "cache_storage_per_1m_hr": 4.50,
                "service": "Vertex AI"
            },
            "gemini_3_pro_image": {
                "text_input_per_1m": 2.00,
                "image_input_per_image": 0.0011,  # ~560 tokens
                "text_output_per_1m": 12.00,
                "image_output_1k_2k": 0.134,     # 1K/2K images
                "image_output_4k": 0.24,         # 4K images
                "service": "Vertex AI"
            },
            "imagen_3": {
                "generation_per_image": 0.04,
                "service": "Vertex AI"
            },
            "imagen_4": {
                "generation_per_image": 0.04,
                "service": "Vertex AI"
            }
        }
    
    def log_generation(self, 
                       model: str, 
                       operation: str,
                       count: int = 1,
                       tokens_in: int = 0,
                       tokens_out: int = 0,
                       thoughts_tokens: int = 0,
                       metadata: dict = None):
        """
        Log a generation operation and its cost
        """
        timestamp = datetime.now().isoformat()
        
        tokens_in = tokens_in or 0
        tokens_out = tokens_out or 0
        thoughts_tokens = thoughts_tokens or 0
        
        # Calculate cost
        cost = 0.0
        model_key = model.lower().replace("-", "_").replace("preview", "").rstrip("_")
        if "flash" in model_key:
            p = self.pricing.get("gemini_3_flash", {})
            total_output = tokens_out + thoughts_tokens
            cost = (tokens_in / 1_000_000 * p.get("input_per_1m", 0) +
                   total_output / 1_000_000 * p.get("output_per_1m", 0))
        elif "image" in model_key:
            p = self.pricing.get("gemini_3_pro_image", {})
            cost = count * p.get("image_output", 0.134) + (tokens_in / 1_000_000 * p.get("text_input_per_1m", 0))
        elif "pro" in model_key:
            p = self.pricing.get("gemini_3_pro", {})
            total_output = tokens_out + thoughts_tokens
            cost = (tokens_in / 1_000_000 * p.get("input_per_1m", 0) +
                   total_output / 1_000_000 * p.get("output_per_1m", 0))
        
        entry = {
            "timestamp": timestamp,
            "project_id": self.project_id,
            "model": model,
            "operation": operation,
            "count": count,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "thoughts_tokens": thoughts_tokens,
            "cost_usd": round(cost, 6),
            "metadata": metadata or {}
        }
        
        # Load existing
        if self.cost_log_path.exists():
            with open(self.cost_log_path, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(entry)
        
        # Save
        with open(self.cost_log_path, 'w') as f:
            json.dump(logs, f, indent=2)
        
        logger.info(f"💰 Cost logged: ${cost:.6f} ({operation})")
        return cost
    
    def get_session_cost(self, hours: int = 24) -> dict:
        """Get total cost for recent session"""
        if not self.cost_log_path.exists():
            return {"total_cost": 0.0, "operations": 0}
        
        with open(self.cost_log_path, 'r') as f:
            logs = json.load(f)
        
        # Filter by time
        cutoff = datetime.now().timestamp() - (hours * 3600)
        recent = [l for l in logs if datetime.fromisoformat(l['timestamp']).timestamp() > cutoff]
        
        total_cost = sum(l['cost_usd'] for l in recent)
        
        return {
            "total_cost": round(total_cost, 6),
            "operations": len(recent),
            "breakdown": {
                "analysis": sum(l['cost_usd'] for l in recent if l['operation'] == 'analysis'),
                "generation": sum(l['cost_usd'] for l in recent if l['operation'] == 'generation')
            }
        }
    
    def get_total_cost(self) -> float:
        """Get all-time total cost"""
        if not self.cost_log_path.exists():
            return 0.0
        
        with open(self.cost_log_path, 'r') as f:
            logs = json.load(f)
        
        return round(sum(l['cost_usd'] for l in logs), 6)
    
    def check_quota_usage(self, warn_threshold: float = 10.0) -> dict:
        """
        Check if we're approaching quota limits
        """
        session_cost = self.get_session_cost(hours=1)  # Last hour
        total_cost = self.get_total_cost()
        
        status = {
            "last_hour_cost": session_cost['total_cost'],
            "total_cost": total_cost,
            "warning": session_cost['total_cost'] > warn_threshold,
            "message": "OK"
        }
        
        if status['warning']:
            status['message'] = f"⚠️ High usage: ${session_cost['total_cost']:.2f} in last hour"
        
        return status


# Integration example
def track_batch_generation(tracker: YukiCostTracker, 
                          analysis_model: str,
                          generation_model: str,
                          image_count: int,
                          analysis_tokens: int):
    """
    Track costs for a batch generation
    """
    # Log analysis cost
    analysis_cost = tracker.log_generation(
        model=analysis_model,
        operation="analysis",
        tokens_in=analysis_tokens,
        metadata={"batch_size": image_count}
    )
    
    # Log generation cost
    gen_cost = tracker.log_generation(
        model=generation_model,
        operation="generation",
        count=image_count,
        metadata={"batch_size": image_count}
    )
    
    total = analysis_cost + gen_cost
    logger.info(f"📊 Batch cost: ${total:.6f} (Analysis: ${analysis_cost:.6f}, Generation: ${gen_cost:.6f})")
    
    return total


if __name__ == "__main__":
    # Test
    tracker = YukiCostTracker(project_id="gifted-cooler-479623-r7")
    
    # Simulate Jesse's 10-image batch
    track_batch_generation(
        tracker=tracker,
        analysis_model="gemini-3-flash-preview",
        generation_model="gemini-3-pro-image-preview",
        image_count=10,
        analysis_tokens=5000
    )
    
    # Check session cost
    session = tracker.get_session_cost(hours=24)
    print(f"\n💰 Session Cost: ${session['total_cost']:.6f}")
    print(f"   Operations: {session['operations']}")
    print(f"   Analysis: ${session['breakdown']['analysis']:.6f}")
    print(f"   Generation: ${session['breakdown']['generation']:.6f}")
    
    # Check quota
    quota = tracker.check_quota_usage()
    print(f"\n📊 Quota Status: {quota['message']}")
