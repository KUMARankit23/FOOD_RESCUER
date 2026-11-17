# � Food Rescue MAS - Multi-Agent System

A sophisticated food rescue and redistribution platform powered by multi-agent AI orchestration. Connects food donors, pickers, and recipients in real-time with intelligent decision-making and live tracking.

**Live Demo:** https://food-rescuer-1.onrender.com

---

## 🎯 System Overview

### How It Works

```
1. Donor submits surplus food with location 📍
   ↓
2. Intake Agent (Eklavya) validates food details
   ↓
3. Recipient Matcher (Arjuna) finds best recipients
   ↓
4. Safety Agent (Dronacharya) checks food safety
   ↓
5. Coordinator (Chanakya) makes final dispatch decision
   ↓
6. Picker picks up food and delivers to recipient
   ↓
7. Real-time tracking & recipient confirmation ✅
```

---

## 🚀 Quick Start

### Deploy on Render.com (Free)

1. **Fork the Repository**
   - https://github.com/KUMARankit23/FOOD_RESCUER

2. **Create Render Service**
   - Go to https://render.com
   - New → Web Service
   - Select your forked repo
   - Build command: (auto-detected)
   - Start command: `python api.py`

3. **Deploy**
   - Click Deploy
   - Wait 3-5 minutes
   - Your app will be live at `https://your-service.onrender.com`

---

## � Local Development

### Prerequisites
- Python 3.10+
- Node.js 18+
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/KUMARankit23/FOOD_RESCUER
cd "food rescue mas"

# Backend setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd frontend_react
npm install
npm run build
cd ..
```

### Run Locally

**Terminal 1 - Backend:**
```bash
python api.py
```
Backend runs on `http://localhost:8000`

**Terminal 2 - Frontend (Dev Mode):**
```bash
cd frontend_react
npm run dev
```
Frontend runs on `http://localhost:5173`

**Access:** http://localhost:5173

---

## 🏗️ Architecture

### Backend (FastAPI)
- **api.py** - REST API endpoints & static file serving
- **sutradhara_flow.py** - Multi-agent orchestration engine
- **sukshmadarshini_observer.py** - Agent execution monitoring
- **vyasa_generator.py** - Report generation & scenarios

### Frontend (React 18 + Vite)
- **Dashboard** - Real-time overview & metrics
- **Submit Food** - Donor food submission with map picker
- **Operations** - Live dispatch tracking & agent chat
- **Analytics** - Performance metrics & evaluation summary
- **Live Map** - Real-time delivery tracking with GPS

---

## 📋 Features

### Core Features
✅ Multi-agent decision-making system  
✅ Real-time live tracking with GPS  
✅ Interactive location picker (Leaflet maps)  
✅ Agent chat & execution timeline  
✅ Recipient status updates & feedback  
✅ Analytics & performance dashboard  
✅ Food category tracking  
✅ Delivery history & reports  

### Agent System
- **Eklavya** (Intake) - Food validation & intake
- **Arjuna** (Matching) - Recipient matching algorithm
- **Dronacharya** (Safety) - Food safety verification
- **Chanakya** (Coordination) - Final dispatch decisions

---

## 🎨 Design System

### Color Palette
- **Cream** - `#F8F5ED` (Background)
- **Forest Green** - `#3F654A` (Primary)
- **Terracotta** - `#C77C55` (Accent)
- **Sage** - `#829B78` (Secondary)

### Component Library
- Custom buttons, cards, badges
- Form components with validation
- Charts (Recharts integration)
- Timeline & tracking UI
- Responsive layout system

---

## � Project Structure

```
food-rescue-mas/
├── api.py                          # FastAPI app + CORS + static serving
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Multi-stage Docker build
├── sutradhara_flow.py             # Agent orchestration
├── sukshmadarshini_observer.py    # Execution monitoring
├── vyasa_generator.py             # Report generation
├── *_service.py                   # Service layers
├── *_agents.py                    # Agent implementations
│
└── frontend_react/
    ├── package.json               # React dependencies
    ├── vite.config.js            # Vite build config
    ├── tailwind.config.js        # Tailwind CSS
    ├── postcss.config.js         # PostCSS
    ├── index.html                # Entry HTML
    │
    └── src/
        ├── main.jsx              # React entry point
        ├── App.jsx               # Main router
        ├── components/
        │   ├── charts/           # Analytics charts
        │   ├── common/           # Reusable components
        │   ├── layout/           # Layout components
        │   ├── maps/             # Map & location
        │   ├── operations/       # Operations UI
        │   └── forms/            # Form components
        ├── pages/                # Page components
        ├── hooks/                # Custom React hooks
        ├── services/             # API clients
        ├── utils/                # Helper functions
        └── styles/               # CSS/Tailwind styles
```

