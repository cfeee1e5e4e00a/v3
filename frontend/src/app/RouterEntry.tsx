import { FC } from 'react';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';

import { BaseLayout } from '@/shared/ui/layouts/BaseLayout';
import { IndexPage } from '@/pages/IndexPage';

const router = createBrowserRouter([
    {
        path: '/',
        element: <IndexPage />,
    },
    {
        path: '/dashboard',
        element: <BaseLayout />,
        children: [
            {
                index: true,
                element: <main>Dashboard Home</main>,
            },
            {
                path: 'sensors',
                element: <main>sensors</main>,
            },
        ],
    },
    {
        path: '/login',
        element: <main>login</main>,
    },
]);

export const RouterEntry: FC = () => {
    return <RouterProvider router={router} />;
};
