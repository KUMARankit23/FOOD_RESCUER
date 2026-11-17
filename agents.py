"""
The Four Agents of FoodRescue-MAS - LLM-POWERED
Each agent uses Google Gemini for reasoning while maintaining deterministic safety rules.
"""

import json
from typing import Optional, List, Dict, Any
from schemas import SurplusReport, ValidatedRecord, RankedMatches, RankedMatch, SafetyDecision, Evidence
from tools import (
    validate_report, lookup_location, estimate_demand, query_recipients,
    distance_km, time_temp_check, schedule_pickup
)
from rag_system import get_rag_system
from llm_integration import get_llm_manager
from food_categories import FOOD_CATEGORIES


class EklavyaIntakeAgent:
    """The self-taught watcher: LLM-powered intake and validation."""
    
    name = "Eklavya"
    description = "Intake and Validation Agent"
    
    def __init__(self):
        self.llm = get_llm_manager()
    
    def execute(self, report: SurplusReport) -> ValidatedRecord:
        """Validate report using LLM reasoning + deterministic rules."""
        
        # Step 1: LLM-based extraction and reasoning
        extraction_prompt = f"""Analyze this food donation report and extract key details:

Food Type: {report.food_type}
Quantity: {report.quantity} portions
Prep Time: {report.prep_time}
Temperature: {report.temperature_c}°C
Location: {report.location}
Pickup Deadline: {report.pickup_deadline}

Provide analysis as JSON:
{{
  "extracted_food_type": "...",
  "inferred_category": "...",
  "is_complete": true/false,
  "issues": ["..."],
  "confidence": 0.0-1.0
}}"""
        
        try:
            llm_analysis = self.llm.generate(
                prompt=extraction_prompt,
                system="You are Eklavya, the Food Intake Agent. Extract and validate donation information.",
                structured_output={"type": "object"}
            )
            analysis = json.loads(llm_analysis)
        except:
            analysis = {
                "extracted_food_type": report.food_type,
                "inferred_category": "unknown",
                "is_complete": True,
                "issues": [],
                "confidence": 0.7
            }
        
        # Step 2: Deterministic validation (cannot be overridden)
        validation = validate_report(
            report.food_type,
            report.quantity,
            report.temperature_c,
            report.location
        )
        
        loc_result = lookup_location(report.location)
        
        # Step 3: Combine issues
        issues = list(set(validation["issues"] + analysis.get("issues", [])))
        
        if not loc_result["exists"]:
            issues.append(f"Location '{report.location}' not found in system")
        
        # Step 4: Status determination (deterministic + LLM confidence)
        llm_confidence = analysis.get("confidence", 0.5)
        has_issues = len(issues) > 0
        
        if validation["valid"] and loc_result["exists"] and llm_confidence > 0.7 and not has_issues:
            status = "valid"
        elif has_issues and len(issues) < 2:
            status = "needs_fix"
        else:
            status = "rejected"
        
        return ValidatedRecord(
            report=report,
            status=status,
            issues=issues,
            missing_fields=analysis.get("missing_fields", [])
        )


