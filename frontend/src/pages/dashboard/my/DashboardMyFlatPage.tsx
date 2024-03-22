import { FC } from 'react';

import { MeasurementType } from '@/features/measurements/Measurement';
import { FlatMeasurementChart } from '@/features/flat/FlatMeasurementChart';
import { FlatMeasurementGauge } from '@/features/flat/FlatMeasurementGauge';
import { FlatTargetTemperatureControl } from '@/features/flat/FlatTargetTemperatureControl';
import { useUser } from '@/features/user/useUser';
import { SetTemperatureScheduleForm } from '@/features/flat/SetTemperatureScheduleForm';
import { Role } from '@/features/user/User';

export const DashboardMyFlatPage: FC = () => {
    const user = useUser();

    if (!user.data) {
        return null;
    }

    return (
        <main className="grid w-full grid-cols-2 grid-rows-2 gap-4">
            <FlatMeasurementChart
                measurement={MeasurementType.TEMPERATURE}
                label="Температура в °C"
                title="Температура в квартире"
            />
            <div className="grid grid-cols-1 grid-rows-3 gap-4">
                <FlatMeasurementGauge
                    measurement={MeasurementType.TEMPERATURE}
                    title="Текущая температура в квартире"
                    unit="°C"
                />
                <FlatMeasurementGauge
                    measurement={MeasurementType.TARGET_TEMPERATURE}
                    title="Целевая температура в квартире"
                    unit="°C"
                />
                <FlatTargetTemperatureControl />
            </div>
            <FlatMeasurementChart
                measurement={MeasurementType.HUMIDITY}
                label="Влажность в %"
                title="Влажность в квартире"
            />
            {user.data.role === Role.USER_FLOOR_1 && (
                <SetTemperatureScheduleForm flat={user.data.flat} />
            )}
            <FlatMeasurementChart
                measurement={MeasurementType.CURRENT}
                label="Потребление тока в А"
                title="Потрбление тока в квартире"
            />
        </main>
    );
};
