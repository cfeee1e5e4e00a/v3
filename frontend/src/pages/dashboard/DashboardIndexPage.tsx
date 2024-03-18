import { FC } from 'react';
import useSWR from 'swr';

import { getMe } from '@/entities/user/api/getMe';

export const DashboardIndexPage: FC = () => {
    const me = useSWR('/api/me', () => getMe());

    return <main>{me.data && JSON.stringify(me.data)}</main>;
};