class ArjunaMatchingAgent:
    """The focused archer: LLM-powered recipient matching using tools."""
    
    name = "Arjuna"
    description = "Demand and Matching Agent"
    
    def __init__(self):
        self.llm = get_llm_manager()
    
    def execute(self, validated_record: ValidatedRecord) -> RankedMatches:
        """Rank recipients using LLM reasoning + tool-assisted matching."""
        
        report = validated_record.report
        food_category = FOOD_CATEGORIES.get(report.food_type, "packaged")
        
        # Step 1: Query compatible recipients using tool
        compatible = query_recipients(food_category)
        
        if not compatible:
            return RankedMatches(matches=[])
        
        # Step 2: LLM-powered reasoning for ranking
        recipient_info = json.dumps(compatible, indent=2)
        ranking_prompt = f"""You are Arjuna, the Recipient Matching Agent.

Food Details:
- Type: {report.food_type}
- Quantity: {report.quantity} portions
- Location: {report.location}
- Deadline: {report.pickup_deadline}

Available Recipients:
{recipient_info}

Rank recipients by suitability. Consider:
1. Distance from donor location
2. Recipient capacity vs quantity needed
3. Food preferences and dietary restrictions
4. Estimated demand for this food type

Return JSON with top 3 ranked recipients:
{{
  "rankings": [
    {{
      "recipient_id": "...",
      "rank": 1,
      "score": 0-100,
      "reasoning": "Why this is the best match"
    }}
  ]
}}"""
        
        try:
            llm_ranking = self.llm.generate(
                prompt=ranking_prompt,
                system="You are Arjuna, the expert in recipient matching.",
                structured_output={"type": "object"}
            )
            ranking_result = json.loads(llm_ranking)
            rankings = ranking_result.get("rankings", [])
        except:
            rankings = []
        
        # Step 3: Deterministic scoring as fallback/validation
        scored = []
        for recipient in compatible:
            recipient_id = recipient["recipient_id"]
            
            distance = distance_km(report.location, recipient_id)
            if distance is None:
                distance = 10.0
            distance_score = max(0, 100 - distance * 10)
            
            capacity_score = min(100, (recipient["capacity"] / report.quantity) * 50) if report.quantity > 0 else 50
            
            demand = estimate_demand(report.food_type)
            demand_score = demand["estimated_demand_ratio"] * 100
            
            combined_score = (distance_score * 0.4 + capacity_score * 0.3 + demand_score * 0.3)
            
            scored.append({
                "recipient_id": recipient_id,
                "recipient_name": recipient["recipient_name"],
                "score": combined_score,
                "distance_km": distance,
                "reason": f"Distance {distance:.1f}km, capacity {recipient['capacity']} portions"
            })
        
        # Merge LLM ranking with deterministic scoring
        if rankings:
            for ranking in rankings:
                rid = ranking.get("recipient_id")
                for scored_item in scored:
                    if scored_item["recipient_id"] == rid:
                        scored_item["score"] = ranking.get("score", scored_item["score"])
                        scored_item["reason"] = ranking.get("reasoning", scored_item["reason"])
                        break
        
        scored.sort(key=lambda x: x["score"], reverse=True)
        top_3 = scored[:3]
        
        matches = [RankedMatch(**m) for m in top_3]
        return RankedMatches(matches=matches)


class DronacharyyaSafetyAgent:
    """The keeper of rules: LLM-powered safety assessment with RAG evidence."""
    
    name = "Dronacharya"
    description = "Safety and Compliance Agent"
    
    def __init__(self):
        self.llm = get_llm_manager()
        self.rag = get_rag_system()
    
    def execute(self, validated_record: ValidatedRecord) -> SafetyDecision:
        """Assess food safety using RAG evidence + LLM reasoning."""
        
        report = validated_record.report
        food_category = FOOD_CATEGORIES.get(report.food_type, "packaged")
        
        # Step 1: Retrieve relevant safety passages using RAG
        search_query = f"{report.food_type} {food_category} temperature {report.temperature_c}°C holding time"
        passages = self.rag.retrieve(search_query, k=5)
        
        if not passages:
            # Fallback to deterministic check
            safety_check = time_temp_check(report.prep_time, report.temperature_c, food_category)
            verdict = "unsafe" if not safety_check["safe_temperature"] else "conditional"
            reason = f"Temperature {report.temperature_c}°C - No specific guidelines found"
            evidence = []
            source_refs = []
        else:
            # Step 2: Format evidence
            evidence = [
                Evidence(
                    chunk_id=p["doc_id"],
                    text=p["text"][:300]  # Truncate for display
                )
                for p in passages[:3]
            ]
            
            # Step 3: LLM-powered assessment using evidence
            assessment_prompt = f"""You are Dronacharya, the Food Safety Agent. Assess if this food can be safely redistributed.

FOOD DETAILS:
- Type: {report.food_type}
- Category: {food_category}
- Quantity: {report.quantity} portions
- Temperature: {report.temperature_c}°C
- Prep Time: {report.prep_time}

EVIDENCE FROM FSSAI GUIDELINES:
{json.dumps([p['text'][:200] for p in passages[:3]], indent=2)}

Determine verdict as JSON:
{{
  "verdict": "safe|unsafe|conditional|insufficient_evidence",
  "reasoning": "Detailed explanation",
  "key_concerns": [],
  "confidence": 0.0-1.0
}}"""
            
            try:
                assessment = self.llm.generate(
                    prompt=assessment_prompt,
                    system="You are an expert food safety officer. Make conservative safety decisions.",
                    structured_output={"type": "object"}
                )
                assessment_result = json.loads(assessment)
                verdict = assessment_result.get("verdict", "conditional")
                reason = assessment_result.get("reasoning", "Assessment completed")
            except:
                # Fallback to deterministic
                safety_check = time_temp_check(report.prep_time, report.temperature_c, food_category)
                verdict = "unsafe" if not safety_check["safe_temperature"] else "conditional"
                reason = f"Temperature {report.temperature_c}°C assessment"
            
            source_refs = [
                {
                    "source": p["source"],
                    "organization": p["organization"],
                    "page": p["page_number"]
                }
                for p in passages[:3]
            ]
        
        return SafetyDecision(
            verdict=verdict,
            reason=reason,
            evidence=evidence if evidence else [Evidence(chunk_id="none", text="No specific evidence found")]
        )


