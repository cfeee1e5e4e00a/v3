import ky from 'ky';

export type LoginParams = {
    username: string;
    password: string;
};

export async function login(params: LoginParams): Promise<string> {
    const res = await ky.post(
        'http://diarrhea.cfeee1e5e4e00a.ru:8000/auth/login',
        {
            json: {
                name: params.username,
                password: params.password,
            },
        },
    );

    if (!res.ok) {
        throw new Error(res.statusText);
    }

    return await res.json();
}
