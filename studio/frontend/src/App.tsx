import {
  BrowserRouter,
  Routes,
  Route,
} from 'react-router-dom'


import KnowledgeDashboard from './pages/KnowledgeDashboard'

import AssistantPage from './pages/assistant/AssistantPage'



function App() {

  return (

    <BrowserRouter>

      <Routes>


        <Route

          path="/"

          element={
            <KnowledgeDashboard />
          }

        />



        <Route

          path="/assistant"

          element={
            <AssistantPage />
          }

        />


      </Routes>

    </BrowserRouter>

  )

}


export default App
