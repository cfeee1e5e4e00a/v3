import { FC } from 'react';

import { MeasurementsGauge } from '@/features/measurements/MeasurementGauge';
import { useFlatMeasurement } from '@/features/flat/useFlatMeasurement';
import { MeasurementType } from '@/features/measurements/Measurement';
import { useUser } from '@/features/user/useUser';

type Props = {
    measurement: MeasurementType;
    title: string;
    unit: string;
};

export const FlatMeasurementGauge: FC<Props> = ({
    measurement,
    title,
    unit,
}) => {
    const user = useUser();
    const data = useFlatMeasurement<number>(() =>
        user.data
            ? {
                  flat: user.data.flat,
                  measurement,
                  start: '-1m',
                  stop: 'now()',
                  window: '1m',
              }
            : null,
    );

    return (
        <MeasurementsGauge<number>
            data={data.data?.at(data.data?.length - 1 ?? 0)}
            title={title}
            unit={unit}
        />
    );
};
