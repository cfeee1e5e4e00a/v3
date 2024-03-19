import { FC } from 'react';

import { DisplayGraphic } from '@/features/display-graphic/DisplayGraphic';

export const DashboardMyFlatPage: FC = () => {
    return (
        <main className="grid h-full w-full grid-cols-2 grid-rows-3">
            <DisplayGraphic />
        </main>
    );
};
