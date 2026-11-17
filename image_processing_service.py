"""
Image Processing Service for Multimodal Food Analysis
Vision LLM integration for food photo understanding
"""

import base64
import json
from typing import Dict, Any, Optional, List
from llm_integration import get_llm_manager


class ImageAnalyzer:
    """Analyzes food images using vision LLM"""
    
    def __init__(self):
        self.llm = get_llm_manager()
        self.max_image_size_mb = 5
    
    def validate_image(self, image_base64: str) -> tuple[bool, Optional[str]]:
        """Validate image format and size"""
        
        if not image_base64:
            return False, "Empty image"
        
        try:
            size_mb = len(base64.b64decode(image_base64)) / (1024 * 1024)
            if size_mb > self.max_image_size_mb:
                return False, f"Image too large: {size_mb:.1f}MB"
        except:
            return False, "Invalid base64 image"
        
        return True, None
    
    def analyze_food_image(self, image_base64: str, donor_food_type: str) -> Dict[str, Any]:
        """Analyze food image and extract observations"""
        
        is_valid, error = self.validate_image(image_base64)
        if not is_valid:
            return {
                "valid": False,
                "error": error,
                "observations": []
            }
        
        # Prepare image for LLM
        analysis_prompt = f"""Analyze this food image. The donor claims it is: {donor_food_type}

Provide analysis as JSON:
{{
  "detected_food_type": "what you see",
  "condition": "good|acceptable|poor",
  "visible_issues": [],
  "freshness_estimate": "fresh|acceptable|old",
  "safety_concerns": [],
  "matches_donor_claim": true/false,
  "confidence": 0.0-1.0
}}

IMPORTANT: Do not claim to detect bacterial contamination, toxins, or microbes - only visible observations."""
        
        try:
            # For now, return mock analysis (real vision LLM would be called here)
            analysis = {
                "valid": True,
                "detected_food_type": donor_food_type,
                "condition": "good",
                "visible_issues": [],
                "freshness_estimate": "fresh",
                "safety_concerns": [],
                "matches_donor_claim": True,
                "confidence": 0.85
            }
            
            return analysis
        except Exception as e:
            return {
                "valid": False,
                "error": str(e),
                "observations": []
            }
    
    def compare_with_donor_claim(self, image_analysis: Dict[str, Any], 
                                donor_food_type: str) -> Dict[str, Any]:
        """Compare image analysis with donor claim"""
        
        detected = image_analysis.get("detected_food_type", "unknown").lower()
        claimed = donor_food_type.lower()
        
        matches = detected in claimed or claimed in detected
        
        return {
            "matches": matches,
            "detected": detected,
            "claimed": claimed,
            "discrepancy": not matches,
            "confidence": image_analysis.get("confidence", 0)
        }


class PickupPhotoRecorder:
    """Records photo evidence for pickup"""
    
    def __init__(self):
        self.photos: Dict[str, List[Dict[str, Any]]] = {}
    
    def record_photo(self, job_id: str, image_base64: str, caption: str) -> Dict[str, Any]:
        """Record photo with metadata"""
        
        analyzer = ImageAnalyzer()
        is_valid, error = analyzer.validate_image(image_base64)
        
        if not is_valid:
            return {"status": "error", "message": error}
        
        photo = {
            "id": f"{job_id}_{len(self.photos.get(job_id, []))}",
            "job_id": job_id,
            "image": image_base64[:100] + "...",  # Truncated for storage
            "caption": caption,
            "recorded_at": json.dumps({"datetime": "now"})
        }
        
        if job_id not in self.photos:
            self.photos[job_id] = []
        
        self.photos[job_id].append(photo)
        
        return {"status": "success", "photo_id": photo["id"]}
    
    def get_photos(self, job_id: str) -> List[Dict[str, Any]]:
        """Get all photos for a job"""
        return self.photos.get(job_id, [])


class DeliveryProofCollector:
    """Collects proof of delivery"""
    
    def __init__(self):
        self.proofs: Dict[str, Dict[str, Any]] = {}
    
    def record_delivery_proof(self, run_id: str, recipient_confirmation_image: str,
                             recipient_name: str, quantity_received: int) -> Dict[str, Any]:
        """Record delivery proof"""
        
        analyzer = ImageAnalyzer()
        is_valid, error = analyzer.validate_image(recipient_confirmation_image)
        
        if not is_valid:
            return {"status": "error", "message": error}
        
        proof = {
            "run_id": run_id,
            "image_hash": hash(recipient_confirmation_image) % 10000,
            "recipient": recipient_name,
            "quantity": quantity_received,
            "recorded_at": "now"
        }
        
        self.proofs[run_id] = proof
        return {"status": "success", "proof_recorded": True}
    
    def get_proof(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Get delivery proof"""
        return self.proofs.get(run_id)


# Global instances
image_analyzer = ImageAnalyzer()
pickup_recorder = PickupPhotoRecorder()
delivery_proof = DeliveryProofCollector()


def get_image_analyzer() -> ImageAnalyzer:
    return image_analyzer


def get_pickup_recorder() -> PickupPhotoRecorder:
    return pickup_recorder


def get_delivery_proof_collector() -> DeliveryProofCollector:
    return delivery_proof
