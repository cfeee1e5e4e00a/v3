import {
    NotAuthenticatedError,
    readAuthTokenFromLocalStorage,
} from '@/features/auth';
import ky from 'ky';

export type SetTermperatureScheduleParams = {
    flat: number;
    points: Array<{
        time: number;
        temp: number;
    }>;
};

export async function setTemperatureSchedule({
    flat,
    points,
}: SetTermperatureScheduleParams): Promise<void> {
    const authToken = readAuthTokenFromLocalStorage();

    if (!authToken) {
        throw new NotAuthenticatedError();
    }

    const url = new URL(
        `http://diarrhea.cfeee1e5e4e00a.ru:8000/flats/${flat}/schedule`,
    );

    const body = { entries: points };

    const res = await ky.post(url, {
        headers: {
            Authorization: authToken,
        },
        json: body,
    });

    if (!res.ok) {
        throw new Error(res.statusText);
    }
}
