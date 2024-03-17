import { FC } from 'react';

import { TeamName } from '@/shared/ui/TeamName';

export const IndexPage: FC = () => {
    return (
        <main className="flex h-full w-full flex-col items-center justify-center gap-12">
            <h1 className="text-4xl">
                <TeamName />
            </h1>
            <button className="flex items-center justify-center rounded-xl border border-gray-200 bg-white px-12 py-3 text-2xl duration-100 hover:bg-green-400">
                Войти
            </button>
        </main>
    );
};
