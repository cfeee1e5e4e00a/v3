import {
    NotAuthenticatedError,
    readAuthTokenFromLocalStorage,
} from '@/features/auth';
import { Flat } from '@/features/flat/Flat';
import {
    MeasurementType,
    MeasurementsData,
} from '@/features/measurements/Measurement';

export type GetFlatMeasurementParams = {
    flat: Flat['id'];
    measurement: MeasurementType;
    start: string;
    stop: string;
    window: string;
};

export async function getFlatMeasurement<T>(
    params: GetFlatMeasurementParams,
): Promise<MeasurementsData<T>> {
    const authToken = readAuthTokenFromLocalStorage();

    if (!authToken) {
        throw new NotAuthenticatedError();
    }

    const url = new URL(
        `http://diarrhea.cfeee1e5e4e00a.ru:8000/flats/${params.flat}/${params.measurement}`,
    );

    url.searchParams.set('start', params.start);
    url.searchParams.set('stop', params.stop);
    url.searchParams.set('window', params.window);
    url.searchParams.set(
        'tz',
        Intl.DateTimeFormat().resolvedOptions().timeZone,
    );

    const res = await fetch(url, {
        headers: {
            Authorization: authToken,
        },
    });

    if (!res.ok) {
        throw new Error(res.statusText);
    }

    return await res.json();
}
