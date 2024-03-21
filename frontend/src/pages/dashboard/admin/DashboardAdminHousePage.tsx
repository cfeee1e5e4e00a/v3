import { FC } from 'react';

import { HouseMeasurementChart } from '@/features/house/HouseMeasurementChart';
import { MeasurementType } from '@/features/measurements/Measurement';
import { HouseMeasurementGauge } from '@/features/house/HouseMeasurementGauge';
import { HouseFlatTargetTemperatureControl } from '@/features/house/HouseFlatTargetTemperatureControl';

export const DashboardAdminHousePage: FC = () => {
    return (
        <main className="h-full w-full">
            <div className="grid grid-cols-4 grid-rows-7 gap-1">
                {Array.from({ length: 6 }, (_, i) => i + 1).map((flat) => (
                    <>
                        <HouseMeasurementChart
                            key={`/flats/${flat}/temp`}
                            flat={flat}
                            measurement={MeasurementType.TEMPERATURE}
                            label="Температура в °C"
                            title={`Температура в квартире ${flat}`}
                        />
                        <HouseMeasurementChart
                            key={`/flats/${flat}/humd`}
                            flat={flat}
                            measurement={MeasurementType.HUMIDITY}
                            label="Влажность в %"
                            title={`Влажность в квартире ${flat}`}
                        />
                        <HouseMeasurementChart
                            key={`/flats/${flat}/curr`}
                            flat={flat}
                            measurement={MeasurementType.CURRENT}
                            label="Потребление тока в А"
                            title={`Потрбление тока в квартире ${flat}`}
                        />
                        <div
                            className="grid grid-cols-1 grid-rows-2 gap-1"
                            key={`/flats/${flat}/gauges`}
                        >
                            <HouseMeasurementGauge
                                flat={flat}
                                measurement={MeasurementType.TEMPERATURE}
                                title={`Текущая температура в квартире ${flat}`}
                                unit="°C"
                            />
                            <HouseMeasurementGauge
                                flat={flat}
                                measurement={MeasurementType.TARGET_TEMPERATURE}
                                title={`Целевая температура в квартире ${flat}`}
                                unit="°C"
                            />
                            <HouseFlatTargetTemperatureControl flat={flat} />
                        </div>
                    </>
                ))}
            </div>
        </main>
    );
};
