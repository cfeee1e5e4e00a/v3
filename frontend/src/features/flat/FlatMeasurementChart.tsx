import { FC } from 'react';

import { MeasurementsChart } from '@/features/measurements/MeasurementsChart';
import { useFlatMeasurement } from '@/features/flat/useFlatMeasurement';
import { MeasurementType } from '@/features/measurements/Measurement';
import { useUser } from '@/features/user/useUser';
import { useMeasurementChartOptions } from '@/features/measurements/useMeasurementChartOptions';

type Props = {
    measurement: MeasurementType;
    label: string;
    title: string;
};

export const FlatMeasurementChart: FC<Props> = ({
    measurement,
    title,
    label,
}) => {
    const chartOptions = useMeasurementChartOptions();
    const user = useUser();
    const data = useFlatMeasurement<number>(() =>
        user.data
            ? {
                  flat: 1,
                  measurement,
                  start: `-${chartOptions.options.period}`,
                  stop: 'now()',
                  window: chartOptions.options.window,
              }
            : null,
    );

    return (
        <MeasurementsChart<number>
            data={data.data}
            title={title}
            label={label}
            options={chartOptions}
        />
    );
};
