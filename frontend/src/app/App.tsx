import { FC, StrictMode } from 'react';
import 'chart.js/auto';

import { RouterEntry } from '@/app/RouterEntry';
import '@/app/index.css';

export const App: FC = () => {
    return (
        <StrictMode>
            <RouterEntry />
        </StrictMode>
    );
};
