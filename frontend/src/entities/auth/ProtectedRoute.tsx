import { authToken } from '@/entities/auth';
import { FC, ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router-dom';

type Props = {
    children: ReactNode;
    redirectTo?: string;
    inverse?: boolean;
};

export const ProtectedRoute: FC<Props> = ({
    children,
    redirectTo = '/signin',
    inverse = false,
}) => {
    const location = useLocation();

    if (!authToken.value || inverse) {
        return <Navigate to={redirectTo} state={{ from: location }} replace />;
    }

    return children;
};
