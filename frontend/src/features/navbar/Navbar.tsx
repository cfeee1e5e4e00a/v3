import { FC, useMemo } from 'react';
import { Link } from 'react-router-dom';

import { Role } from '@/features/user/User';
import { UserShortInfo } from '@/features/user/UserShortInfo';
import { useUser } from '@/features/user/useUser';
import { HomeIcon, BanknotesIcon, UserIcon } from '@heroicons/react/24/outline';

const items = [
    {
        displayName: 'Моя квартира',
        icon: <HomeIcon />,
        to: '/dashboard/my/flat',
        roles: [Role.USER_FLOOR_1, Role.USER_FLOOR_2],
    },
    {
        displayName: 'Счёта',
        icon: <BanknotesIcon />,
        to: '/dashboard/my/bills',
        roles: [Role.USER_FLOOR_1, Role.USER_FLOOR_2],
    },
    {
        displayName: 'Дом',
        icon: <HomeIcon />,
        to: '/dashboard/admin/house',
        roles: [Role.ADMIN],
    },
    {
        displayName: 'Пользователи',
        icon: <UserIcon />,
        to: '/dashboard/admin/users',
        roles: [Role.ADMIN],
    },
];

export const Navbar: FC = () => {
    const user = useUser();

    const owned = useMemo(
        () =>
            items.filter(
                ({ roles }) =>
                    user.data?.role && roles.includes(user.data?.role),
            ),
        [user.data?.role],
    );

    return (
        <nav className="bg-accent text-accent-content sticky top-0 flex h-screen flex-col items-center justify-between gap-8 p-6">
            <Link to="/dashboard" className="text-2xl">
                cfee
            </Link>
            {user.data?.role && (
                <ul className="flex flex-col items-center gap-4">
                    {owned.map(({ displayName, icon, to }) => (
                        <Link to={to} key={to}>
                            <li className="flex flex-col items-center gap-2 text-center">
                                <span className="h-8 w-8">{icon}</span>
                                <span>{displayName}</span>
                            </li>
                        </Link>
                    ))}
                </ul>
            )}
            <div className="flex h-full flex-col justify-end">
                {user.data && <UserShortInfo user={user.data} />}
            </div>
        </nav>
    );
};
