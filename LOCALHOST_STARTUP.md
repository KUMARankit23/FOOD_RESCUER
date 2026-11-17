# 🚀 FoodRescue-MAS: Localhost Startup Guide

## ✅ Services Now Running

### 1. **REST API** - `http://localhost:8000`
**Status**: ✅ Running on Uvicorn  
**Port**: 8000  
**Purpose**: Backend API for food report submission and data retrieval

#### Available Endpoints:

**Health Check**:
```bash
curl http://localhost:8000/health
# Response: {"status": "ok"}
```

**Submit a Food Report**:
```bash
curl -X POST http://localhost:8000/api/v1/reports \
  -H "Content-Type: application/json" \
  -d '{
    "food_type": "biryani",
    "quantity": 60,
    "prep_time": "14:00",
    "temperature_c": 58.0,
    "location": "Hostel",
    "pickup_deadline": "20:00"
  }'
```

**View Past Runs**:
```bash
curl http://localhost:8000/api/v1/runs
```

**Get Execution Trace**:
```bash
curl http://localhost:8000/api/v1/runs/{run_id}/trace
```

**List Recipients**:
```bash
curl http://localhost:8000/api/v1/recipients
```

---

### 2. **Streamlit Dashboard** - `http://localhost:8501`
**Status**: ✅ Running on Streamlit  
**Port**: 8501  
**Purpose**: Interactive web interface with 4 pages

#### Available Pages:

1. **Submit Report**
   - Form to enter surplus food data
   - Real-time validation
   - Immediate decision display

2. **View Runs**
   - List all past executions
   - Click to see detailed trace
   - View all intermediate steps

3. **Metrics**
   - Performance statistics
   - Accuracy charts
   - Latency analysis
   - Reliability metrics

4. **RAG Test**
   - Test knowledge base retrieval
   - See how safety agent finds evidence
   - Verify fact-checking capability

---

## 🎯 How to Use

### Option 1: Web Dashboard (Easiest)
1. Open browser: `http://localhost:8501`
2. Go to "Submit Report" page
3. Fill in the form:
   - Food type: "biryani"
   - Quantity: 60 portions
   - Temperature: 58°C
   - Location: "Hostel"
   - Pickup deadline: "20:00"
4. Click "Process"
5. See the decision immediately!

### Option 2: REST API (For Developers)
```bash
# 1. Submit report
curl -X POST http://localhost:8000/api/v1/reports \
  -H "Content-Type: application/json" \
  -d '{
    "food_type": "biryani",
    "quantity": 60,
    "prep_time": "14:00",
    "temperature_c": 58.0,
    "location": "Hostel",
    "pickup_deadline": "20:00"
  }'

# Expected response:
# {
#   "run_id": "run_abc123",
#   "decision": {
#     "action": "dispatch",
#     "recipient_name": "Community Kitchen",
#     "pickup_time": "18:15",
#     "explanation": "..."
#   }
# }

# 2. Get the trace for that run
curl http://localhost:8000/api/v1/runs/run_abc123/trace

# 3. See all metrics
curl http://localhost:8000/api/v1/runs
```

### Option 3: Test Different Scenarios
Try these different scenarios in the dashboard:

**Scenario A: Valid Food**
- Food: "biryani"
- Quantity: 60
- Temperature: 58°C
- Expected: ✅ Dispatch

**Scenario B: Cold Food**
- Food: "rice"
- Quantity: 30
- Temperature: 40°C
- Expected: ❌ Unsafe (below 57°C)

**Scenario C: Invalid Location**
- Food: "dal"
- Quantity: 40
- Temperature: 65°C
- Location: "Unknown"
- Expected: ❌ Invalid location

---

## 📊 What's Happening Behind the Scenes

When you submit a report, this is what happens:

```
1. EKLAVYA (Intake Agent)
   └─ Validates all fields
   └─ Checks location exists
   └─ Output: ValidatedRecord

2. ARJUNA (Matching Agent)
   └─ Queries recipient database
   └─ Calculates distances
   └─ Ranks by capacity & proximity
   └─ Output: Top 3 matches

3. DRONACHARYA (Safety Agent)
   └─ Retrieves food safety passages (RAG)
   └─ Checks temperature thresholds
   └─ Cites evidence
   └─ Output: SafetyDecision with citations

4. CHANAKYA (Logistics Manager)
   └─ Combines all inputs
   └─ Checks recipient availability
   └─ Schedules pickup
   └─ Output: FinalDecision

5. SUKSHMADARSHINI (Observability)
   └─ Records full trace
   └─ Calculates metrics
   └─ Stores for analysis
```

---

## 🔍 Real-Time Monitoring

### View Live Logs
Both processes show live output in their terminals:

**API Terminal**:
```
INFO:     Started server process [44840]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Dashboard Terminal**:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### Check What's Running
```bash
# Windows - Show all Python processes
Get-Process python

