import { MeasurementsData } from '@/features/measurements/Measurement';
import { Line } from 'react-chartjs-2';

type Props<T> = {
    data?: MeasurementsData<T>;
    label?: string;
    title?: string;
};

export const MeasurementDisplay = <T,>({ data, label, title }: Props<T>) => {
    return (
        <div className="flex items-center justify-center rounded-xl bg-white p-4">
            {!data && <p>loading</p>}
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
    );
};
