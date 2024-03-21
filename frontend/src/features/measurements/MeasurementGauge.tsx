import { Measurement } from '@/features/measurements/Measurement';

type Props<T> = {
    data?: Measurement<T>;
    title: string;
    unit: string;
};

export const MeasurementsGauge = <T,>({ data, title, unit }: Props<T>) => {
    return (
        <div className="flex items-center justify-center rounded-xl bg-white p-4">
            {!data && <p>loading</p>}
            {data && (
                <div className="flex flex-col items-center justify-center gap-2 text-gray-500">
                    <span className="text-6xl font-medium">
                        {String(data.value)} {unit}
                    </span>
                    <p className="text-lg font-medium">{title}</p>
                </div>
            )}
        </div>
    );
};
