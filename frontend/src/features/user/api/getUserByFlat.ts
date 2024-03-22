import {
    readAuthTokenFromLocalStorage,
    NotAuthenticatedError,
} from '@/features/auth';
import { User } from '@/features/user/User';
import ky from 'ky';

export type GetUserByFlatParams = {
    flat: number;
};

export async function getUserByFlat(
    params: GetUserByFlatParams,
): Promise<User> {
    const authToken = readAuthTokenFromLocalStorage();

    if (!authToken) {
        throw new NotAuthenticatedError();
    }

    const url = new URL(
        `http://diarrhea.cfeee1e5e4e00a.ru:8000/auth/by-flat/${params.flat}`,
    );

    const res = await ky(url, {
        headers: {
            Authorization: authToken,
        },
    });

    if (!res.ok) {
        throw new Error(res.statusText);
    }

    return await res.json();
}
