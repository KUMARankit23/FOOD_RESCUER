"""
The Four Agents of FoodRescue-MAS.
Each with a specific role, tools, and structured output.
"""

from typing import Optional, List
from schemas import SurplusReport, ValidatedRecord, RankedMatches, RankedMatch, SafetyDecision, Evidence
from tools import (
    validate_report, lookup_location, estimate_demand, query_recipients,
    distance_km, time_temp_check, schedule_pickup
)
from rag_knowledge_base import retrieve_passages
from food_categories import FOOD_CATEGORIES


class EklavyaIntakeAgent:
    """The self-taught watcher: Reads raw reports and validates them."""
    
    name = "Eklavya"
    description = "Intake and Validation Agent"
    
    def execute(self, report: SurplusReport) -> ValidatedRecord:
        """Validate a raw surplus report."""
        
        # Run validation checks
        validation = validate_report(
            report.food_type,
            report.quantity,
            report.temperature_c,
            report.location
        )
        
        # Lookup location
        loc_result = lookup_location(report.location)
        
        issues = validation["issues"]
        missing_fields = []
        
        if not loc_result["exists"]:
            issues.append(f"Location '{report.location}' not found in system")
        
        # Determine status
        if validation["valid"] and loc_result["exists"]:
            status = "valid"
        else:
            status = "needs_fix" if len(issues) < 3 else "rejected"
        
        return ValidatedRecord(
            report=report,
            status=status,
            issues=issues,
            missing_fields=missing_fields
        )


class ArjunaMatchingAgent:
    """The focused archer: Ranks the best recipient, ignoring distractions."""
    
    name = "Arjuna"
    description = "Demand and Matching Agent"
    
    def execute(self, validated_record: ValidatedRecord) -> RankedMatches:
        """Rank compatible recipients for the surplus."""
        
        report = validated_record.report
        
        # Get food category
        food_category = FOOD_CATEGORIES.get(report.food_type, "packaged")
        
        # Query compatible recipients
        compatible = query_recipients(food_category)
        
        if not compatible:
            # Return empty matches
            return RankedMatches(matches=[])
        
        # Score each recipient
        scored = []
        for recipient in compatible:
            recipient_id = recipient["recipient_id"]
            
            # Distance score (closer is better)
            dist = distance_km(report.location, recipient_id)
            if dist is None:
                dist = 10.0  # Default large distance
            distance_score = max(0, 100 - dist * 10)
            
            # Capacity score (can fit the quantity)
            capacity_score = min(100, (recipient["capacity"] / report.quantity) * 50) if report.quantity > 0 else 50
            
            # Demand score (estimated from food type)
            demand = estimate_demand(report.food_type)
            demand_score = demand["estimated_demand_ratio"] * 100
            
            # Combined score
            combined_score = (distance_score * 0.4 + capacity_score * 0.3 + demand_score * 0.3)
            
            scored.append({
                "recipient_id": recipient_id,
                "recipient_name": recipient["recipient_name"],
                "score": combined_score,
                "distance_km": dist,
                "reason": f"Distance {dist:.1f}km, capacity {recipient['capacity']} portions"
            })
        
        # Sort by score descending, take top 3
        scored.sort(key=lambda x: x["score"], reverse=True)
        top_3 = scored[:3]
        
        matches = [RankedMatch(**m) for m in top_3]
        return RankedMatches(matches=matches)


