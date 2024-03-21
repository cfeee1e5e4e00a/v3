import { FC } from 'react';

import { MeasurementsChart } from '@/features/measurements/MeasurementsChart';
import { useFlatMeasurement } from '@/features/flat/useFlatMeasurement';
import { MeasurementType } from '@/features/measurements/Measurement';
import { useMeasurementChartOptions } from '@/features/measurements/useMeasurementChartOptions';

type Props = {
    measurement: MeasurementType;
    label: string;
    title: string;
    flat: number;
};

export const HouseMeasurementChart: FC<Props> = ({
    measurement,
    title,
    label,
    flat,
}) => {
    const chartOptions = useMeasurementChartOptions();
    const data = useFlatMeasurement<number>(() => ({
        flat,
        measurement,
        start: `-${chartOptions.options.period}`,
        stop: 'now()',
        window: chartOptions.options.window,
    }));

    return (
        <MeasurementsChart<number>
            data={data.data}
            title={title}
            label={label}
            options={chartOptions}
        />
    );
};
