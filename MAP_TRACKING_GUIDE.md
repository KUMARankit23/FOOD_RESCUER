# 🗺️ FoodRescue-MAS: Map Tracking Guide

Real-time visualization and tracking of food rescue operations with interactive maps, routes, and statistics.

---

## 📍 Features

### 1. **Real-Time Map Visualization**
- Interactive Folium maps showing all operations
- Donor locations (🔴 Red pins)
- Recipient locations (🟢 Green pins)
- Active delivery routes (🔵 Blue lines)
- Route status indicators (⏳ Pending, 🚚 In Transit, ✓ Arrived)

### 2. **Live Tracking**
- Track each dispatch from pickup to delivery
- Real-time ETA updates
- Distance calculations
- Status transitions

### 3. **Statistical Dashboard**
- Total distance covered
- Active routes count
- Delivery success rate
- Status distribution
- Heatmaps of activity

### 4. **Export & Integration**
- Download maps as HTML
- API endpoints for programmatic access
- Historical dispatch data
- Performance analytics

---

## 🎯 How to Use - Dashboard

### Step 1: Open Map Tracking Page
1. Open `http://localhost:8501`
2. Select **"Map Tracking"** from the sidebar
3. View the live operation map

### Step 2: Understand the Map
```
🔴 Red Pins    = Food Donor Locations (where food is stored)
🟢 Green Pins  = Recipient Locations (where food goes)
🔵 Blue Lines  = Active Delivery Routes
🟦 Circles     = Active Dispatches (with status)
```

### Step 3: Monitor Dispatches
- **Dispatch Table**: Shows all recent dispatches
- **Status Column**: Pending → In Transit → Delivered
- **Distance Column**: Total km covered
- **Quantity Column**: Portions being transported

### Step 4: View Statistics
```
Total Dispatches      = Number of food rescue operations
Distance Covered      = Total km traveled by all trucks
Active Routes         = Currently in-transit deliveries
Delivered             = Completed deliveries
Status Distribution   = Breakdown by pending/in-transit/delivered
```

---

## 🔌 API Endpoints

### Core Map Data

#### 1. Get All Tracking Data
```bash
curl http://localhost:8000/api/v1/map/tracking
```

**Response**:
```json
{
  "dispatches": [
    {
      "run_id": "run_20241106_143025",
      "donor_location": "Hostel Mess A",
      "recipient_id": "r1",
      "recipient_name": "Community Kitchen A",
      "quantity": 60,
      "status": "delivered",
      "created_at": "2024-11-06T17:45:00"
    }
  ],
  "statistics": {
    "total_dispatches": 5,
    "total_distance_km": 12.5,
    "status_distribution": {
      "pending": 1,
      "in_transit": 1,
      "delivered": 3
    }
  },
  "donors": [...],
  "recipients": [...]
}
```

#### 2. Get Map Statistics
```bash
curl http://localhost:8000/api/v1/map/statistics
```

**Response**:
```json
{
  "timestamp": "2024-11-06T18:30:45.123456",
  "statistics": {
    "total_dispatches": 5,
    "total_distance_km": 12.5,
    "active_dispatches": 2,
    "delivered": 3
  }
}
```

#### 3. Get Dispatch History (for heatmaps)
```bash
curl http://localhost:8000/api/v1/map/history
```

**Response**:
```json
{
  "total_historical_dispatches": 10,
  "history": [
    {
      "run_id": "run_20241106_143025",
      "donor_location": "Hostel Mess A",
      "recipient_id": "r1",
      "timestamp": "2024-11-06T17:45:00"
    }
  ]
}
```

### Location Data

#### 4. Get All Donor Locations
```bash
curl http://localhost:8000/api/v1/map/donors
```

**Response**:
```json
{
  "donors": [
    {
      "name": "Hostel Mess A",
      "coords": [40.8075, -73.9626],
      "icon_color": "red",
      "icon": "info-sign"
    }
  ],
  "total": 5
}
```

#### 5. Get All Recipient Locations
```bash
curl http://localhost:8000/api/v1/map/recipients
```

