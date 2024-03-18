import ky from 'ky';

import { User } from '@/entities/user/User';
import { NotAuthenticatedError, authToken } from '@/entities/auth';

export async function getMe(): Promise<User> {
    if (!authToken.value) {
        throw new NotAuthenticatedError();
    }

    const res = await ky.get('http://diarrhea.cfeee1e5e4e00a.ru:8000/auth/me', {
        headers: {
            Authorization: authToken.value,
        },
    });

    if (!res.ok) {
        throw new Error(res.statusText);
    }

    return res.json();
}
