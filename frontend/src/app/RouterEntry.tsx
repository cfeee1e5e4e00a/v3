import { FC } from 'react';
import {
    Navigate,
    Outlet,
    RouterProvider,
    createBrowserRouter,
} from 'react-router-dom';

import { DashboardLayout } from '@/features/navbar/DashboardLayout';
import { AuthProtectedRoute } from '@/entities/auth/AuthProtectedRoute';
import { RoleProtectedRoute } from '@/entities/auth/RoleProtectedRoute';
import { Role } from '@/entities/user/User';
import { IndexPage } from '@/pages/IndexPage';
import { SignInPage } from '@/pages/SignInPage';
import { DashboardIndexPage } from '@/pages/dashboard/DashboardIndexPage';
import { NotFoundPage } from '@/pages/NotFoundPage';
import { ForbiddenPage } from '@/pages/ForbiddenPage';

const router = createBrowserRouter([
    {
        path: '/',
        element: (
            <AuthProtectedRoute redirectTo="/dashboard" inverse>
                <IndexPage />
            </AuthProtectedRoute>
        ),
    },
    {
        path: '/dashboard',
        element: (
            <AuthProtectedRoute>
                <DashboardLayout />
            </AuthProtectedRoute>
        ),
        children: [
            {
                index: true,
                element: <DashboardIndexPage />,
            },
            {
                path: 'my',
                element: (
                    <RoleProtectedRoute roles={[Role.USER]}>
                        <Outlet />
                    </RoleProtectedRoute>
                ),
                children: [
                    {
                        path: 'flat',
                        element: <main>My flat</main>,
                    },
                    {
                        path: 'bills',
                        element: <main>My bills</main>,
                    },
                ],
            },
            {
                path: 'users',
                element: (
                    <RoleProtectedRoute roles={[Role.ADMIN]}>
                        <Outlet />
                    </RoleProtectedRoute>
                ),
                children: [
                    {
                        index: true,
                        element: <main>users list</main>,
                    },
                    {
                        path: ':user',
                        element: <main>users list</main>,
                    },
                ],
            },
            {
                path: 'house',
                element: (
                    <RoleProtectedRoute roles={[Role.ADMIN]}>
                        a
                    </RoleProtectedRoute>
                ),
            },
        ],
    },
    {
        path: '/signin',
        element: (
            <AuthProtectedRoute redirectTo="/dashboard" inverse>
                <SignInPage />
            </AuthProtectedRoute>
        ),
    },
    { path: '/404', element: <NotFoundPage /> },
    { path: '/401', element: <ForbiddenPage /> },
    { path: '*', element: <Navigate to="/404" /> },
]);

export const RouterEntry: FC = () => {
    return <RouterProvider router={router} />;
};
