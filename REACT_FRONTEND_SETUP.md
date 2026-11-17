# ANNASARTHI AI - React Frontend Setup Guide

## Overview

The React frontend is a complete modern web application for the Food Rescue Multi-Agent System. This guide covers setup, running, and development.

## Prerequisites

- **Node.js**: 18.0.0 or later (check with `node --version`)
- **npm**: 9.0.0 or later (check with `npm --version`)
- **Backend Service**: FastAPI running on `http://localhost:8000`

## Installation Steps

### Step 1: Navigate to Frontend Directory

```bash
cd "c:\Users\ankit\Downloads\food rescue mas\frontend_react"
```

### Step 2: Install Dependencies

```bash
npm install
```

This will install all required packages:
- React 18
- React Router for navigation
- TanStack Query for server state
- Tailwind CSS for styling
- Framer Motion for animations
- Recharts for data visualization
- And 15+ more essential libraries

**Installation time**: ~2-3 minutes (depends on internet speed)

### Step 3: Configure Environment

Create or update `.env` file:

```env
VITE_API_BASE_URL=http://localhost:8000
```

This tells the React app where to find the FastAPI backend.

## Running the Frontend

### Development Mode

```bash
npm run dev
```

**Output:**
```
  VITE v5.0.0  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

Open browser to `http://localhost:5173/`

### Production Build

```bash
npm run build
```

Generates optimized files in `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

Serves the production build locally for testing.

## Accessing the Application

### URL Structure

| Page | Route | Purpose |
|------|-------|---------|
| Dashboard | `/` | Overview, KPIs, charts |
| Submit Food | `/submit` | Report food surplus |
| Operations | `/operations` | Run history, agent timeline |
| Analytics | `/analytics` | Performance metrics |
| Live Map | `/map` | Geographic visualization |
| Knowledge Base | `/knowledge` | Food safety search |

### First Visit Checklist

1. ✅ Dashboard loads with KPI cards
2. ✅ Sidebar navigation works
3. ✅ Charts display (even if no data)
4. ✅ Submit Food form renders
5. ✅ All pages accessible

## Feature Walk-Through

### 1. Dashboard
- Real-time KPI metrics
- Activity trend charts
- Decision distribution pie chart
- Recent operations list

### 2. Submit Food Report
- Multi-step form with validation
- Food type and quantity
- Temperature safety check
- Location and timing fields
- Form validation with error messages

### 3. Operations
- Complete run history table
- Agent execution timeline
- Detailed run information panel
- Real-time updates

### 4. Analytics
- System performance metrics
- Agent accuracy comparison
- Response time analysis
- Dispatch rate trends

### 5. Live Map
- Active dispatch visualization
- Donor/recipient location markers
- Route statistics
- Dispatch history

### 6. Knowledge Base
- RAG-powered search
- Featured food safety guidelines
- Suggested searches
- Results with relevance scoring

## Backend Integration

### API Endpoints Connected

The frontend automatically calls these endpoints:

```
POST   /api/v1/reports              # Submit food report
GET    /api/v1/runs                 # List all operations
GET    /api/v1/runs/{id}            # Get specific run
GET    /api/v1/runs/{id}/trace      # Get agent execution trace
GET    /api/v1/evaluate/summary     # System metrics
GET    /api/v1/recipients           # Recipient directory
GET    /api/v1/map/tracking         # Real-time dispatch tracking
GET    /api/v1/map/statistics       # Route statistics
GET    /api/v1/map/history          # Dispatch history
GET    /api/v1/map/donors           # Donor locations
GET    /api/v1/map/recipients       # Recipient locations
GET    /api/v1/safety/retrieve      # Knowledge base search
```

### Real-Time Updates

The following data auto-refreshes:
- Runs list: Every 5 seconds
- Map tracking: Every 10 seconds
- Analytics: Every 30 seconds

## Development Workflow

### Making Changes

1. Edit source files in `src/`
2. Vite automatically hot-reloads in browser
3. Check browser console for errors
4. No manual rebuild needed during development

### Creating New Components

```javascript
// src/components/common/NewComponent.jsx
import React from 'react';
import { motion } from 'framer-motion';