class DronacharyyaSafetyAgent:
    """The keeper of rules: Judges safety, backed by evidence."""
    
    name = "Dronacharya"
    description = "Safety and Compliance Agent"
    
    def execute(self, validated_record: ValidatedRecord) -> SafetyDecision:
        """Assess food safety and cite evidence."""
        
        report = validated_record.report
        food_category = FOOD_CATEGORIES.get(report.food_type, "packaged")
        
        # Retrieve relevant passages
        query = f"{report.food_type} {food_category} temperature holding"
        passages = retrieve_passages(query, k=3)
        
        # Run time-temp check
        safety_check = time_temp_check(
            report.prep_time,
            report.temperature_c,
            food_category
        )
        
        # Determine verdict
        if not safety_check["safe_temperature"]:
            verdict = "unsafe"
            reason = f"Temperature {report.temperature_c}°C below required {safety_check['min_required_temp_c']}°C"
        else:
            verdict = "conditional"
            reason = f"Temperature acceptable. Elapsed time approaching {safety_check['max_safe_hours']}-hour limit."
        
        # Attach evidence
        evidence = [
            Evidence(chunk_id=p["id"], text=p["text"])
            for p in passages
        ]
        
        return SafetyDecision(
            verdict=verdict,
            reason=reason,
            evidence=evidence
        )


class ChanakyaLogisticsAgent:
    """The strategist: Combines outputs into a final decision and plan."""
    
    name = "Chanakya"
    description = "Logistics Manager Agent"
    
    def execute(
        self,
        validated_record: ValidatedRecord,
        ranked_matches: RankedMatches,
        safety_decision: SafetyDecision,
        run_id: str
    ):
        """Combine all factors into a final pickup decision."""
        
        from schemas import FinalDecision
        
        report = validated_record.report
        
        # Check basic conditions
        if validated_record.status != "valid":
            return FinalDecision(
                action="no_pickup",
                recipient_id=None,
                recipient_name=None,
                pickup_time=None,
                explanation=f"Report validation failed: {', '.join(validated_record.issues)}",
                run_id=run_id
            )
        
        if safety_decision.verdict == "unsafe":
            return FinalDecision(
                action="discard",
                recipient_id=None,
                recipient_name=None,
                pickup_time=None,
                explanation=f"Safety check failed: {safety_decision.reason}",
                run_id=run_id
            )
        
        if not ranked_matches.matches:
            return FinalDecision(
                action="no_pickup",
                recipient_id=None,
                recipient_name=None,
                pickup_time=None,
                explanation="No compatible recipients found.",
                run_id=run_id
            )
        
        # Try to schedule pickup with top match
        top_match = ranked_matches.matches[0]
        schedule = schedule_pickup(top_match.recipient_id, report.pickup_deadline)
        
        if schedule["available"]:
            return FinalDecision(
                action="dispatch",
                recipient_id=top_match.recipient_id,
                recipient_name=top_match.recipient_name,
                pickup_time=schedule["scheduled_time"],
                explanation=f"Dispatch to {top_match.recipient_name}. {safety_decision.reason}",
                run_id=run_id
            )
        else:
            # Top recipient not available, check if retry with next is worth it
            # (One re-check, then give up)
            return FinalDecision(
                action="hold",
                recipient_id=None,
                recipient_name=None,
                pickup_time=None,
                explanation=f"Top recipient unavailable at {report.pickup_deadline}. Waiting for next available slot.",
                run_id=run_id
            )


if __name__ == "__main__":
    from schemas import SurplusReport
    
    # Test agents
    report = SurplusReport(
        food_type="vegetable biryani",
        quantity=60,
        prep_time="14:00",
        temperature_c=58.0,
        location="Hostel Mess B",
        pickup_deadline="20:00"
    )
    
    print("=== Eklavya ===")
    eklavya = EklavyaIntakeAgent()
    validated = eklavya.execute(report)
    print(f"Status: {validated.status}, Issues: {validated.issues}")
    
    print("\n=== Arjuna ===")
    arjuna = ArjunaMatchingAgent()
    matches = arjuna.execute(validated)
    print(f"Top match: {matches.matches[0].recipient_name if matches.matches else 'None'}")
    
    print("\n=== Dronacharya ===")
    dronacharya = DronacharyyaSafetyAgent()
    safety = dronacharya.execute(validated)
    print(f"Verdict: {safety.verdict}, Reason: {safety.reason}")
