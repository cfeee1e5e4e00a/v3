import { Dispatch, SetStateAction, useState } from 'react';

export const measurementChartOptions = [
    {
        period: '1m',
        window: '10s',
    },
    {
        period: '5m',
        window: '10s',
    },
    {
        period: '15m',
        window: '1m',
    },
    {
        period: '30m',
        window: '1m',
    },
    {
        period: '1h',
        window: '1m',
    },
    {
        period: '3h',
        window: '1m',
    },
    {
        period: '6h',
        window: '1m',
    },
    {
        period: '12h',
        window: '2m',
    },
    {
        period: '24h',
        window: '10m',
    },
] as const;

type MeasurementChartOptions = (typeof measurementChartOptions)[number];

export type MeasurementChartOptionsProps = {
    options: MeasurementChartOptions;
    setOptions: Dispatch<SetStateAction<MeasurementChartOptions>>;
};

export function useMeasurementChartOptions(): MeasurementChartOptionsProps {
    const [options, setOptions] = useState<MeasurementChartOptions>({
        period: '15m',
        window: '1m',
    });

    return {
        options,
        setOptions,
    };
}