---

## 🔌 API Endpoints

### Reports
- `POST /api/v1/reports` - Submit food report
- `GET /api/v1/runs` - List all runs
- `GET /api/v1/runs/{run_id}` - Get run details
- `GET /api/v1/runs/{run_id}/trace` - Get agent execution trace

### Recipients
- `GET /api/v1/recipients` - List all recipients
- `GET /api/v1/map/recipients` - Get recipient locations

### Analytics
- `GET /api/v1/evaluate/summary` - Evaluation metrics
- `GET /api/v1/scenarios` - Generate scenarios
- `POST /api/v1/scenarios/evaluate` - Evaluate scenarios

### Map & Tracking
- `GET /api/v1/map/tracking` - Real-time tracking data
- `GET /api/v1/map/statistics` - Map statistics
- `GET /api/v1/map/history` - Dispatch history
- `GET /api/v1/map/donors` - Donor locations
- `POST /api/v1/map/generate-html` - Generate map HTML

### Health
- `GET /health` - Service health check

---

## 🌍 Deployment

### Render.com (Production)
```
URL: https://food-rescuer-1.onrender.com
Auto-deploys from: main branch
Build time: ~3-5 minutes
```

### Docker (Local)
```bash
# Build
docker build -t food-rescue .

# Run
docker run -p 8000:8000 food-rescue
```

---

## 📦 Dependencies

### Backend
- **fastapi** (0.109.0) - Web framework
- **uvicorn** (0.31.1+) - ASGI server
- **pydantic** (2.6.0+) - Data validation
- **python-dotenv** (1.2.2+) - Environment config

### Frontend
- **react** (18.2.0) - UI library
- **vite** (5.0.0) - Build tool
- **tailwindcss** (3.4.0) - Styling
- **react-router-dom** (6.20.0) - Routing
- **leaflet** (1.9.4) - Maps
- **recharts** (2.10.0) - Charts
- **axios** (1.6.0) - HTTP client

---

## 🧪 Testing

### Local Testing

**Backend Health:**
```bash
curl http://localhost:8000/health
```

**Submit Food Report:**
```bash
curl -X POST http://localhost:8000/api/v1/reports \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Hostel A",
    "quantity": 10,
    "food_type": "Rice",
    "urgency": "High"
  }'
```

**List Runs:**
```bash
curl http://localhost:8000/api/v1/runs
```

---

## 🔐 Environment Variables

### Backend (.env)
```
PYTHONUNBUFFERED=1
```

### Frontend (.env)
```
VITE_API_BASE_URL=http://localhost:8000  # Dev only (leave empty for production)
```

---

## � Troubleshooting

### "Not Found" on Frontend
- Ensure `npm run build` completed successfully
- Check `/app/static/index.html` exists in Dockerfile
- Verify Render deployment has both stages building

### CORS Errors
- Check api.py has correct allow_origins
- On Render, use relative paths: `/api/v1/...`
- Frontend should not hardcode localhost

### Blank Dashboard
- Check browser console for network errors (DevTools → Network)
- Verify API calls go to same domain
- Check backend is running (GET /health should return 200)

### Build Failures
- Check requirements.txt for version conflicts
- Ensure package.json has all dependencies
- Review Dockerfile for correct paths

---

## 📊 Performance

- **Frontend Load Time:** < 2s
- **API Response Time:** < 500ms
- **Map Load Time:** < 1.5s
- **Dashboard Refresh:** 2s intervals

---

## 📝 License

MIT License - See LICENSE file for details

---

## � Team & Acknowledgments

Built with ❤️ for food rescue and community welfare.

**Core Agents Named After Sanskrit/Historical Figures:**
- Eklavya - Legendary archer, self-learning
- Arjuna - Master strategist & warrior
- Dronacharya - Teacher & strategist
- Chanakya - Brilliant administrator

---

## 🚀 Future Roadmap

- [ ] SMS notifications for donors & recipients
- [ ] Mobile app (React Native)
- [ ] Advanced route optimization
- [ ] ML-based food quality prediction
- [ ] Integration with NGOs
- [ ] Sustainability metrics dashboard
- [ ] Multi-language support

---

## 📞 Support

- **GitHub Issues:** https://github.com/KUMARankit23/FOOD_RESCUER/issues
- **Documentation:** Check individual component files for detailed comments
- **Live Demo:** https://food-rescuer-1.onrender.com

---

## ✨ Key Takeaways

This system demonstrates:
- Multi-agent AI orchestration in production
- Real-time data tracking & visualization
- Containerized deployment on Render
- React + FastAPI modern stack
- Responsive, accessible UI design
- Complete end-to-end food rescue workflow

**Start using it today to make a difference in your community! 🌱**
