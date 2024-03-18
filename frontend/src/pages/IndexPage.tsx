import { FC } from 'react';
import { useNavigate } from 'react-router-dom';

import { TeamName } from '@/shared/ui/TeamName';

export const IndexPage: FC = () => {
    const navigate = useNavigate();

    const goToSignInPage = () => navigate('/signin');

    return (
        <main className="flex h-full w-full flex-col items-center justify-center gap-12">
            <h1 className="text-4xl">
                <TeamName />
            </h1>
            <button
                onClick={goToSignInPage}
                className="btn btn-primary btn-large btn-wide"
            >
                <a className="text-xl">Войти</a>
            </button>
        </main>
    );
};
