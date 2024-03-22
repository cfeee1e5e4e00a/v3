import {
    NotAuthenticatedError,
    readAuthTokenFromLocalStorage,
} from '@/features/auth';
import ky from 'ky';

export type ToggleFlatParams = {
    flat: number;
    state: boolean;
};

export async function toggleFlat(params: ToggleFlatParams): Promise<void> {
    const authToken = readAuthTokenFromLocalStorage();

    if (!authToken) {
        throw new NotAuthenticatedError();
    }

    const url = new URL(
        `http://diarrhea.cfeee1e5e4e00a.ru:8000/flats/${params.flat}/toggle`,
    );

    url.searchParams.set('state', params.state);

    const res = await ky.post(url, {
        headers: {
            Authorization: authToken,
        },
    });

    if (!res.ok) {
        throw new Error(res.statusText);
    }
}
