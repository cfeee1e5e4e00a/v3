import ky from 'ky';

import { User } from '@/features/user/User';
import {
    readAuthTokenFromLocalStorage,
    NotAuthenticatedError,
} from '@/features/auth';

export async function getMe(): Promise<User> {
    const authToken = readAuthTokenFromLocalStorage();

    if (!authToken) {
        throw new NotAuthenticatedError();
    }

    const res = await ky.get('http://diarrhea.cfeee1e5e4e00a.ru:8000/auth/me', {
        headers: {
            Authorization: authToken,
        },
    });

    if (!res.ok) {
        throw new Error(res.statusText);
    }

    return res.json();
}
