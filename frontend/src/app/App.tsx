import { FC, StrictMode } from 'react';

import { RouterEntry } from '@/app/RouterEntry';

export const App: FC = () => {
    return (
        <StrictMode>
            <RouterEntry />
        </StrictMode>
    );
};
