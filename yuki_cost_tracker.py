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
        
        # ACTUAL CONTRACT PRICING (from GCP CSV - December 2025)
        # ⚠️ Previous estimates were 3x TOO LOW!
        self.pricing = {
            "gemini_2.5_flash": {
                "input_per_1m": 0.30,          # $0.30 per 1M tokens (was $0.10 - 3x correction!)
                "output_per_1m": 2.50,         # $2.50 per 1M tokens with thinking (was $0.40 - 6x!)
                "output_regular_per_1m": 0.40, # Estimated regular output (no contract data)
                "caching_input_per_1m": 0.03,  # 90% discount on cached input
                "image_input_per_1m": 0.30,    # $0.30 per 1M images
                "service": "Vertex AI",
                "sku_input": "FDAB-647C-5A22",
                "sku_output_thinking": "A253-E8A3-DE5C"
            },
            "gemini_2.5_pro": {
                "input_per_1m": 1.25,          # $1.25 per 1M tokens
                "output_per_1m": 10.00,        # $10.00 per 1M tokens
                "caching_input_per_1m": 0.125, # 90% discount on cached input
                "image_input_per_1m": 1.25,    # $1.25 per 1M images
                "image_caching_per_1m": 0.125, # $0.125 per 1M cached images
                "service": "Vertex AI",
                "sku_input": "A121-E2B5-1418",
                "sku_output": "5DA2-3F77-1CA5"
            },
            "gemini_3_pro_image": {
                "image_output_per_1m": 120.00, # $120 per 1M images ($0.12 per image)
                "image_input_per_1m": 2.00,    # $2.00 per 1M images
                "text_input_per_1m": 2.00,     # $2.00 per 1M tokens
                "text_output_per_1m": 12.00,   # $12.00 per 1M tokens
                "service": "Vertex AI",
                "sku_image_output": "47A8-A5A1-B26C",
                "sku_text_input": "EAC4-305F-1249"
            },
            "imagen_3": {
                "generation_per_image": 0.04,  # $0.04 per image
                "service": "Vertex AI",
                "sku": "B5BE-136B-2CA1"
            },
            "imagen_4": {
                "generation_per_image": 0.04,  # $0.04 per image  
                "service": "Vertex AI",
                "sku": "180A-C24F-9D7F"
            }
        }
    
    def log_generation(self, 
                       model: str, 
                       operation: str,
                       count: int = 1,
                       tokens_in: int = 0,
                       tokens_out: int = 0,
                       metadata: dict = None):
        """
        Log a generation operation and its cost
        """
        timestamp = datetime.now().isoformat()
        
        # Calculate cost
        cost = 0.0
        if "flash" in model.lower():
            cost = (tokens_in / 1_000_000 * self.pricing["gemini_2.5_flash"]["input_per_1m"] +
                   tokens_out / 1_000_000 * self.pricing["gemini_2.5_flash"]["output_per_1m"])
        elif "image" in model.lower() or "pro" in model.lower():
            cost = count * self.pricing["gemini_3_pro_image"]["image_gen"]
        
        entry = {
            "timestamp": timestamp,
            "project_id": self.project_id,
            "model": model,
            "operation": operation,
            "count": count,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
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
        analysis_model="gemini-2.5-flash",
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
