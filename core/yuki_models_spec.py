"""
YUKI MODELS Specification (CORRECTED CONTRACT PRICING)
======================================================
Based on Who Visions LLC GCP Contract CSV (December 2025)

⚠️ NOTE: This pricing DIFFERS from Unk's models_spec.py
Unk's pricing is outdated - this uses actual contract values
"""

from typing import Dict, Any

# CORRECTED PRICING from Who Visions LLC Contract CSV
YUKI_MODELS: Dict[str, Dict[str, Any]] = {
    "gemini_3_flash": {
        "model_id": "gemini-3-flash-preview",
        "tier": "flash",
        "context_window": 1_048_576,
        "max_output_tokens": 65_536,
        "capabilities": ["multimodal", "tools", "fast", "thinking_tokens"],
        "pricing": {
            # Official Gemini 3 Pricing (Dec 2025)
            "input_per_1m": 0.50,           # $0.50/1M (text/image/video)
            "input_audio_per_1m": 1.00,     # $1.00/1M (audio)
            "output_per_1m": 3.00,          # $3.00/1M (includes thinking)
            "caching_input_per_1m": 0.05,   # $0.05/1M (text/image/video)
            "caching_audio_per_1m": 0.10,   # $0.10/1M (audio)
            "cache_storage_per_1m_hr": 1.00 # $1.00/1M tokens per hour
        },
        "rate_limits": {
            "rpm": 2000,
            "tpm": 4_000_000,
            # Batch API enqueued token limits by tier
            "batch_tokens_tier1": 3_000_000,
            "batch_tokens_tier2": 400_000_000,
            "batch_tokens_tier3": 500_000_000
        },
        "description": "Pro-level intelligence at Flash speed and pricing.",
        "use_cases": ["perspective_analysis", "facial_analysis", "image_understanding"]
    },
    
    "gemini_3_pro": {
        "model_id": "gemini-3-pro-preview",
        "tier": "pro",
        "context_window": 1_048_576,
        "max_output_tokens": 65_536,
        "capabilities": ["complex_reasoning", "coding", "thinking_tokens", "multimodal"],
        "pricing": {
            # Official Gemini 3 Pricing (Dec 2025) - tiered
            "input_per_1m": 2.00,       # $2.00/1M tokens (<200k)
            "input_per_1m_long": 4.00,  # $4.00/1M tokens (>200k)
            "output_per_1m": 12.00,     # $12.00/1M tokens (<200k)
            "output_per_1m_long": 18.00, # $18.00/1M tokens (>200k)
            "caching_input_per_1m": 0.20    # 90% discount
        },
        "rate_limits": {
            "rpm": 150,
            "tpm": 1_000_000,
            # Batch API enqueued token limits by tier
            "batch_tokens_tier1": 50_000_000,
            "batch_tokens_tier2": 500_000_000,
            "batch_tokens_tier3": 1_000_000_000
        },
        "description": "Best for complex tasks requiring broad world knowledge and advanced reasoning.",
        "use_cases": ["complex_analysis", "research"]
    },
    
    "gemini_3_pro_image": {
        "model_id": "gemini-3-pro-image-preview",
        "tier": "pro",
        "location": "global",
        "context_window": 65_536,          # 65k input tokens
        "max_output_tokens": 32_768,       # 32k output tokens
        "capabilities": ["image_generation", "thinking", "search_grounding", "structured_outputs"],
        "pricing": {
            # Official Gemini 3 Pricing (Dec 2025)
            "text_input_per_1m": 2.00,      # $2.00/1M tokens
            "image_input_per_image": 0.0011, # ~560 tokens per image
            "text_output_per_1m": 12.00,    # $12.00/1M (text + thinking)
            "image_output_1k_2k": 0.134,    # $0.134 per 1K/2K image (1120 tokens)
            "image_output_4k": 0.24,        # $0.24 per 4K image (2000 tokens)
        },
        "rate_limits": {
            "rpm": 60,
            "tpm": 500_000,
            # Batch API enqueued token limits by tier
            "batch_tokens_tier1": 2_000_000,
            "batch_tokens_tier2": 270_000_000,
            "batch_tokens_tier3": 1_000_000_000
        },
        "description": "Nano Banana Pro - highest quality image generation model.",
        "use_cases": ["character_transformation", "cosplay_generation"]
    },
    "imagen_3": {
        "model_id": "imagen-3.0-generate-001",
        "tier": "specialist",
        "location": "us-central1",
        "capabilities": ["image_generation"],
        "pricing": {
            # ⚠️ CONTRACT PRICING (CSV)
            "generation_per_image": 0.04  # $0.04/image (SKU: B5BE-136B-2CA1)
        },
        "rate_limits": {
            "rpm": 100
        },
        "description": "COST OPTIMIZED alternative. 67% cheaper than Gemini 3 Pro.",
        "use_cases": ["batch_generation", "cost_sensitive_tasks"]
    },
    
    "imagen_4": {
        "model_id": "imagen-4.0-generate-001",
        "tier": "specialist",
        "location": "us-central1",
        "capabilities": ["image_generation"],
        "pricing": {
            # ⚠️ CONTRACT PRICING (CSV)
            "generation_per_image": 0.04  # $0.04/image (SKU: 180A-C24F-9D7F)
        },
        "rate_limits": {
            "rpm": 100
        },
        "description": "COST OPTIMIZED alternative. 67% cheaper than Gemini 3 Pro.",
        "use_cases": ["batch_generation", "cost_sensitive_tasks"]
    }
}


