import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import App from './App'
import './styles/global.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
      <Toaster
        position="bottom-right"
        toastOptions={{
          style: {
            background: '#0D1520',
            color: '#E8F4FF',
            border: '1px solid #1A2D45',
            fontFamily: 'DM Mono, monospace',
            fontSize: '0.82rem',
          },
          success: { iconTheme: { primary: '#10B981', secondary: '#0D1520' } },
          error:   { iconTheme: { primary: '#EF4444', secondary: '#0D1520' } },
        }}
      />
    </BrowserRouter>
  </React.StrictMode>
)
