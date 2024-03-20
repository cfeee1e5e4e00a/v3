import { FC } from 'react';

import { useUser } from '@/entities/user/useUser';

export const DashboardIndexPage: FC = () => {
    const me = useUser();

    if (me.isLoading || !me.data) {
        return (
            <main className="flex h-full w-full items-center justify-center">
                Загрузка
            </main>
        );
    }

    return (
        <main className="h-full w-full">
            <h1 className="p-16 text-4xl">Приветствуем, {me.data.name}!</h1>
        </main>
    );
};
