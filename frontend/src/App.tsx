import {BrowserRouter} from "react-router";
import AppRouter from "./components/AppRouter.tsx";
import {ThemeProvider} from "./contexts/ThemeContext.tsx";

function App() {
    return (
        <ThemeProvider>
            <BrowserRouter>
                <AppRouter/>
            </BrowserRouter>
        </ThemeProvider>
    )
}

export default App
