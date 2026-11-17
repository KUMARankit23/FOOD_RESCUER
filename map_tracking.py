"""
Map Tracking Module: Real-time visualization of food rescue operations.
Uses Folium for interactive maps, displays donors, recipients, routes, and pickups.
"""

import folium
from folium import plugins
import json
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
import math


# Location data
RECIPIENTS_DB = {
    "r1": {
        "name": "Community Kitchen A",
        "location": "Shelter District",
        "coords": (40.7128, -74.0060),
        "capacity": 100,
        "icon_color": "blue",
        "icon": "cutlery",
    },
    "r2": {
        "name": "Shelter B",
        "location": "Community Center",
        "coords": (40.7580, -73.9855),
        "capacity": 150,
        "icon_color": "green",
        "icon": "home",
    },
    "r3": {
        "name": "NGO Feeding Center",
        "location": "Downtown",
        "coords": (40.7489, -73.9680),
        "capacity": 80,
        "icon_color": "purple",
        "icon": "heart",
    },
}

DONOR_LOCATIONS = {
    "Hostel Mess A": {
        "coords": (40.8075, -73.9626),
        "icon_color": "red",
        "icon": "info-sign",
    },
    "Hostel Mess B": {
        "coords": (40.8049, -73.9649),
        "icon_color": "red",
        "icon": "info-sign",
    },
    "Canteen": {
        "coords": (40.8048, -73.9645),
        "icon_color": "orange",
        "icon": "info-sign",
    },
    "Event Hall": {
        "coords": (40.8060, -73.9630),
        "icon_color": "red",
        "icon": "info-sign",
    },
    "Sports Complex": {
        "coords": (40.8090, -73.9620),
        "icon_color": "red",
        "icon": "info-sign",
    },
}


def create_base_map(center_lat: float = 40.755, center_lon: float = -73.9776, zoom: int = 13) -> folium.Map:
    """Create a base Folium map centered on the campus area."""
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        tiles="OpenStreetMap"
    )
    
    # Add map controls
    folium.LayerControl().add_to(m)
    
    return m


def add_donor_markers(m: folium.Map, donors: Optional[List[Dict[str, Any]]] = None) -> folium.Map:
    """Add donor location markers to the map."""
    if donors is None:
        # Use default donor locations
        donors = [
            {
                "name": name,
                "coords": data["coords"],
                "food_type": "Various",
                "quantity": 0,
                "status": "available"
            }
            for name, data in DONOR_LOCATIONS.items()
        ]
    
    for donor in donors:
        coords = donor.get("coords")
        if coords:
            popup_text = f"""
            <b>{donor['name']}</b><br>
            Food: {donor.get('food_type', 'N/A')}<br>
            Quantity: {donor.get('quantity', 0)} portions<br>
            Status: {donor.get('status', 'unknown')}
            """
            
            folium.Marker(
                location=coords,
                popup=folium.Popup(popup_text, max_width=250),
                icon=folium.Icon(color="red", icon="info-sign", prefix="glyphicon"),
                tooltip=donor["name"]
            ).add_to(m)
    
    return m


def add_recipient_markers(m: folium.Map, recipients: Optional[List[Dict[str, Any]]] = None) -> folium.Map:
    """Add recipient location markers to the map."""
    if recipients is None:
        recipients = [
            {
                "id": rid,
                "name": data["name"],
                "coords": data["coords"],
                "capacity": data["capacity"],
                "location": data["location"],
                "status": "ready"
            }
            for rid, data in RECIPIENTS_DB.items()
        ]
    
    for recipient in recipients:
        coords = recipient.get("coords")
        if coords:
            capacity = recipient.get("capacity", 0)
            status = recipient.get("status", "unknown")
            
            # Color based on capacity usage
            if status == "full":
                color = "black"
            elif status == "ready":
                color = "green"
            else:
                color = "gray"
            
            popup_text = f"""
            <b>{recipient['name']}</b><br>
            Location: {recipient.get('location', 'N/A')}<br>
            Capacity: {capacity} portions<br>
            Status: {status}
            """
            
            folium.Marker(
                location=coords,
                popup=folium.Popup(popup_text, max_width=250),
                icon=folium.Icon(color=color, icon="cutlery", prefix="glyphicon"),
                tooltip=recipient["name"]
            ).add_to(m)
    
    return m


