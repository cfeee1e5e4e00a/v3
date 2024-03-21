import { FC } from 'react';

import { MeasurementsGauge } from '@/features/measurements/MeasurementGauge';
import { useFlatMeasurement } from '@/features/flat/useFlatMeasurement';
import { MeasurementType } from '@/features/measurements/Measurement';

type Props = {
    measurement: MeasurementType;
    title: string;
    unit: string;
    flat: number;
};

export const HouseMeasurementGauge: FC<Props> = ({
    measurement,
    title,
    unit,
    flat,
}) => {
    const data = useFlatMeasurement<number>(() => ({
        flat,
        measurement,
        start: '-1m',
        stop: 'now()',
        window: '1m',
    }));

    return (
        <MeasurementsGauge<number>
            size="s"
            data={data.data?.at(data.data?.length - 1 ?? 0)}
            title={title}
            unit={unit}
        />
    );
};
