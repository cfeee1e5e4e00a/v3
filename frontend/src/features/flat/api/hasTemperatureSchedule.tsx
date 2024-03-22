import {
    NotAuthenticatedError,
    readAuthTokenFromLocalStorage,
} from '@/features/auth';
import ky from 'ky';

export type HasTemperatureScheduleParams = {
    flat: number;
};

export async function hasTemperatureSchedule(
    params: HasTemperatureScheduleParams,
): Promise<boolean> {
    const authToken = readAuthTokenFromLocalStorage();

    if (!authToken) {
        throw new NotAuthenticatedError();
    }

    const url = new URL(
        `http://diarrhea.cfeee1e5e4e00a.ru:8000/flats/${params.flat}/has_schedule`,
    );

    const res = await ky(url, {
        headers: {
            Authorization: authToken,
        },
    });

    if (!res.ok) {
        throw new Error(res.statusText);
    }

    return res.json();
}
