import { FC, ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router-dom';

import { Role } from '@/features/user/User';
import { useUser } from '@/features/user/useUser';

type Props = {
    children: ReactNode;
    redirectTo?: string;
    roles?: Array<Role>;
};

export const RoleProtectedRoute: FC<Props> = ({
    children,
    redirectTo = '/401',
    roles,
}) => {
    const location = useLocation();
    const user = useUser();

    if (user.isLoading || !user.data) {
        return null;
    }

    if (user.data.role && !roles?.includes(user.data.role)) {
        return <Navigate to={redirectTo} state={{ from: location }} replace />;
    }

    return children;
};
