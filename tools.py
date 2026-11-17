"""
Deterministic tools used by agents.
No LLM inside - pure functions for reliable, traceable logic.
"""

import math
from typing import List, Dict, Any, Optional


# Recipient database
RECIPIENTS_DB = {
    "r1": {
        "name": "Community Kitchen A",
        "food_types": ["cooked_veg", "cooked_starch"],
        "capacity": 100,
        "location": "Shelter District",
        "location_coords": (40.7128, -74.0060),
        "hours": "08:00-18:00",
    },
    "r2": {
        "name": "Shelter B",
        "food_types": ["cooked_veg", "cooked_meat", "cooked_starch"],
        "capacity": 150,
        "location": "Community Center",
        "location_coords": (40.7580, -73.9855),
        "hours": "06:00-22:00",
    },
    "r3": {
        "name": "NGO Feeding Center",
        "food_types": ["cooked_veg", "packaged"],
        "capacity": 80,
        "location": "Downtown",
        "location_coords": (40.7489, -73.9680),
        "hours": "10:00-16:00",
    },
}

LOCATION_COORDS = {
    "Hostel Mess A": (40.8075, -73.9626),
    "Hostel Mess B": (40.8049, -73.9649),
    "Canteen": (40.8048, -73.9645),
    "Event Hall": (40.8060, -73.9630),
    "Sports Complex": (40.8090, -73.9620),
}

FOOD_CATEGORIES = {
    "vegetable biryani": "cooked_veg",
    "chicken curry": "cooked_meat",
    "rice": "cooked_starch",
    "bread": "packaged",
    "dairy dessert": "dairy",
}


def validate_report(food_type: str, quantity: int, temperature_c: float, location: str) -> Dict[str, Any]:
    """Schema and range validation."""
    issues = []
    
    if food_type not in FOOD_CATEGORIES:
        issues.append(f"Unknown food type: {food_type}")
    if quantity <= 0 or quantity > 500:
        issues.append(f"Invalid quantity: {quantity}")
    if temperature_c < -10 or temperature_c > 90:
        issues.append(f"Invalid temperature: {temperature_c}")
    if location not in LOCATION_COORDS:
        issues.append(f"Unknown location: {location}")
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
    }


def lookup_location(location: str) -> Dict[str, Any]:
    """SQLite lookup - location validation."""
    if location in LOCATION_COORDS:
        return {"exists": True, "coords": LOCATION_COORDS[location]}
    return {"exists": False, "coords": None}


def estimate_demand(food_type: str) -> Dict[str, Any]:
    """Rule-based demand estimation."""
    # Simple model: some foods have higher demand
    base_demand = {
        "cooked_veg": 0.8,
        "cooked_meat": 0.9,
        "cooked_starch": 0.7,
        "packaged": 0.6,
        "dairy": 0.5,
    }
    category = FOOD_CATEGORIES.get(food_type, "packaged")
    return {"estimated_demand_ratio": base_demand.get(category, 0.5)}


def query_recipients(food_category: str) -> List[Dict[str, Any]]:
    """Query SQLite for compatible recipients."""
    compatible = []
    for rid, data in RECIPIENTS_DB.items():
        if food_category in data["food_types"]:
            compatible.append({
                "recipient_id": rid,
                "recipient_name": data["name"],
                "capacity": data["capacity"],
                "location": data["location"],
                "hours": data["hours"],
            })
    return compatible


def distance_km(from_location: str, to_recipient_id: str) -> Optional[float]:
    """Calculate distance in km using Haversine formula."""
    if from_location not in LOCATION_COORDS or to_recipient_id not in RECIPIENTS_DB:
        return None
    
    from_coords = LOCATION_COORDS[from_location]
    to_coords = RECIPIENTS_DB[to_recipient_id]["location_coords"]
    
    # Simple approximation: 1 degree ≈ 111 km
    lat_diff = abs(from_coords[0] - to_coords[0]) * 111
    lon_diff = abs(from_coords[1] - to_coords[1]) * 111 * math.cos(math.radians(from_coords[0]))
    
    return math.sqrt(lat_diff**2 + lon_diff**2)


def time_temp_check(prep_time_str: str, current_temp_c: float, food_category: str) -> Dict[str, Any]:
    """Check if food is safe based on time and temperature."""
    # Simplified: assume elapsed time proportional to hours since prep
    # Real system would use actual timestamps
    
    safe_temps = {
        "cooked_veg": 57,
        "cooked_meat": 60,
        "cooked_starch": 55,
        "packaged": 20,
        "dairy": 5,
    }
    safe_hours = {
        "cooked_veg": 4,
        "cooked_meat": 3,
        "cooked_starch": 4,
        "packaged": 8,
        "dairy": 2,
    }
    
    min_temp = safe_temps.get(food_category, 20)
    max_hours = safe_hours.get(food_category, 4)
    
    return {
        "safe_temperature": current_temp_c >= min_temp,
        "min_required_temp_c": min_temp,
        "max_safe_hours": max_hours,
    }


def schedule_pickup(recipient_id: str, pickup_time: str) -> Dict[str, Any]:
    """Check if a pickup slot is available and schedule it."""
    if recipient_id not in RECIPIENTS_DB:
        return {"available": False, "reason": "Unknown recipient"}
    
    recipient = RECIPIENTS_DB[recipient_id]
    hours = recipient["hours"]  # e.g., "06:00-22:00"
    
    # Simple check: is pickup_time within hours?
    try:
        start, end = hours.split("-")
        pickup_hour = int(pickup_time.split(":")[0])
        start_hour = int(start.split(":")[0])
        end_hour = int(end.split(":")[0])
        
        within_hours = start_hour <= pickup_hour < end_hour
        return {
            "available": within_hours,
            "scheduled_time": pickup_time if within_hours else None,
            "reason": "Within operating hours" if within_hours else f"Outside hours {hours}",
        }
    except:
        return {"available": False, "reason": "Invalid time format"}


if __name__ == "__main__":
    # Test tools
    print("=== Validate Report ===")
    print(validate_report("vegetable biryani", 60, 58.0, "Hostel Mess B"))
    
    print("\n=== Query Recipients ===")
    print(query_recipients("cooked_veg"))
    
    print("\n=== Distance ===")
    print(distance_km("Hostel Mess B", "r1"))
    
    print("\n=== Time-Temp Check ===")
    print(time_temp_check("14:00", 58.0, "cooked_veg"))