**Response**:
```json
{
  "recipients": [
    {
      "id": "r1",
      "name": "Community Kitchen A",
      "coords": [40.7128, -74.0060],
      "capacity": 100,
      "location": "Shelter District",
      "icon_color": "green",
      "icon": "cutlery"
    }
  ],
  "total": 3
}
```

### Map Generation

#### 6. Generate HTML Map
```bash
curl -X POST http://localhost:8000/api/v1/map/generate-html
```

**Response**:
```json
{
  "status": "success",
  "filename": "operation_map_api.html",
  "message": "Map HTML generated successfully"
}
```

---

## 🚀 Integration Examples

### Example 1: Fetch and Display Tracking Data
```bash
# Get all tracking data
curl -s http://localhost:8000/api/v1/map/tracking | python -m json.tool

# Extract just statistics
curl -s http://localhost:8000/api/v1/map/tracking | jq '.statistics'
```

### Example 2: Monitor Active Routes
```bash
#!/bin/bash
while true; do
  echo "=== Active Routes ==="
  curl -s http://localhost:8000/api/v1/map/statistics | jq '.statistics | {active: .active_dispatches, total: .total_dispatches, distance: .total_distance_km}'
  sleep 5
done
```

### Example 3: Generate Maps Periodically
```bash
#!/bin/bash
# Generate a new map every hour
while true; do
  curl -X POST http://localhost:8000/api/v1/map/generate-html
  echo "Map generated at $(date)"
  sleep 3600
done
```

### Example 4: Python Integration
```python
import requests
import json

# Get tracking data
response = requests.get('http://localhost:8000/api/v1/map/tracking')
data = response.json()

# Extract statistics
stats = data['statistics']
print(f"Total Dispatches: {stats['total_dispatches']}")
print(f"Distance Covered: {stats['total_distance_km']} km")
print(f"Active Routes: {stats['active_dispatches']}")

# Extract dispatch details
for dispatch in data['dispatches']:
    print(f"  - {dispatch['donor_location']} → {dispatch['recipient_name']}")
```

---

## 🎨 Map Features

### 1. Interactive Controls
- **Zoom**: Scroll to zoom in/out
- **Pan**: Click and drag to move around
- **Click on Pins**: View details popup
- **Layer Toggle**: Hide/show layers (donors, recipients, routes)

### 2. Visual Indicators
```
Route Colors:
  🟠 Orange = Pending (waiting to pickup)
  🔵 Blue   = In Transit (actively delivering)
  🟢 Green  = Arrived (at recipient location)
  ⚫ Gray   = Delivered (completed)

Location Status:
  🔴 Red    = Active donors
  🟢 Green  = Ready recipients
  ⚫ Black   = Full recipients
  ⚪ Gray    = Unavailable
```

### 3. Map Layers
- **Base Map**: OpenStreetMap
- **Donor Layer**: All donor locations
- **Recipient Layer**: All recipient locations
- **Route Layer**: Active and historical routes
- **Heatmap Layer**: Dispatch frequency visualization

---

## 📊 Statistics Explained

### Total Dispatches
- **Definition**: Number of food rescue operations completed or in progress
- **Use**: Track volume of food redistribution

### Distance Covered
- **Definition**: Total kilometers traveled by all deliveries
- **Calculation**: Haversine formula between donor and recipient
- **Use**: Estimate fuel costs and logistics impact

### Active Dispatches
- **Definition**: Deliveries currently in transit
- **Use**: Monitor current operations

### Delivered
- **Definition**: Completed food rescues
- **Use**: Measure success rate

### Status Distribution
- **Pending**: Awaiting pickup
- **In Transit**: Currently being delivered
- **Delivered**: Completed successfully

---

## 🔍 Example Scenarios

### Scenario 1: View Recent Deliveries
```bash
# Get last 5 deliveries
curl -s http://localhost:8000/api/v1/map/history | \
  jq '.history[-5:] | .[] | {run_id, donor_location, recipient_name}'
```

