import {
    BrowserRouter,
    Routes,
    Route,
} from "react-router-dom"


import KnowledgeDashboard
    from "./pages/KnowledgeDashboard"


import AssistantPage
    from "./pages/assistant/AssistantPage"


import {
    ProjectsPage,
} from "./pages/ProjectsPage"



export default function App(){

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


                <Route

                    path="/projects"

                    element={
                        <ProjectsPage />
                    }

                />


            </Routes>

        </BrowserRouter>

    )

}
