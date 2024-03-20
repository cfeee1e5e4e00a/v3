import { FC } from 'react';

import { FlatTemperatureChart } from '@/features/flat/FlatTemperatureChart';
import { FlatCurrentChart } from '@/features/flat/FlatCurrentChart';
import { FlatHumidityChart } from '@/features/flat/FlatHumidityChart';

export const DashboardMyFlatPage: FC = () => {
    return (
        <main className="grid h-full w-full grid-cols-2 grid-rows-3 gap-4">
            <FlatTemperatureChart />
            <FlatHumidityChart />
            <FlatCurrentChart />
        </main>
    );
};
