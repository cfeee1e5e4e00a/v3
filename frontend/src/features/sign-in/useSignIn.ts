import useSWRMutation from 'swr/mutation';

import { signIn } from '@/entities/auth';
import { LoginParams } from '@/entities/auth/api/login';

export function useSignInMutation() {
    return useSWRMutation('/auth/me', (_, { arg }: { arg: LoginParams }) =>
        signIn(arg),
    );
}
