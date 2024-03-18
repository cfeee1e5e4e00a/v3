import { FC } from 'react';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';

import { BaseLayout } from '@/shared/ui/BaseLayout';
import { ProtectedRoute } from '@/entities/auth/ProtectedRoute';
import { IndexPage } from '@/pages/IndexPage';
import { SignInPage } from '@/pages/SignInPage';
import { DashboardIndexPage } from '@/pages/dashboard/DashboardIndexPage';

const router = createBrowserRouter([
    {
        path: '/',
        element: (
            <ProtectedRoute redirectTo="/dashboard" inverse>
                <IndexPage />
            </ProtectedRoute>
        ),
    },
    {
        path: '/dashboard',
        element: (
            <ProtectedRoute>
                <BaseLayout />
            </ProtectedRoute>
        ),
        children: [
            {
                index: true,
                element: <DashboardIndexPage />,
            },
            {
                path: 'sensors',
                element: <main>sensors</main>,
            },
        ],
    },
    {
        path: '/signin',
        element: (
            <ProtectedRoute redirectTo="/dashboard" inverse>
                <SignInPage />
            </ProtectedRoute>
        ),
    },
]);

export const RouterEntry: FC = () => {
    return <RouterProvider router={router} />;
};