def add_route(m: folium.Map, from_coords: Tuple[float, float], to_coords: Tuple[float, float],
              route_id: str = "", color: str = "blue", weight: int = 2) -> folium.Map:
    """Add a route line between two points."""
    folium.PolyLine(
        locations=[from_coords, to_coords],
        color=color,
        weight=weight,
        opacity=0.8,
        popup=f"Route: {route_id}"
    ).add_to(m)
    
    return m


def add_active_dispatch(m: folium.Map, dispatch: Dict[str, Any]) -> folium.Map:
    """
    Add an active dispatch to the map with:
    - Donor location (red)
    - Recipient location (green)
    - Route between them (animated arrow)
    """
    
    donor_name = dispatch.get("donor_location", "")
    recipient_id = dispatch.get("recipient_id", "")
    status = dispatch.get("status", "in_transit")
    
    # Get coordinates
    donor_coords = DONOR_LOCATIONS.get(donor_name, {}).get("coords")
    recipient = RECIPIENTS_DB.get(recipient_id, {})
    recipient_coords = recipient.get("coords")
    
    if donor_coords and recipient_coords:
        # Add route
        color_map = {
            "pending": "orange",
            "in_transit": "blue",
            "arrived": "green",
            "delivered": "gray"
        }
        route_color = color_map.get(status, "blue")
        
        add_route(m, donor_coords, recipient_coords, dispatch.get("run_id", ""), color=route_color, weight=3)
        
        # Add midpoint with status icon
        mid_lat = (donor_coords[0] + recipient_coords[0]) / 2
        mid_lon = (donor_coords[1] + recipient_coords[1]) / 2
        
        status_emoji = {
            "pending": "⏳",
            "in_transit": "🚚",
            "arrived": "✓",
            "delivered": "✔️"
        }.get(status, "•")
        
        popup_text = f"""
        <b>Dispatch: {dispatch.get('run_id', 'N/A')}</b><br>
        From: {donor_name}<br>
        To: {recipient.get('name', 'N/A')}<br>
        Quantity: {dispatch.get('quantity', 0)} portions<br>
        Status: {status} {status_emoji}<br>
        ETA: {dispatch.get('eta', 'N/A')}
        """
        
        folium.CircleMarker(
            location=[mid_lat, mid_lon],
            radius=8,
            popup=folium.Popup(popup_text, max_width=250),
            color=route_color,
            fill=True,
            fillColor=route_color,
            fillOpacity=0.7,
            weight=2,
            tooltip=f"Dispatch {dispatch.get('run_id', 'N/A')}"
        ).add_to(m)
    
    return m


def create_operation_map(active_dispatches: Optional[List[Dict[str, Any]]] = None) -> folium.Map:
    """
    Create a complete operation map showing:
    - All donor locations
    - All recipient locations
    - Active dispatches with routes
    - Heat map of activity
    """
    
    m = create_base_map()
    
    # Add static locations
    add_donor_markers(m)
    add_recipient_markers(m)
    
    # Add active dispatches
    if active_dispatches:
        for dispatch in active_dispatches:
            add_active_dispatch(m, dispatch)
    
    return m


