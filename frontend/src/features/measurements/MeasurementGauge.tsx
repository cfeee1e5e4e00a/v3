import { Measurement } from '@/features/measurements/Measurement';
import clsx from 'clsx';

type Props<T> = {
    data?: Measurement<T>;
    title: string;
    unit: string;
    size?: 'm' | 's';
};

export const MeasurementsGauge = <T,>({
    data,
    title,
    unit,
    size = 'm',
}: Props<T>) => {
    return (
        <div className="flex items-center justify-center rounded-xl bg-white">
            {!data && <p>loading</p>}
            {data && (
                <div className="flex flex-col items-center justify-center  text-gray-500">
                    <span
                        className={clsx({
                            ['text-3xl font-medium']: size == 'm',
                            ['text-2xl']: size == 's',
                        })}
                    >
                        {String(data.value)} {unit}
                    </span>
                    <p
                        className={clsx('text-center', {
                            ['text-lg font-medium']: size == 'm',
                            ['text-md']: size == 's',
                        })}
                    >
                        {title}
                    </p>
                </div>
            )}
        </div>
    );
};
