import ky from 'ky';

import {
    readAuthTokenFromLocalStorage,
    NotAuthenticatedError,
} from '@/features/auth';

export type SetTargetTemperatureParams = {
    flat: number;
    temperature: number;
};

export async function setTargetTemperature(
    params: SetTargetTemperatureParams,
): Promise<void> {
    const authToken = readAuthTokenFromLocalStorage();

    if (!authToken) {
        throw new NotAuthenticatedError();
    }

    const url = new URL(
        `http://diarrhea.cfeee1e5e4e00a.ru:8000/flats/${params.flat}/target`,
    );
    url.searchParams.set('temp', String(params.temperature));

    const res = await ky(url, {
        headers: {
            Authorization: authToken,
        },
    });

    if (!res.ok) {
        throw new Error(res.statusText);
    }
}