export const NewComponent = ({ prop1, prop2 }) => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      {/* Component JSX */}
    </motion.div>
  );
};
```

### Adding New Pages

1. Create page in `src/pages/NewPage.jsx`
2. Export default component
3. Add route to `App.jsx`:

```javascript
import NewPage from './pages/NewPage';

<Route path="/newpage" element={<NewPage />} />
```

## Troubleshooting

### Issue: "Cannot GET /api/v1/reports"

**Solution**: Ensure backend is running
```bash
# In another terminal
python main.py
```

### Issue: Blank page with "VITE" logo

**Solution**: Wait for compilation to complete. Check browser console for errors.

### Issue: Styling looks broken

**Solution**: Rebuild Tailwind CSS
```bash
npm install
npm run dev
```

### Issue: Outdated data in UI

**Solution**: Data refreshes automatically. Force refresh with:
- Browser: `F5` or `Ctrl+Shift+R`
- Or click the refresh button in top-right navbar

### Issue: Port 5173 already in use

**Solution**: Stop other processes or run on different port
```bash
npm run dev -- --port 3000
```

## Performance Tips

1. **Use DevTools**: Open DevTools (F12) → Performance tab
2. **Check Network**: Tab shows API response times
3. **Monitor State**: React DevTools extension helpful
4. **Production Build**: Use `npm run build` for production

## File Structure

```
frontend_react/
├── src/
│   ├── components/          # Reusable React components
│   │   ├── common/          # Buttons, cards, badges
│   │   ├── layout/          # Sidebar, navbar
│   │   ├── charts/          # Data visualizations
│   │   └── operations/      # Timeline, tables
│   ├── pages/               # Full page components
│   ├── hooks/               # Custom React hooks
│   ├── services/            # API client
│   ├── store/               # Zustand state management
│   ├── utils/               # Constants, helpers
│   ├── styles/              # Global CSS
│   └── App.jsx              # Main app component
├── .env                     # Environment variables
├── vite.config.js           # Vite build config
├── tailwind.config.js       # Tailwind CSS config
└── package.json             # Dependencies
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+K` | Quick search (in future) |
| `Ctrl+S` | Save (IDE) |
| `F12` | Dev Tools |
| `Ctrl+Shift+R` | Hard refresh |

## Environment Variables

```env
# Required
VITE_API_BASE_URL=http://localhost:8000

# Optional (defaults to above)
# VITE_APP_NAME=ANNASARTHI AI
# VITE_LOG_LEVEL=info
```

## Debugging

### Enable Console Logging

Open DevTools → Console → See all logs

### Check Network Requests

DevTools → Network tab → Monitor API calls

### React DevTools Extension

1. Install from Chrome Web Store
2. Open DevTools → Components tab
3. Inspect component state and props

## Next Steps

1. **Test Submission**: Use Submit Food page to create a report
2. **View Operations**: Check Operations page for results
3. **Explore Analytics**: Review performance metrics
4. **Check Map**: Verify dispatch visualization
5. **Search Knowledge**: Try Knowledge Base search

## Common Tasks

### Reset All Data
1. Backend: Restart `main.py`
2. Frontend: Hard refresh with `Ctrl+Shift+R`

### Change API Endpoint
Edit `.env`:
```env
VITE_API_BASE_URL=http://your-new-url:8000
```
Restart dev server: `Ctrl+C` then `npm run dev`

### Build for Deployment

```bash
npm run build
# Outputs optimized files in dist/
```

Upload `dist/` folder to your hosting service.

## Support & Resources

- **React Docs**: https://react.dev
- **Tailwind CSS**: https://tailwindcss.com
- **Vite**: https://vitejs.dev
- **TanStack Query**: https://tanstack.com/query

## Deployment

### For Development Environment
- Keep running on local machine
- Backend must also be running

### For Production

1. Build optimized bundle:
```bash
npm run build
```

2. Deploy `dist/` folder to:
   - Vercel (recommended for React)
   - Netlify
   - AWS S3 + CloudFront
   - Any static hosting

3. Update backend API URL in environment variables

## License

MIT License - See LICENSE file for details
