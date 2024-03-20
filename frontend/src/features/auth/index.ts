import useSWR from 'swr';

import { LoginParams, login } from '@/features/auth/api/login';

export class NotAuthenticatedError extends Error {
    constructor() {
        super('Вы неаутефицированы');
        Object.setPrototypeOf(this, NotAuthenticatedError.prototype);
    }
}

export class NotAuthorizedError extends Error {
    constructor() {
        super('Вы неавторизованы для этого!');
        Object.setPrototypeOf(this, NotAuthorizedError.prototype);
    }
}

export type AuthToken = string;

export function readAuthTokenFromLocalStorage(): AuthToken | null {
    return window.localStorage.getItem('auth-token');
}

export function useAuthToken() {
    return useSWR('localStorage://auth-token', () =>
        readAuthTokenFromLocalStorage(),
    );
}

export async function signIn(params: LoginParams): Promise<void> {
    const token = await login(params);
    window.localStorage.setItem('auth-token', token);
}

export function logout(): void {
    window.localStorage.removeItem('auth-token');
}
