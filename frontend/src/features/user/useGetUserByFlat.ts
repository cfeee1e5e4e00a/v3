import {
    GetUserByFlatParams,
    getUserByFlat,
} from '@/features/user/api/getUserByFlat';
import useSWR from 'swr';

export function useGetUserByFlat(
    shouldFetch: () => GetUserByFlatParams | null,
) {
    return useSWR(
        () => {
            const params = shouldFetch();
            if (!params) {
                return null;
            }
            return [`/auth/by-flat/${params.flat}`, params];
        },
        ([, params]) => getUserByFlat(params),
    );
}
