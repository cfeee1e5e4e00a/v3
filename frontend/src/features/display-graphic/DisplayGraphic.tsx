import { FC } from 'react';
import { Line } from 'react-chartjs-2';

const data = [];

export const DisplayGraphic: FC = () => {
    return (
        <div className="flex items-center justify-center rounded-xl bg-white p-4">
            <Line
                data={{
                    datasets: [{ data, label: 'Температура в C' }],
                }}
                options={{
                    responsive: true,
                    plugins: {
                        legend: { position: 'bottom' },
                        title: {
                            display: true,
                            text: 'Температура в квартире',
                        },
                    },
                    parsing: {
                        xAxisKey: 'timestamp',
                        yAxisKey: 'value',
                    },
                    scales: {
                        x: {
                            type: 'linear',
                        },
                    },
                }}
            />
        </div>
    );
};
