import React, { Suspense } from 'react'
import ReactDOM from 'react-dom/client'
import './styles/globals.css'

// Lazy load full app
const App = React.lazy(() => import('./App.jsx'))

// Loading fallback
function LoadingScreen() {
  return (
    <div style={{ 
      width: '100vw', 
      height: '100vh', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center',
      background: '#F8F5ED',
      fontFamily: 'Inter, sans-serif',
      flexDirection: 'column',
      gap: '20px'
    }}>
      <div style={{ textAlign: 'center' }}>
        <h2 style={{ color: '#3F654A', fontSize: '32px', margin: '0 0 10px 0' }}>🌱 ANNASARTHI AI</h2>
        <p style={{ color: '#829B78', fontSize: '14px', margin: '0' }}>Loading dashboard...</p>
      </div>
    </div>
  )
}

const rootElement = document.getElementById('root')
if (rootElement) {
  rootElement.innerHTML = ''
}

const root = ReactDOM.createRoot(rootElement)
root.render(
  <React.StrictMode>
    <Suspense fallback={<LoadingScreen />}>
      <App />
    </Suspense>
  </React.StrictMode>
)