class ChanakyaLogisticsAgent:
    """The strategist: LLM-powered coordination and decision making."""
    
    name = "Chanakya"
    description = "Logistics Manager Agent"
    
    def __init__(self):
        self.llm = get_llm_manager()
    
    def execute(
        self,
        validated_record: ValidatedRecord,
        ranked_matches: RankedMatches,
        safety_decision: SafetyDecision,
        run_id: str
    ):
        """Coordinate all inputs into a final dispatch decision using LLM."""
        
        from schemas import FinalDecision
        
        report = validated_record.report
        
        # Step 1: Check if basic conditions prevent dispatch
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
                explanation=f"Safety check failed: {safety_decision.reason}. UNSAFE FOR DISTRIBUTION.",
                run_id=run_id
            )
        
        if not ranked_matches.matches:
            return FinalDecision(
                action="no_pickup",
                recipient_id=None,
                recipient_name=None,
                pickup_time=None,
                explanation="No compatible recipients available.",
                run_id=run_id
            )
        
        # Step 2: LLM-powered coordination decision
        matches_info = json.dumps([
            {
                "rank": i+1,
                "name": m.recipient_name,
                "score": m.score,
                "distance": m.distance_km,
                "reason": m.reason
            }
            for i, m in enumerate(ranked_matches.matches)
        ], indent=2)
        
        coordination_prompt = f"""You are Chanakya, the Logistics Coordinator. Make the final dispatch decision.

SUMMARY:
- Report Status: {validated_record.status}
- Safety Verdict: {safety_decision.verdict}
- Top Recipients:
{matches_info}

CONSTRAINTS:
- NEVER override a "unsafe" verdict from Dronacharya
- Consider availability and feasibility
- Optimize for recipient suitability

DECISION (as JSON):
{{
  "action": "dispatch|hold|discard|no_pickup",
  "recipient_choice": "recipient_id_or_null",
  "rationale": "Why this decision",
  "confidence": 0.0-1.0
}}"""
        
        try:
            decision_result = self.llm.generate(
                prompt=coordination_prompt,
                system="You are Chanakya, the expert logistics coordinator. Make conservative dispatch decisions.",
                structured_output={"type": "object"}
            )
            decision_json = json.loads(decision_result)
            action = decision_json.get("action", "hold")
            chosen_recipient_id = decision_json.get("recipient_choice")
            explanation = decision_json.get("rationale", "Dispatch coordinated")
        except:
            # Fallback: dispatch to top match if safety allows
            action = "dispatch"
            chosen_recipient_id = ranked_matches.matches[0].recipient_id if ranked_matches.matches else None
            explanation = "Dispatch to top-ranked recipient"
        
        if action == "dispatch" and chosen_recipient_id:
            # Find the chosen recipient's details
            chosen = next((m for m in ranked_matches.matches if m.recipient_id == chosen_recipient_id), ranked_matches.matches[0])
            
            schedule = schedule_pickup(chosen.recipient_id, report.pickup_deadline)
            
            if schedule["available"]:
                return FinalDecision(
                    action="dispatch",
                    recipient_id=chosen.recipient_id,
                    recipient_name=chosen.recipient_name,
                    pickup_time=schedule["scheduled_time"],
                    explanation=explanation,
                    run_id=run_id
                )
            else:
                return FinalDecision(
                    action="hold",
                    recipient_id=None,
                    recipient_name=None,
                    pickup_time=None,
                    explanation=f"Top choice {chosen.recipient_name} unavailable. Waiting for next slot.",
                    run_id=run_id
                )
        
        return FinalDecision(
            action=action,
            recipient_id=None,
            recipient_name=None,
            pickup_time=None,
            explanation=explanation,
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
