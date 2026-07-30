import {
  Navigate,
  Route,
  Routes,
} from 'react-router-dom'

import { StudioLayout } from './components/layout/StudioLayout'
import { CommandsPage } from './pages/CommandsPage'
import { DashboardPage } from './pages/DashboardPage'
import { ProjectsPage } from './pages/ProjectsPage'

export default function App() {
  return (
    <StudioLayout>
      <Routes>
        <Route
          element={<DashboardPage />}
          path="/"
        />

        <Route
          element={<ProjectsPage />}
          path="/projects"
        />

        <Route
          element={<CommandsPage />}
          path="/commands"
        />

        <Route
          element={<Navigate replace to="/" />}
          path="*"
        />
      </Routes>
    </StudioLayout>
  )
}
