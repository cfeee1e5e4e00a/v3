import useSWRMutation from 'swr/mutation';

import {
    SetTermperatureScheduleParams,
    setTemperatureSchedule,
} from '@/features/flat/api/setTemperatureSchedule';

export function useSetTemperatureScheduleMutation() {
    return useSWRMutation(
        '/flats/schedule',
        (_, { arg }: { arg: SetTermperatureScheduleParams }) => {
            setTemperatureSchedule(arg);
        },
    );
}