# Utility functions
def get_model(mode: str) -> Dict[str, Any]:
    """Retrieve model spec."""
    return YUKI_MODELS.get(mode, YUKI_MODELS["gemini_3_flash"])


def estimate_cost(mode: str, input_tokens: int = 0, output_tokens: int = 0, images: int = 0) -> float:
    """
    Estimate cost using CONTRACT PRICING.
    
    Args:
        mode: Model mode key
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        images: Number of images (generation or input)
    """
    spec = get_model(mode)
    pricing = spec.get("pricing", {})
    
    total_cost = 0.0
    
    # Text tokens
    if input_tokens > 0:
        # Simplified: use low token pricing
        input_price = pricing.get("input_per_1m") or pricing.get("text_input_per_1m") or pricing.get("input_per_1m_low_tokens", 0)
        total_cost += (input_tokens / 1_000_000) * input_price
    
    if output_tokens > 0:
        output_price = pricing.get("output_per_1m") or pricing.get("text_output_per_1m") or pricing.get("output_per_1m_low_tokens", 0)
        total_cost += (output_tokens / 1_000_000) * output_price
    
    # Images
    if images > 0:
        # Check if this is a generation model
        if "generation_per_image" in pricing:
            total_cost += images * pricing["generation_per_image"]
        elif "image_output" in pricing:
            total_cost += images * pricing["image_output"]
        elif "image_input_per_1m" in pricing:
            total_cost += (images / 1_000_000) * pricing["image_input_per_1m"]
    
    return round(total_cost, 6)


def calculate_session_cost(analysis_tokens: int, num_images: int) -> Dict[str, float]:
    """
    Calculate typical Yuki session cost.
    
    Args:
        analysis_tokens: Tokens used for facial analysis (Gemini 2.5 Flash)
        num_images: Number of images generated (Gemini 3 Pro)
    """
    analysis_cost = estimate_cost("gemini_3_flash", input_tokens=analysis_tokens)
    generation_cost = estimate_cost("gemini_3_pro_image", images=num_images)
    
    # Calculate Imagen alternative cost
    imagen_cost = estimate_cost("imagen_3", images=num_images)
    savings = generation_cost - imagen_cost
    
    return {
        "analysis_cost": analysis_cost,
        "generation_cost": generation_cost,
        "total_cost": round(analysis_cost + generation_cost, 6),
        "cost_per_image": round((analysis_cost + generation_cost) / num_images, 6) if num_images > 0 else 0,
        "imagen_alternative": {
            "cost": imagen_cost,
            "savings": round(savings, 6),
            "savings_percentage": round((savings / generation_cost) * 100, 2) if generation_cost > 0 else 0
        }
    }


# PRICING COMPARISON with Unk's models_spec.py
PRICING_DISCREPANCIES = {
    "gemini_2.5_flash": {
        "unk_spec": {"input": 0.10, "output": 0.40},
        "contract_csv": {"input": 0.30, "output": 2.50},
        "difference": {
            "input": "+200%",
            "output": "+525%"
        },
        "note": "Unk's pricing is outdated. Contract pricing is 3-6x higher!"
    },
    "gemini_2.5_pro": {
        "unk_spec": {"input": 2.50, "output": 10.00},
        "contract_csv": {"input": 1.25, "output": 10.00},
        "difference": {
            "input": "-50% (Unk spec is 2x TOO HIGH)",
            "output": "MATCH ✅"
        },
        "note": "Unk's input pricing is 2x higher than contract. Output matches."
    }
}


if __name__ == "__main__":
    print("=== YUKI COST CALCULATOR (CONTRACT PRICING) ===\n")
    
    # Example: Today's session (18 images)
    session = calculate_session_cost(analysis_tokens=5000, num_images=18)
    
    print(f"Session Cost Breakdown:")
    print(f"  Analysis: ${session['analysis_cost']:.6f}")
    print(f"  Generation: ${session['generation_cost']:.6f}")
    print(f"  Total: ${session['total_cost']:.2f}")
    print(f"  Per Image: ${session['cost_per_image']:.2f}")
    print(f"\nImagen 3 Alternative:")
    print(f"  Cost: ${session['imagen_alternative']['cost']:.2f}")
    print(f"  Savings: ${session['imagen_alternative']['savings']:.2f} ({session['imagen_alternative']['savings_percentage']:.0f}%)")
