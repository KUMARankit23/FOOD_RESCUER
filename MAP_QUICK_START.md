# 🗺️ Map Tracking Quick Start

Get started with real-time map tracking in 2 minutes.

---

## ⚡ Quick Start

### Step 1: Open Dashboard (30 seconds)
```
1. Open: http://localhost:8501
2. Click "Map Tracking" in sidebar
3. View the interactive map!
```

### Step 2: Submit a Report to Populate Map
```bash
curl -X POST http://localhost:8000/api/v1/reports \
  -H "Content-Type: application/json" \
  -d '{
    "food_type": "vegetable biryani",
    "quantity": 60,
    "prep_time": "14:00",
    "temperature_c": 58.0,
    "location": "Hostel Mess A",
    "pickup_deadline": "20:00"
  }'
```

### Step 3: Refresh Dashboard
- Go back to Map Tracking page
- You'll see the route appear on the map!
- Check statistics below the map

---

## 🎯 What You Can See

### On the Map:
- 🔴 **Red Pin** = Donor location (Hostel Mess A)
- 🟢 **Green Pin** = Recipient location (Community Kitchen A)
- 🔵 **Blue Line** = Route from donor to recipient
- 🟦 **Circle** = Active dispatch status

### Statistics Below:
```
Total Dispatches     = 1
Distance Covered     = ~12.5 km
Active Routes        = 0
Delivered            = 1
```

### Dispatch Table:
```
Run ID              From              To                    Qty  Status
run_20241106_143025 Hostel Mess A    Community Kitchen A   60   delivered
```

---

## 🔌 API Quick Calls

### Get All Tracking Data
```bash
curl http://localhost:8000/api/v1/map/tracking | python -m json.tool
```

### Get Just Statistics
```bash
curl http://localhost:8000/api/v1/map/statistics | python -m json.tool
```

### Get Donor Locations
```bash
curl http://localhost:8000/api/v1/map/donors | python -m json.tool
```

### Get Recipient Locations
```bash
curl http://localhost:8000/api/v1/map/recipients | python -m json.tool
```

### Download Map as HTML
```bash
curl -X POST http://localhost:8000/api/v1/map/generate-html
```

---

## 📊 Submit Multiple Reports to See More Activity

```bash
# Report 1: Hostel → Community Kitchen
curl -X POST http://localhost:8000/api/v1/reports \
  -H "Content-Type: application/json" \
  -d '{"food_type":"vegetable biryani","quantity":60,"prep_time":"14:00","temperature_c":58.0,"location":"Hostel Mess A","pickup_deadline":"20:00"}'

# Report 2: Canteen → Shelter B
curl -X POST http://localhost:8000/api/v1/reports \
  -H "Content-Type: application/json" \
  -d '{"food_type":"chicken curry","quantity":80,"prep_time":"12:30","temperature_c":62.0,"location":"Canteen","pickup_deadline":"18:00"}'

# Report 3: Event Hall → NGO Center
curl -X POST http://localhost:8000/api/v1/reports \
  -H "Content-Type: application/json" \
  -d '{"food_type":"rice","quantity":40,"prep_time":"13:00","temperature_c":55.0,"location":"Event Hall","pickup_deadline":"19:00"}'
```

---

## 🎨 Map Legend

| Symbol | Meaning |
|--------|---------|
| 🔴 | Food Source (Donor) |
| 🟢 | Food Destination (Recipient) |
| 🔵 | Delivery Route |
| 🟦 | Active Dispatch |
| ⏳ | Pending Status |
| 🚚 | In Transit |
| ✓ | Delivered |

---

## 📱 Dashboard Pages

| Page | Purpose |
|------|---------|
| **Submit Report** | Create new food rescue ops |
| **View Runs** | See past reports and traces |
| **Metrics** | View performance stats |
| **Map Tracking** | 🎯 Real-time map visualization |
| **RAG Test** | Test knowledge base |

---

## 💡 Tips

1. **Submit different locations** to see routes across the map
2. **Zoom and pan** on the map to explore
3. **Click on pins** to see location details
4. **Refresh page** to see latest data
5. **Use API** for programmatic access

---

## 🚀 Next: Advanced Features

- **Heatmaps**: See high-activity areas
- **Export HTML**: Share maps with stakeholders
- **Historical Analysis**: View past dispatch patterns
- **Performance Metrics**: Track optimization over time

---

## ✅ You're Ready!

1. ✅ Dashboard: `http://localhost:8501` - Map Tracking page
2. ✅ API: `http://localhost:8000` - Map endpoints
3. ✅ Submit reports to see routes appear
4. ✅ Monitor statistics in real-time

**Happy tracking! 🎉**
