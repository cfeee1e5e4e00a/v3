import { mutate } from 'swr';
import useSWRMutation from 'swr/mutation';

import { LoginParams } from '@/entities/auth/api/login';
import { signIn } from '@/entities/auth';

export function useSignInMutation() {
    return useSWRMutation(
        '/auth/me',
        async (_, { arg }: { arg: LoginParams }) => {
            await signIn(arg);
            mutate('localStorage://auth-token');
        },
    );
}
