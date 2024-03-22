import useSWRMutation from 'swr/mutation';

import {
    SetTargetTemperatureParams,
    setTargetTemperature,
} from '@/features/flat/api/setTargetTemperature';

export function useSetTargetTemperatureMutation() {
    return useSWRMutation(
        `/flats/target`,
        (_, { arg }: { arg: SetTargetTemperatureParams }) => {
            setTargetTemperature(arg);
        },
    );
}
