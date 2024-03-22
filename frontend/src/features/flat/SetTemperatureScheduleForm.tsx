import { ChangeEvent, FC, useState } from 'react';
import { Line } from 'react-chartjs-2';

import { useFlatMeasurement } from '@/features/flat/useFlatMeasurement';
import { MeasurementType } from '@/features/measurements/Measurement';
import { useSetTemperatureScheduleMutation } from '@/features/flat/useSetTemperatureScheduleMutation';
import { useHasTemperatureSchedule } from '@/features/flat/useHasTemperatureSchedule';

type Points = Array<Point>;
type Point = { time: number; temp: number };

type Props = {
    flat: number;
};

export const SetTemperatureScheduleForm: FC<Props> = ({ flat }) => {
    const setTemperatureScheduleMutation = useSetTemperatureScheduleMutation();
    const hasTemperatureSchedule = useHasTemperatureSchedule(() => ({ flat }));
    const temperatures = useFlatMeasurement<number>(() => ({
        flat,
        measurement: MeasurementType.TEMPERATURE,
        start: '-1m',
        stop: 'now()',
        window: '1m',
    }));

    const last = temperatures.data?.at(temperatures.data?.length - 1 ?? 0);

    const [points, setPoints] = useState<Points>([{ time: 10, temp: 25 }]);

    if (hasTemperatureSchedule.isLoading) {
        return null;
    }

    const addPoint = () => {
        setPoints((oldPoints) => {
            const { time, temp: value } = oldPoints[oldPoints.length - 1];
            return [...oldPoints, { time, temp: value }];
        });
    };

    const onInputChange =
        (field: keyof Point, idx: number) =>
        (event: ChangeEvent<HTMLInputElement>) => {
            const value = Number(event.currentTarget.value);

            if (Number.isNaN(value)) {
                return;
            }

            setPoints((oldPoints) => {
                const newPoints = [...oldPoints];
                newPoints[idx][field] = value;
                return newPoints;
            });
        };

    const submit = () => {
        setTemperatureScheduleMutation.trigger({ flat, points });
    };

    return (
        <div className="flex flex-col items-center justify-center gap-2 rounded-xl bg-white p-2">
            {hasTemperatureSchedule.data === true ? (
                <h1 className="text-2xl font-medium text-gray-500">
                    Профиль установлен
                </h1>
            ) : (
                <>
                    <h1 className="text-lg font-medium text-gray-500">
                        Установить профиль температуры
                    </h1>
                    <Line
                        data={{
                            datasets: [
                                {
                                    data: [
                                        { time: 0, temp: last?.value },
                                        ...points,
                                    ],
                                    label: 'Профиль температуры',
                                },
                            ],
                        }}
                        options={{
                            responsive: true,
                            plugins: {
                                legend: { position: 'bottom' },
                            },
                            parsing: {
                                xAxisKey: 'time',
                                yAxisKey: 'temp',
                            },
                            scales: {
                                x: {
                                    type: 'linear',
                                },
                            },
                        }}
                    />
                    <ul className="flex flex-col flex-wrap items-stretch gap-2">
                        {points.map((point, idx) => (
                            <li
                                className="flex flex-row items-center gap-2"
                                key={idx}
                            >
                                <span className="mr-2 w-8">{idx + 1}.</span>
                                <input
                                    type="number"
                                    placeholder="Время"
                                    onChange={onInputChange('time', idx)}
                                    value={point.time}
                                    className="input input-bordered input-sm w-24"
                                />
                                <input
                                    type="number"
                                    placeholder="Температура"
                                    onChange={onInputChange('temp', idx)}
                                    value={point.temp}
                                    className="input input-bordered input-sm w-36"
                                />
                            </li>
                        ))}
                        <button
                            onClick={addPoint}
                            className="btn btn-sm btn-primary self-end"
                        >
                            +
                        </button>
                    </ul>
                    <button
                        className="btn btn-primary btn-md text-lg"
                        onClick={submit}
                    >
                        Установить
                    </button>
                </>
            )}
        </div>
    );
};
