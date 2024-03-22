import useSWR from 'swr';

import {
    HasTemperatureScheduleParams,
    hasTemperatureSchedule,
} from '@/features/flat/api/hasTemperatureSchedule';

export function useHasTemperatureSchedule(
    shouldFetch: () => HasTemperatureScheduleParams | null,
) {
    return useSWR(
        () => {
            const params = shouldFetch();
            if (!params) {
                return null;
            }
            return [`/flats/${params.flat}/has_schedule`, params];
        },
        ([, params]) => hasTemperatureSchedule(params),
    );
}