# Or check specific ports
netstat -ano | findstr :8000
netstat -ano | findstr :8501
```

---

## 📱 API Documentation

### 11 Available Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Service health check |
| `/api/v1/reports` | POST | Submit food report |
| `/api/v1/runs` | GET | List all runs |
| `/api/v1/runs/{run_id}` | GET | Get specific run details |
| `/api/v1/runs/{run_id}/trace` | GET | Get execution trace |
| `/api/v1/recipients` | GET | List all recipients |
| `/api/v1/scenarios/generate` | POST | Generate test scenarios |
| `/api/v1/evaluate` | POST | Run evaluation suite |
| `/api/v1/evaluate/summary` | GET | Get evaluation metrics |
| `/api/v1/safety/retrieve` | GET | Test RAG retrieval |
| `/api/v1/schema` | GET | Get API schema |

---

## 🎮 Example Workflow

### Step 1: Health Check
```bash
curl http://localhost:8000/health
# {"status":"ok"}
```

### Step 2: Submit Report
```bash
curl -X POST http://localhost:8000/api/v1/reports \
  -H "Content-Type: application/json" \
  -d '{
    "food_type": "biryani",
    "quantity": 60,
    "prep_time": "14:00",
    "temperature_c": 58.0,
    "location": "Hostel",
    "pickup_deadline": "20:00"
  }'
```

**Response**:
```json
{
  "run_id": "run_20241106_143025",
  "decision": {
    "action": "dispatch",
    "recipient_id": "r1",
    "recipient_name": "Community Kitchen",
    "pickup_time": "18:15",
    "explanation": "Dispatch to Community Kitchen at 18:15"
  },
  "timing_ms": {
    "total": 156.23,
    "eklavya": 39.06,
    "arjuna": 39.06,
    "dronacharya": 46.87,
    "chanakya": 31.24
  }
}
```

### Step 3: View Trace
```bash
curl http://localhost:8000/api/v1/runs/run_20241106_143025/trace
```

**Response**:
```json
{
  "run_id": "run_20241106_143025",
  "agents": [
    {
      "name": "eklavya",
      "status": "success",
      "input": {"food_type": "biryani", ...},
      "output": {"status": "valid", "issues": []},
      "timing_ms": 39.06
    },
    {
      "name": "arjuna",
      "status": "success",
      "output": {
        "matches": [
          {"recipient_id": "r1", "score": 85.0, "distance_km": 2.4}
        ]
      },
      "timing_ms": 39.06
    },
    ...
  ]
}
```

---

## 🎯 Common Tasks

### Task 1: Test the System Works
```bash
# Test API
curl http://localhost:8000/health

# Test Dashboard
Open http://localhost:8501 in browser
```

### Task 2: Submit Multiple Reports
```bash
# Report 1: Good food
curl -X POST http://localhost:8000/api/v1/reports -d '{"food_type":"biryani",...}'

# Report 2: Cold food
curl -X POST http://localhost:8000/api/v1/reports -d '{"food_type":"rice",...,"temperature_c":40}'

# View all
curl http://localhost:8000/api/v1/runs
```

### Task 3: Run Evaluation
```bash
curl -X POST http://localhost:8000/api/v1/evaluate

# Get results
curl http://localhost:8000/api/v1/evaluate/summary
```

### Task 4: Generate Scenarios
```bash
curl -X POST http://localhost:8000/api/v1/scenarios/generate \
  -H "Content-Type: application/json" \
  -d '{"count": 10}'
```

---

## 🔧 Troubleshooting

### Port Already in Use
If port 8000 or 8501 is already in use:

```bash
# Find what's using the port
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <PID> /F

# Or use different ports
python api.py --port 9000
streamlit run streamlit_dashboard.py --server.port 9501
```

### Module Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Verify installation
python -c "import api; print('OK')"
```

### Slow Response
- Check terminal output for errors
- Restart services
- Verify internet connection (for MCP tools)

---

## 📊 What You Can Do Now

✅ **Submit Reports** - Using form or API  
✅ **See Decisions** - Dispatch, hold, discard, no_pickup  
✅ **View Traces** - Complete execution flow  
✅ **Test Scenarios** - Multiple food types  
✅ **Check Metrics** - Accuracy, latency, reliability  
✅ **Verify Safety** - RAG retrieval with evidence

---

## 🎉 You're Ready!

Both services are running and ready to use:

- **API**: `http://localhost:8000`
- **Dashboard**: `http://localhost:8501`

### Next Steps:
1. Open `http://localhost:8501` in your browser
2. Go to "Submit Report" page
3. Fill in a food report
4. See the decision immediately!

---

## 📞 Need Help?

- **API Docs**: Visit `http://localhost:8000/docs` for interactive API documentation
- **Dashboard**: All features available in the web interface
- **Errors**: Check the terminal where services are running for detailed logs

---

**🚀 FoodRescue-MAS is now running on your localhost!**
