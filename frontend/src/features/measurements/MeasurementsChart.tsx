import { Line } from 'react-chartjs-2';

import { MeasurementsData } from '@/features/measurements/Measurement';
import {
    MeasurementChartOptionsProps,
    measurementChartOptions,
} from '@/features/measurements/useMeasurementChartOptions';

type Props<T> = {
    data?: MeasurementsData<T>;
    label?: string;
    title?: string;
    options: MeasurementChartOptionsProps;
};

export const MeasurementsChart = <T,>({
    data,
    label,
    title,
    options: { options, setOptions },
}: Props<T>) => {
    return (
        <div className="flex flex-col items-end justify-between rounded-xl bg-white p-1">
            {!data && <p>loading</p>}
            {data && (
                <>
                    <div className="flex h-full w-full justify-center">
                        <Line
                            data={{
                                datasets: [{ data, label }],
                            }}
                            options={{
                                responsive: true,
                                plugins: {
                                    legend: { position: 'bottom' },
                                    title: {
                                        display: true,
                                        text: title,
                                    },
                                },
                                parsing: {
                                    xAxisKey: 'timestamp',
                                    yAxisKey: 'value',
                                },
                            }}
                        />
                    </div>
                    <label className="form-control w-24 max-w-xs">
                        <select
                            className="select select-bordered select-sm"
                            value={options.period}
                            onChange={(event) => {
                                const option = measurementChartOptions.at(
                                    event.currentTarget.selectedIndex,
                                );

                                if (option) {
                                    setOptions(option);
                                }
                            }}
                        >
                            {measurementChartOptions.map(({ period }) => (
                                <option value={period} key={period}>
                                    {period}
                                </option>
                            ))}
                        </select>
                    </label>
                </>
            )}
        </div>
    );
};
