import { FC } from 'react';

import { useUser } from '@/entities/user/useUser';

export const DashboardIndexPage: FC = () => {
    const me = useUser();

    return (
        <main className="h-full w-full">
            {me.data && JSON.stringify(me.data)}
        </main>
    );
};
