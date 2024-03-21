import { FC } from 'react';
import { useNavigate } from 'react-router-dom';

import { useLogoutMutation } from '@/features/auth/useLogoutMutation';
import { Role, User } from '@/features/user/User';

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

    const floor =
        user.role === Role.USER_FLOOR_1
            ? 1
            : user.role === Role.USER_FLOOR_2
              ? 2
              : null;

    return (
        <div className="flex flex-col items-center gap-4 text-center">
            <span>{user.name}</span>
            {user.role !== Role.ADMIN && (
                <>
                    <span>Квартира - {user.flat}</span>
                    <span>Этаж - {floor}</span>
                </>
            )}
            <button onClick={onLogoutClick}>Выйти</button>
        </div>
    );
};