### Scenario 2: Calculate Total Distance Today
```bash
# Get sum of all distances
curl -s http://localhost:8000/api/v1/map/statistics | \
  jq '.statistics.total_distance_km'
```

### Scenario 3: Find Active Routes
```bash
# List all in-transit deliveries
curl -s http://localhost:8000/api/v1/map/tracking | \
  jq '.dispatches[] | select(.status=="in_transit") | {run_id, donor_location, recipient_name}'
```

### Scenario 4: Monitor Recipient Capacity
```bash
# Check recipient availability
curl -s http://localhost:8000/api/v1/map/recipients | \
  jq '.recipients[] | {name, capacity}'
```

---

## 📈 Performance Metrics

### Tracking Efficiency
- **Route Optimization**: Shorter routes = lower cost
- **Speed**: Average delivery time
- **Coverage**: Number of recipients served

### Resource Usage
- **Total Distance**: Sum of all routes
- **Average Distance**: Per delivery
- **Peak Hours**: When most active

### Success Metrics
- **Delivery Rate**: % successfully delivered
- **On-Time Rate**: % within ETA
- **Recipient Satisfaction**: Distance to recipient

---

## 🛠️ Technical Details

### Map Tracking Module (`map_tracking.py`)
```
Functions:
  - create_base_map()          # Create Folium map
  - add_donor_markers()        # Add donor locations
  - add_recipient_markers()    # Add recipient locations
  - add_route()                # Add route line
  - add_active_dispatch()      # Add dispatch with status
  - create_operation_map()     # Complete operation map
  - add_heatmap()              # Add frequency heatmap
  - calculate_route_stats()    # Compute statistics
  - export_map_html()          # Save as HTML file
```

### Data Structures

**Dispatch Object**:
```python
{
    "run_id": str,
    "donor_location": str,
    "recipient_id": str,
    "recipient_name": str,
    "quantity": int,
    "status": "pending|in_transit|delivered",
    "created_at": datetime,
    "eta": str
}
```

**Statistics Object**:
```python
{
    "total_dispatches": int,
    "total_distance_km": float,
    "active_dispatches": int,
    "delivered": int,
    "status_distribution": {
        "pending": int,
        "in_transit": int,
        "delivered": int
    }
}
```

---

## 🔧 Troubleshooting

### Issue: Map Not Loading
**Solution**: 
```bash
# Check if folium is installed
pip install -r requirements.txt

# Restart Streamlit
# Close Streamlit (Ctrl+C) and run:
streamlit run streamlit_dashboard.py
```

### Issue: No Dispatches Showing
**Solution**:
```bash
# Submit a report first
curl -X POST http://localhost:8000/api/v1/reports \
  -H "Content-Type: application/json" \
  -d '{
    "food_type": "biryani",
    "quantity": 60,
    "prep_time": "14:00",
    "temperature_c": 58.0,
    "location": "Hostel Mess A",
    "pickup_deadline": "20:00"
  }'

# Then check tracking
curl http://localhost:8000/api/v1/map/tracking
```

### Issue: Coordinates Not Working
**Solution**: Verify coordinates are in [latitude, longitude] format:
```python
# Correct format
coords = (40.8075, -73.9626)  # (latitude, longitude)

# Check in tools.py or map_tracking.py
```

---

## 📚 References

- **Folium Documentation**: https://python-visualization.github.io/folium/
- **OpenStreetMap**: https://www.openstreetmap.org/
- **Haversine Formula**: Distance calculation between coordinates

---

## 🎯 Next Steps

1. ✅ **Submit reports** to populate the map
2. ✅ **View real-time tracking** on dashboard
3. ✅ **Download map HTML** for sharing
4. ✅ **Query API** for programmatic access
5. ✅ **Integrate with external systems** (fleet management, etc.)

---

## 📞 Support

For issues or questions:
1. Check the **Troubleshooting** section above
2. Review **API Endpoint** documentation
3. Check terminal output for error messages
4. Verify all services are running (`http://localhost:8000` and `http://localhost:8501`)

---

**🚀 Map Tracking is now integrated into FoodRescue-MAS!**
