import { FC } from 'react';
import { useNavigate } from 'react-router-dom';

import { useLogoutMutation } from '@/features/logout/useLogoutMutation';
import { User } from '@/entities/user/User';

type Props = {
    user: User;
};

export const UserShortInfo: FC<Props> = ({ user }) => {
    const navigate = useNavigate();
    const logoutMutation = useLogoutMutation();

    const onLogoutClick = async () => {
        await logoutMutation.trigger();
        navigate('/');
    };

    return (
        <div className="flex flex-col items-center gap-4">
            <span>{user.name}</span>
            <button onClick={onLogoutClick}>Выйти</button>
        </div>
    );
};
