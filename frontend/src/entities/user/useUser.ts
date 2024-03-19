import { getMe } from '@/entities/user/api/getMe';
import useSWR from 'swr';

export function useUser() {
    return useSWR('/auth/me', () => getMe());
}
