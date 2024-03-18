import { computed, signal } from '@preact/signals-react';

import { LoginParams, login } from '@/entities/auth/api/login';

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

function readStateFromLocalStorage() {
    return window.localStorage.getItem('auth-token');
}

export const authToken = signal<string | null>(readStateFromLocalStorage());

export const isLoggedIn = computed(() => authToken.value !== null);

export async function signIn(params: LoginParams): Promise<void> {
    const token = await login(params);
    authToken.value = token;
    window.localStorage.setItem('auth-token', token);
}

export function logout(): void {
    authToken.value = null;
    window.localStorage.removeItem('auth-token');
}
