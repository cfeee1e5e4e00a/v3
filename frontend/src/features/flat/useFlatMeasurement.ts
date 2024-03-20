import {
    GetFlatMeasurementParams,
    getFlatMeasurement,
} from '@/features/flat/api/getFlatMeasurement';
import useSWR from 'swr';

export function useFlatMeasurement<T>(
    shouldFetch: () => GetFlatMeasurementParams | null,
) {
    return useSWR(
        () => {
            const params = shouldFetch();
            if (!params) {
                return null;
            }
            const { flat, measurement, start, stop, window } = params;
            return ['/flats/', flat, measurement, start, stop, window];
        },
        ([, flat, measurement, start, stop, window]) =>
            getFlatMeasurement<T>({ flat, measurement, start, stop, window }),
    );
}
