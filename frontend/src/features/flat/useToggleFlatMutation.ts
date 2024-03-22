import { toggleFlat, ToggleFlatParams } from '@/features/flat/api/toggleFlat';
import { mutate } from 'swr';
import useSWRMutation from 'swr/mutation';

export function useToggleFlatMutation() {
    return useSWRMutation(
        '/flat/toggle',
        async (_, { arg }: { arg: ToggleFlatParams }) => {
            await toggleFlat(arg);
            await mutate([`/auth/by-flat/${arg.flat}`, { flat: arg.flat }]);
        },
    );
}
