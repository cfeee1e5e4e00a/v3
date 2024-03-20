import { FC } from 'react';

import { MeasurementDisplay } from '@/features/measurements/MeasurementDisplay';
import { useFlatMeasurement } from '@/features/flat/useFlatMeasurement';
import { MeasurementType } from '@/features/measurements/Measurement';
import { useUser } from '@/features/user/useUser';

export const FlatHumidityChart: FC = () => {
    const user = useUser();
    const data = useFlatMeasurement<number>(() =>
        user.data
            ? {
                  flat: 1,
                  measurement: MeasurementType.HUMIDITY,
                  start: '-20m',
                  stop: 'now()',
                  window: '1m',
              }
            : null,
    );

    return (
        <MeasurementDisplay<number>
            data={data.data}
            label="Влажность в %"
            title={`Влажность в квартире`}
        />
    );
};
