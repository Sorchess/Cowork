import {Navigate, Route, Routes} from 'react-router';
import { publicRoutes, privateRoutes } from "../router";

const AppRouter = () => {
    const isAuthenticated: boolean = false;
    return (
        isAuthenticated
            ?
            <Routes>
                {privateRoutes.map(route =>
                    <Route
                        path={route.path}
                        element={route.component()}
                        key={route.path}
                    />
                )}
                <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
            :
            <Routes>
                {publicRoutes.map(route =>
                    <Route
                        index={route.index}
                        path={route.path}
                        element={route.component()}
                        key={route.path}
                    />
                )}
                <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>



    );
};

export default AppRouter;