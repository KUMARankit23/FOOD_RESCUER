# 🍽️ Food Rescue Multi-Agent System

A complete food rescue platform connecting donors, delivery agents, and recipients through real-time tracking and AI-powered optimization.

## ✨ Features

- **Interactive Map Location Picker** - Click/search/GPS to select food pickup location
- **Real-Time Delivery Tracking** - Live map visualization with vehicle position, ETA, and progress
- **AI Agent Chat** - Real-time communication with automatic status updates
- **Live Tracking Timeline** - 6-step progress visualization (Location → Safety → Dispatch → Pickup → Delivery → Complete)
- **Recipient Status Updates** - Confirm receipt and provide feedback
- **Run History & Analytics** - Track all food rescues with decision/recipient/time/duration info
- **Responsive Design** - Works on desktop and mobile
- **Form Validation** - React Hook Form + Zod validation

## 🏗️ Tech Stack

**Frontend:**
- React 18 + Vite
- TailwindCSS + Framer Motion
- Leaflet (Maps)
- React Hook Form + Zod
- TanStack Query
- Zustand

**Backend:**
- FastAPI (Python)
- Multi-Agent System
- CORS enabled
- Real-time processing

## 📦 Installation

### Prerequisites
- Node.js 16+
- Python 3.10+
- Git

### Setup

1. **Clone repository**
```bash
git clone https://github.com/KUMARankit23/FOOD_RESCUE.git
cd FOOD_RESCUE
```

2. **Backend Setup**
```bash
pip install -r requirements.txt
python api.py
# Backend runs on http://localhost:8000
```

3. **Frontend Setup**
```bash
cd frontend_react
npm install
npm run dev
# Frontend runs on http://localhost:3000
```

## 🚀 Deployment

### Railway.app (Recommended - Free)

1. Push to GitHub
2. Go to railway.app
3. Click "Deploy from GitHub"
4. Select this repository
5. Railway auto-detects Python + Node
6. Deploy!

### Docker

```bash
docker build -t food-rescue .
docker run -p 8000:8000 -p 3000:3000 food-rescue
```

### Environment Variables

Create `.env` file:
```
BACKEND_PORT=8000
VITE_API_URL=http://localhost:8000
PYTHONUNBUFFERED=1
```

## 📱 Usage

### For Donors (Food Submitters)

1. Go to **Submit Report** page
2. Fill food details (type, quantity, prep time, temperature)
3. **Click on map to select pickup location** or search/use GPS
4. Set pickup deadline
5. Submit
6. Track on **Operations** page
7. Watch delivery on **Map** page

### For Recipients

1. Go to **Operations** page
2. View available food rescues
3. Click any run to see details
4. Watch live tracking
5. Update status when received
6. Provide feedback

### Admin/Developer

1. View **API Docs**: http://localhost:8000/docs
2. Check **Dashboard**: Analytics and metrics
3. Monitor all operations in real-time

## 📊 API Endpoints

```
POST   /api/v1/reports           - Submit food report
GET    /api/v1/runs              - List all runs
GET    /api/v1/runs/{run_id}     - Get specific run
GET    /api/v1/runs/{run_id}/trace - Get agent trace
GET    /api/v1/recipients        - List recipients
GET    /health                   - Health check
```

## 🗂️ Project Structure

```
.
├── api.py                          # FastAPI backend
├── main.py                         # Agent orchestration
├── agents.py                       # AI agents
├── schemas.py                      # Data models
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker config
├── docker-compose.yml              # Multi-container setup
├── frontend_react/                 # React frontend
│   ├── src/
│   │   ├── components/             # Reusable components
│   │   ├── pages/                  # Page components
│   │   ├── hooks/                  # Custom hooks
│   │   ├── services/               # API services
│   │   └── utils/                  # Utilities
│   ├── package.json                # Node dependencies
│   └── vite.config.js              # Vite config
└── README.md                       # This file
```

## 🎯 Key Pages

| Page | Path | Purpose |
|------|------|---------|
| Submit Report | /submit | Donors submit food with location |
| Operations | /operations | Track runs with timeline & chat |
| Map Tracking | /map | Live delivery map visualization |
| Dashboard | / | System overview & KPIs |
| Analytics | /analytics | Performance metrics |
| Knowledge Base | /knowledge | RAG-powered search |

## 🔐 Security

- CORS configured for authorized domains
- Input validation on all forms
- Environment variables for sensitive data
- HTTPS ready (use Let's Encrypt for free SSL)

## 📈 Scaling

- Replace in-memory database with PostgreSQL
- Add Redis for caching
- Implement WebSocket for real-time updates
- Scale frontend on Vercel/Netlify
- Scale backend on Railway/Render

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📝 License

MIT License - see LICENSE file

## 🙋 Support

For issues, questions, or suggestions:
1. Check existing issues on GitHub
2. Create new issue with details
3. Join community discussions

## 🚀 Status

✅ **Production Ready**

All features implemented:
- ✅ Interactive map location picker
- ✅ Real-time tracking with live map
- ✅ Agent chat system
- ✅ Form validation
- ✅ Recipient feedback
- ✅ Complete workflow
- ✅ Deployment ready

---

**Ready to deploy!** Follow the Deployment section above to go live in 5 minutes.