def add_heatmap(m: folium.Map, dispatch_history: List[Dict[str, Any]]) -> folium.Map:
    """Add a heat map layer showing dispatch frequency by location."""
    
    heat_data = []
    
    for dispatch in dispatch_history:
        donor_name = dispatch.get("donor_location")
        if donor_name in DONOR_LOCATIONS:
            coords = DONOR_LOCATIONS[donor_name]["coords"]
            heat_data.append([coords[0], coords[1], 0.5])
        
        recipient_id = dispatch.get("recipient_id")
        if recipient_id in RECIPIENTS_DB:
            coords = RECIPIENTS_DB[recipient_id]["coords"]
            heat_data.append([coords[0], coords[1], 0.5])
    
    if heat_data:
        plugins.HeatMap(heat_data, radius=15, blur=25, max_zoom=1).add_to(m)
    
    return m


def add_distance_circles(m: folium.Map, center_coords: Tuple[float, float], 
                         radius_km: float = 2) -> folium.Map:
    """Add distance circles around a location."""
    
    folium.Circle(
        location=center_coords,
        radius=radius_km * 1000,  # Convert to meters
        color="blue",
        fill=False,
        weight=2,
        opacity=0.6,
        popup=f"{radius_km} km radius"
    ).add_to(m)
    
    return m


def calculate_total_distance(dispatches: List[Dict[str, Any]]) -> float:
    """Calculate total distance traveled by all active dispatches."""
    
    total_distance = 0.0
    
    for dispatch in dispatches:
        donor_name = dispatch.get("donor_location")
        recipient_id = dispatch.get("recipient_id")
        
        donor_coords = DONOR_LOCATIONS.get(donor_name, {}).get("coords")
        recipient_coords = RECIPIENTS_DB.get(recipient_id, {}).get("coords")
        
        if donor_coords and recipient_coords:
            # Haversine formula for distance
            lat1, lon1 = donor_coords
            lat2, lon2 = recipient_coords
            
            R = 6371  # Earth radius in km
            dlat = math.radians(lat2 - lat1)
            dlon = math.radians(lon2 - lon1)
            
            a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            distance = R * c
            
            total_distance += distance
    
    return total_distance


def calculate_route_stats(dispatches: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate statistics about routes and dispatches."""
    
    total_distance = calculate_total_distance(dispatches)
    
    status_counts = {}
    for dispatch in dispatches:
        status = dispatch.get("status", "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1
    
    return {
        "total_dispatches": len(dispatches),
        "total_distance_km": round(total_distance, 2),
        "status_distribution": status_counts,
        "active_dispatches": status_counts.get("in_transit", 0),
        "delivered": status_counts.get("delivered", 0),
    }


def export_map_html(m: folium.Map, filename: str = "map.html") -> str:
    """Export map to HTML file."""
    m.save(filename)
    return filename


# Example usage data structures
SAMPLE_DISPATCH = {
    "run_id": "run_20241106_143025",
    "donor_location": "Hostel Mess A",
    "recipient_id": "r1",
    "recipient_name": "Community Kitchen A",
    "quantity": 60,
    "status": "in_transit",
    "eta": "18:15",
    "created_at": "2024-11-06T17:45:00",
}

SAMPLE_DISPATCH_HISTORY = [
    {
        "run_id": "run_20241106_143025",
        "donor_location": "Hostel Mess A",
        "recipient_id": "r1",
        "status": "delivered",
        "quantity": 60,
    },
    {
        "run_id": "run_20241106_142000",
        "donor_location": "Canteen",
        "recipient_id": "r2",
        "status": "in_transit",
        "quantity": 80,
    },
    {
        "run_id": "run_20241106_141000",
        "donor_location": "Event Hall",
        "recipient_id": "r3",
        "status": "pending",
        "quantity": 40,
    },
]


if __name__ == "__main__":
    # Test map creation
    m = create_operation_map(SAMPLE_DISPATCH_HISTORY)
    add_heatmap(m, SAMPLE_DISPATCH_HISTORY)
    
    # Calculate stats
    stats = calculate_route_stats(SAMPLE_DISPATCH_HISTORY)
    print("Route Statistics:")
    print(json.dumps(stats, indent=2))
    
    # Export
    filename = export_map_html(m, "operation_map.html")
    print(f"Map saved to {filename}")
