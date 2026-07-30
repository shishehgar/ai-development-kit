import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'

import App from './App'
import { StudioThemeProvider } from './providers/StudioThemeProvider'

document.documentElement.lang = 'fa'
document.documentElement.dir = 'rtl'
document.title = 'AIDK Studio'

createRoot(
  document.getElementById('root')!,
).render(
  <StrictMode>
    <StudioThemeProvider>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </StudioThemeProvider>
  </StrictMode>,
)
