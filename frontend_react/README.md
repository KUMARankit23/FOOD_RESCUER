# ANNASARTHI AI - React Frontend

A modern, production-ready React.js frontend for the Food Rescue Multi-Agent System.

## Features

### 🎨 Design System
- **Warm Visual Identity**: Cream (#F8F5ED), Forest Green (#3F654A), Terracotta (#C77C55), Sage (#829B78)
- **Accessibility**: WCAG 2.2 AA compliant (where practical)
- **Responsive Design**: Desktop, tablet, mobile optimized
- **Smooth Animations**: Framer Motion for delightful micro-interactions

### 📱 Pages
1. **Dashboard** - Real-time KPIs, activity charts, decision distribution
2. **Submit Food** - Form-based food report submission with validation
3. **Operations** - Run history, agent execution timeline, trace viewer
4. **Analytics** - Performance metrics, agent accuracy, system health
5. **Live Map** - Geographical visualization of dispatches, donors, recipients
6. **Knowledge Base** - RAG-powered food safety search interface

### 🔧 Tech Stack
- **React 18** - UI framework
- **Vite** - Lightning-fast build tool
- **React Router** - Client-side routing
- **TanStack Query** - Server state management
- **Zustand** - Client state management
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Animation library
- **Recharts** - Data visualization
- **React Leaflet** - Map integration
- **React Hook Form** - Form handling
- **Zod** - Schema validation
- **Lucide React** - Icon library

## Quick Start

### Prerequisites
- Node.js 18+ and npm

### Installation

```bash
cd frontend_react
npm install
```

### Configuration

Create a `.env` file in `frontend_react/`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

### Development

```bash
npm run dev
```

App will be available at `http://localhost:5173`

### Production Build

```bash
npm run build
npm run preview
```

## Project Structure

```
frontend_react/
├── src/
│   ├── components/
│   │   ├── common/       # Reusable components (Button, Card, etc.)
│   │   ├── layout/       # Sidebar, Navbar, PageContainer
│   │   ├── charts/       # Recharts wrappers
│   │   ├── operations/   # Agent timeline, run table
│   │   ├── forms/        # Form components
│   │   ├── maps/         # Map visualizations
│   │   └── knowledge/    # Knowledge base components
│   ├── pages/            # Page components (Dashboard, Submit, etc.)
│   ├── hooks/            # Custom React hooks (useReports, useAnalytics, etc.)
│   ├── services/         # API client and report service
│   ├── store/            # Zustand store for global state
│   ├── utils/            # Constants, helpers
│   ├── styles/           # Global CSS
│   ├── assets/           # Images, fonts
│   ├── App.jsx           # Main app component with routing
│   └── main.jsx          # Entry point
├── index.html            # HTML template
├── package.json          # Dependencies
├── vite.config.js        # Vite configuration
├── tailwind.config.js    # Tailwind CSS config
└── postcss.config.js     # PostCSS config
```

## Component Library

### Common Components
- `Button` - Primary, secondary, outline, danger, ghost variants
- `MetricCard` - KPI display with trend
- `StatusBadge` - Status indicators
- `SectionHeader` - Section titles
- `EmptyState` - Empty state messaging
- `LoadingState` - Loading skeleton
- `ErrorState` - Error messaging
- `SearchInput` - Search field
- `Tabs` - Tabbed interface

### Chart Components
- `RescueActivityChart` - Line/Area chart
- `FoodCategoryChart` - Pie chart
- `AgentPerformanceChart` - Bar chart

### Operation Components
- `AgentExecutionTimeline` - Visual timeline
- `RunHistoryTable` - Run history table
- `DispatchTable` - Dispatch records
- `DecisionCard` - Decision display

### Layout Components
- `AppSidebar` - Navigation sidebar with collapse
- `TopNavbar` - Top navigation bar
- `PageContainer` - Main page wrapper
- `Breadcrumbs` - Navigation breadcrumbs

## Custom Hooks

- `useSubmitReport()` - Submit food report
- `useListRuns()` - Fetch all runs
- `useGetRun(runId)` - Fetch specific run
- `useGetRunTrace(runId)` - Fetch run trace
- `useEvaluationSummary()` - Fetch evaluation metrics
- `useRecipients()` - Fetch recipient list
- `useMapTracking()` - Real-time dispatch tracking
- `useMapStatistics()` - Map route statistics
- `useDispatchHistory()` - Dispatch history
- `useDonorLocations()` - Donor locations
- `useRecipientLocations()` - Recipient locations

## Global State (Zustand)

The `appStore` manages:
- Sidebar open/close state
- Filter state (decision, agent, date range)
- Selected run for detail view
- Connection status
- Last update timestamp

```javascript
import { useAppStore } from './store/appStore';

const { sidebarOpen, setSidebarOpen } = useAppStore();
```

## API Integration

### Base URL
Configured via `VITE_API_BASE_URL` environment variable (defaults to `http://localhost:8000`)

### Endpoints Used
- `POST /api/v1/reports` - Submit food report
- `GET /api/v1/runs` - List all runs
- `GET /api/v1/runs/{id}` - Get run details
- `GET /api/v1/runs/{id}/trace` - Get agent trace
- `GET /api/v1/evaluate/summary` - Get evaluation metrics
- `GET /api/v1/recipients` - List recipients
- `GET /api/v1/map/tracking` - Real-time dispatch tracking
- `GET /api/v1/map/statistics` - Route statistics
- `GET /api/v1/map/history` - Dispatch history
- `GET /api/v1/map/donors` - Donor locations
- `GET /api/v1/map/recipients` - Recipient locations
- `GET /api/v1/safety/retrieve` - RAG-based knowledge retrieval

## Styling

### Tailwind CSS
- Custom color palette aligned with design system
- Responsive grid system
- Custom scrollbar styling
- Focus states for accessibility
- Smooth transitions

### Framer Motion
- Page transitions
- Component entrance animations
- Hover effects
- Micro-interactions on buttons and cards

## Form Validation

Uses `react-hook-form` + `zod` for robust validation:

```javascript
const reportSchema = z.object({
  food_type: z.string().min(1),
  quantity: z.coerce.number().min(1),
  // ...
});

const { control, handleSubmit, formState: { errors } } = useForm({
  resolver: zodResolver(reportSchema),
});
```

## State Management

### Server State (TanStack Query)
- Queries auto-refetch at intervals
- Automatic caching and deduplication
- Built-in error handling and retry logic

### Client State (Zustand)
- UI state (sidebar, modals)
- Filters and selections
- Connection status

## Performance Optimizations

1. **Code Splitting** - React Router lazy routes
2. **Image Optimization** - SVG icons via Lucide
3. **Query Caching** - TanStack Query stale time
4. **Component Memoization** - useMemo for expensive computations
5. **CSS Optimization** - Tailwind purging unused styles

## Accessibility

- Semantic HTML elements
- ARIA labels where needed
- Keyboard navigation
- Color contrast compliance
- Focus states for all interactive elements

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Troubleshooting

### API Connection Issues
- Verify backend is running on `http://localhost:8000`
- Check `VITE_API_BASE_URL` in `.env`
- Check browser console for network errors

### Styling Issues
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Rebuild Tailwind CSS: `npm run build`

### Build Issues
- Ensure Node.js 18+ is installed
- Clear Vite cache: `rm -rf .vite`

## Development Commands

```bash
npm run dev        # Start development server
npm run build      # Build for production
npm run preview    # Preview production build locally
npm run lint       # Run ESLint
```

## Contributing

1. Follow the component structure in `src/components/`
2. Use Tailwind CSS for styling
3. Add proper TypeScript comments
4. Test API integration thoroughly
5. Ensure responsive design

## License

MIT
