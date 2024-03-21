import { FC } from 'react';
import {
    Navigate,
    Outlet,
    RouterProvider,
    createBrowserRouter,
} from 'react-router-dom';

import { DashboardLayout } from '@/features/navbar/DashboardLayout';
import { AuthProtectedRoute } from '@/features/auth/AuthProtectedRoute';
import { RoleProtectedRoute } from '@/features/auth/RoleProtectedRoute';
import { Role } from '@/features/user/User';
import { IndexPage } from '@/pages/IndexPage';
import { SignInPage } from '@/pages/SignInPage';
import { DashboardIndexPage } from '@/pages/dashboard/DashboardIndexPage';
import { DashboardMyFlatPage } from '@/pages/dashboard/my/DashboardMyFlatPage';
import { NotFoundPage } from '@/pages/NotFoundPage';
import { ForbiddenPage } from '@/pages/ForbiddenPage';
import { DashboardAdminHousePage } from '@/pages/dashboard/admin/DashboardAdminHousePage';

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
                    <RoleProtectedRoute
                        roles={[Role.USER_FLOOR_1, Role.USER_FLOOR_2]}
                    >
                        <Outlet />
                    </RoleProtectedRoute>
                ),
                children: [
                    {
                        path: 'flat',
                        element: <DashboardMyFlatPage />,
                    },
                    {
                        path: 'bills',
                        element: <main>My bills</main>,
                    },
                ],
            },
            {
                path: 'admin',
                element: (
                    <RoleProtectedRoute roles={[Role.ADMIN]}>
                        <Outlet />
                    </RoleProtectedRoute>
                ),
                children: [
                    {
                        path: 'users',
                        element: <Outlet />,
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
                                <DashboardAdminHousePage />
                            </RoleProtectedRoute>
                        ),
                    },
                ],
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
