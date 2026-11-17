"""
Vyasa: Scenario and ground-truth generator.
Composes every test case with rule-based ground truth.
"""

import random
import json
from datetime import datetime, timedelta
from typing import Tuple, Dict, Any
from schemas import SurplusReport


FOOD_TYPES = {
    "vegetable biryani": {"category": "cooked_veg", "safe_hours": 4, "safe_temp_c": 57},
    "chicken curry": {"category": "cooked_meat", "safe_hours": 3, "safe_temp_c": 60},
    "rice": {"category": "cooked_starch", "safe_hours": 4, "safe_temp_c": 55},
    "bread": {"category": "packaged", "safe_hours": 8, "safe_temp_c": 20},
    "dairy dessert": {"category": "dairy", "safe_hours": 2, "safe_temp_c": 5},
}

LOCATIONS = ["Hostel Mess A", "Hostel Mess B", "Canteen", "Event Hall", "Sports Complex"]

RECIPIENTS = [
    {"id": "r1", "name": "Community Kitchen A", "food_types": ["cooked_veg", "cooked_starch"], "capacity": 100, "location": "Shelter District", "hours": "08:00-18:00"},
    {"id": "r2", "name": "Shelter B", "food_types": ["cooked_veg", "cooked_meat", "cooked_starch"], "capacity": 150, "location": "Community Center", "hours": "06:00-22:00"},
    {"id": "r3", "name": "NGO Feeding Center", "food_types": ["cooked_veg", "packaged"], "capacity": 80, "location": "Downtown", "hours": "10:00-16:00"},
]


def generate_scenario() -> Tuple[SurplusReport, Dict[str, Any]]:
    """Generate a synthetic scenario with ground truth."""
    
    # Random food selection
    food_type = random.choice(list(FOOD_TYPES.keys()))
    food_info = FOOD_TYPES[food_type]
    
    # Random quantity (about 25% awkward cases)
    if random.random() < 0.25:
        quantity = random.randint(10, 30)  # Small portion
    else:
        quantity = random.randint(40, 100)
    
    # Prep time (last 1-4 hours)
    hours_ago = random.randint(1, 4)
    prep_time = (datetime.now() - timedelta(hours=hours_ago)).strftime("%H:%M")
    
    # Temperature (some awkward cases near boundaries)
    if random.random() < 0.25:
        temp_c = food_info["safe_temp_c"] + random.uniform(-3, 3)  # Borderline
    else:
        temp_c = food_info["safe_temp_c"] + random.uniform(5, 15)  # Safe
    
    # Location
    location = random.choice(LOCATIONS)
    
    # Pickup deadline (30 min to 3 hours away)
    deadline_minutes = random.randint(30, 180)
    pickup_time = (datetime.now() + timedelta(minutes=deadline_minutes)).strftime("%H:%M")
    
    report = SurplusReport(
        food_type=food_type,
        quantity=quantity,
        prep_time=prep_time,
        temperature_c=temp_c,
        location=location,
        pickup_deadline=pickup_time
    )
    
    # Generate ground truth using explicit rules
    ground_truth = _compute_ground_truth(report, food_info)
    
    return report, ground_truth


def _compute_ground_truth(report: SurplusReport, food_info: Dict[str, Any]) -> Dict[str, Any]:
    """Compute rule-based ground truth answer."""
    
    elapsed_hours = random.uniform(0, food_info["safe_hours"])
    is_safe = report.temperature_c >= food_info["safe_temp_c"] and elapsed_hours <= food_info["safe_hours"]
    
    # Find compatible recipients
    compatible = [r for r in RECIPIENTS if food_info["category"] in r["food_types"]]
    
    if not compatible:
        action = "no_pickup"
        reason = "No compatible recipient for this food type."
    elif report.quantity > max(r["capacity"] for r in compatible):
        action = "no_pickup"
        reason = "Quantity exceeds all recipient capacities."
    elif not is_safe:
        action = "discard"
        reason = "Food safety violation: temperature or time threshold exceeded."
    else:
        # Safe and compatible: dispatch to best recipient
        best = compatible[0]
        action = "dispatch"
        reason = f"Dispatch to {best['name']} (capacity {best['capacity']})."
    
    return {
        "expected_action": action,
        "reason": reason,
        "is_safe": is_safe,
        "elapsed_hours": elapsed_hours,
        "compatible_recipients": [r["id"] for r in compatible],
    }


def generate_batch(count: int = 40) -> list:
    """Generate a batch of scenarios."""
    scenarios = []
    for _ in range(count):
        report, ground_truth = generate_scenario()
        scenarios.append({
            "report": report.dict(),
            "ground_truth": ground_truth
        })
    return scenarios


if __name__ == "__main__":
    # Test
    scenarios = generate_batch(5)
    print(json.dumps(scenarios, indent=2, default=str))
