import { FC, ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router-dom';

import { useAuthToken } from '@/entities/auth';

type Props = {
    children: ReactNode;
    redirectTo?: string;
    inverse?: boolean;
};

export const AuthProtectedRoute: FC<Props> = ({
    children,
    redirectTo = '/signin',
    inverse = false,
}) => {
    const location = useLocation();
    const authToken = useAuthToken();

    if (authToken.isLoading || authToken.data === undefined) {
        return null;
    }

    if (inverse) {
        if (authToken.data) {
            return (
                <Navigate to={redirectTo} state={{ from: location }} replace />
            );
        }
    } else {
        if (!authToken.data) {
            return (
                <Navigate to={redirectTo} state={{ from: location }} replace />
            );
        }
    }

    return children;
};
