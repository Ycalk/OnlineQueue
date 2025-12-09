import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import HomePage from './pages/Home.page';
import MyQueue from './pages/MyQueue';
import MyApplication from './pages/MyApplication';
import RegisterPage from './pages/RegisterPage';
import AuthPage from './pages/AuthPage';
import RecoveryPass from './pages/RecoveryPassword';
import NewPass from './pages/NewPassword';
import Notification from './pages/Notification';
import ReturnToEnter from './pages/ReturnToEnter';

const router = createBrowserRouter([
  {
    path: '/',
    element: <HomePage />,
  },
  {
    path: '/my-queue',
    element: <MyQueue />,
  },
  {
    path: '/my-application',
    element: <MyApplication />,
  },
  {
    path: '/regstration',
    element: <RegisterPage />,
  },
  {
    path: '/authorisation',
    element: <AuthPage />,
  },
  {
    path: '/recovery-password',
    element: <RecoveryPass />,
  },
  {
    path: '/new-password',
    element: <NewPass />,
  },
  {
    path: '/notification',
    element: <Notification />,
  },
  {
    path: '/return',
    element: <ReturnToEnter />,
  },
]);

export function Router() {
  return <RouterProvider router={router} />;
}
