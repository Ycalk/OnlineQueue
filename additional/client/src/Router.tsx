import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import HomePage from './pages/HomePage';
import MyQueue from './pages/MyQueue';
import MyApplication from './pages/MyApplication';
import RecoveryPass from './pages/RecoveryPassword';
import NewPass from './pages/NewPassword';

const router = createBrowserRouter([
    {
        path: '/',
        element: <HomePage />,
    },
    {
        path: '/queue/my',
        element: <MyQueue />,
    },
    {
        path: '/application/my',
        element: <MyApplication />,
    },
    {
        path: '/password/recovery',
        element: <RecoveryPass />,
    },
    {
        path: '/password/new',
        element: <NewPass />,
    },
]);

export function Router() {
    return <RouterProvider router={router} />;
}
