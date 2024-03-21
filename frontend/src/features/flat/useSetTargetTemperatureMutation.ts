import useSWRMutation from 'swr/mutation';

import {
    SetTargetTemperatureParams,
    setTargetTemperature,
} from '@/features/flat/api/setTargetTemperature';

export function useSetTargetTemperatureMutation() {
    return useSWRMutation(
        `/flats/target`,
        async (_, { arg }: { arg: SetTargetTemperatureParams }) => {
            setTargetTemperature(arg);
        },
    );
}
