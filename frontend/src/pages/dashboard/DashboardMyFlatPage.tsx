import { FC } from 'react';

import { MeasurementType } from '@/features/measurements/Measurement';
import { FlatMeasurementChart } from '@/features/flat/FlatMeasurementChart';
import { FlatMeasurementGauge } from '@/features/flat/FlatMeasurementGauge';

export const DashboardMyFlatPage: FC = () => {
    return (
        <main className="grid h-full w-full grid-cols-2 grid-rows-3 gap-4">
            <FlatMeasurementChart
                measurement={MeasurementType.TEMPERATURE}
                label="Температура в °C"
                title="Температура в квартире"
            />
            <FlatMeasurementGauge
                measurement={MeasurementType.TEMPERATURE}
                title="Текущая температура в квартире"
                unit="°C"
            />
            <FlatMeasurementChart
                measurement={MeasurementType.HUMIDITY}
                label="Влажность в %"
                title="Влажность в квартире"
            />
            <FlatMeasurementChart
                measurement={MeasurementType.CURRENT}
                label="Потребление тока в А"
                title="Потрбление тока в квартире"
            />
        </main>
    );
};
