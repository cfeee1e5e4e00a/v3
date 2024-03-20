import { mutate } from 'swr';
import useSWRMutation from 'swr/mutation';

import { logout } from '@/features/auth';

export function useLogoutMutation() {
    return useSWRMutation('/auth/me', async () => {
        logout();
        mutate('localStorage://auth-token');
    });
}