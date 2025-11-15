import Welcome from "../pages/Welcome.tsx";
import Auth from "../pages/Auth.tsx";
import Recover from "../pages/Recover.tsx";

export const privateRoutes = [
    {path: "/", component: Welcome, index: false },
]

export const publicRoutes = [
    {path: "/", component: Welcome, index: false },
    {path: "/recover", component: Recover, index: false },
    {path: "/auth", component: Auth, index: false },
]