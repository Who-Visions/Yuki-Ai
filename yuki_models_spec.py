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
    "gemini_2.5_flash": {
        "model_id": "gemini-2.5-flash",
        "tier": "flash",
        "context_window": 1_048_576,
        "capabilities": ["multimodal", "tools", "fast", "thinking_tokens"],
        "pricing": {
            # ⚠️ CONTRACT PRICING (CSV) - Unk's spec has $0.10/$0.40
            "input_per_1m": 0.30,      # $0.30/1M tokens (SKU: FDAB-647C-5A22)
            "output_per_1m": 2.50,     # $2.50/1M tokens thinking (SKU: A253-E8A3-DE5C)
            "output_regular_per_1m": 0.40,  # Estimated regular output (no CSV data)
            "caching_input_per_1m": 0.03,   # $0.03/1M tokens (90% discount)
            "image_input_per_1m": 0.30      # $0.30/1M images (SKU: 7C13-537E-1E75)
        },
        "rate_limits": {
            "rpm": 1000,
            "tpm": 4_000_000
        },
        "description": "Yuki's analysis engine. Fast multimodal processing.",
        "use_cases": ["perspective_analysis", "facial_analysis", "image_understanding"]
    },
    
    "gemini_2.5_pro": {
        "model_id": "gemini-2.5-pro-001",
        "tier": "pro",
        "context_window": 1_048_576,
        "capabilities": ["complex_reasoning", "coding", "thinking_tokens", "multimodal"],
        "pricing": {
            # ⚠️ CONTRACT PRICING (CSV) - Unk's spec has $2.50/$10.00
            "input_per_1m": 1.25,      # $1.25/1M tokens (SKU: A121-E2B5-1418) ✅ CORRECTED
            "output_per_1m": 10.00,    # $10.00/1M tokens (SKU: 5DA2-3F77-1CA5) ✅ MATCH
            "caching_input_per_1m": 0.125,  # $0.125/1M tokens (90% discount)
            "image_input_per_1m": 1.25,     # $1.25/1M images (SKU: B401-3774-BCEE)
            "image_caching_per_1m": 0.125   # $0.125/1M cached images
        },
        "rate_limits": {
            "rpm": 150,
            "tpm": 1_000_000
        },
        "description": "Deep reasoning for complex transformations.",
        "use_cases": ["complex_analysis", "research"]
    },
    
    "gemini_3_pro_image": {
        "model_id": "gemini-3-pro-image-preview",
        "tier": "pro",
        "location": "global",
        "context_window": 1_048_576,
        "capabilities": ["image_generation", "multimodal"],
        "pricing": {
            # ⚠️ CONTRACT PRICING (CSV)
            "image_output_per_1m": 120.00,  # $120/1M images = $0.12/image (SKU: 47A8-A5A1-B26C)
            "image_input_per_1m": 2.00,     # $2.00/1M images (SKU: 98E0-CA2E-4AA8)
            "text_input_per_1m": 2.00,      # $2.00/1M tokens (SKU: EAC4-305F-1249)
            "text_output_per_1m": 12.00     # $12.00/1M tokens (SKU: 2737-2D33-D986)
        },
        "rate_limits": {
            "rpm": 60,
            "tpm": 500_000
        },
        "description": "Yuki's PRIMARY image generator. High quality transformations.",
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
    return YUKI_MODELS.get(mode, YUKI_MODELS["gemini_2.5_flash"])


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
        input_price = pricing.get("input_per_1m") or pricing.get("text_input_per_1m", 0)
        total_cost += (input_tokens / 1_000_000) * input_price
    
    if output_tokens > 0:
        output_price = pricing.get("output_per_1m") or pricing.get("text_output_per_1m", 0)
        total_cost += (output_tokens / 1_000_000) * output_price
    
    # Images
    if images > 0:
        # Check if this is a generation model
        if "generation_per_image" in pricing:
            total_cost += images * pricing["generation_per_image"]
        elif "image_output_per_1m" in pricing:
            # $120 per 1M images = $0.00012 per image, but we want $0.12 per image
            # So actually it's $120 / 1000 images = $0.12 per image
            total_cost += images * 0.12  # Fixed: $0.12 per image
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
    analysis_cost = estimate_cost("gemini_2.5_flash", input_tokens=analysis_tokens)
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
