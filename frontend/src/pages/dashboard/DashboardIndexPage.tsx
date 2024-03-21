import { FC } from 'react';
import { Navigate } from 'react-router-dom';

import { useUser } from '@/features/user/useUser';
import { Role } from '@/features/user/User';

export const DashboardIndexPage: FC = () => {
    const user = useUser();

    if (user.isLoading || !user.data) {
        return null;
    }

    const dest =
        user.data.role == Role.ADMIN
            ? '/dashboard/admin/house'
            : '/dashboard/my/flat';

    return <Navigate to={dest} />;
};
