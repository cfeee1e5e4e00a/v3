import { FC } from 'react';
import clsx from 'clsx';

import { useGetUserByFlat } from '@/features/user/useGetUserByFlat';
import { useToggleFlatMutation } from '@/features/flat/useToggleFlatMutation';

type Props = {
    flat: number;
};

export const FlatToggleStatus: FC<Props> = ({ flat }) => {
    const user = useGetUserByFlat(() => ({ flat }));
    const toggleFlatMutation = useToggleFlatMutation();

    const toggle = () => {
        if (!user.data) {
            return;
        }
        const state = user.data.disabled ? true : false;
        toggleFlatMutation.trigger({ flat, state });
    };

    if (!user.data) {
        return null;
    }

    return (
        <div className="flex flex-col items-center justify-center rounded-xl bg-white p-2">
            <span className="text-lg">Статус</span>
            <span
                className={clsx('mb-2 text-2xl font-bold', {
                    ['text-success']: !user.data.disabled,
                    ['text-error']: user.data.disabled,
                })}
            >
                {user.data.disabled ? 'Отключена' : 'Включена'}
            </span>
            <button
                onClick={toggle}
                className={clsx('btn btn-sm', {
                    ['btn-success text-success-content']: user.data.disabled,
                    ['btn-error text-error-content']: !user.data.disabled,
                })}
            >
                {user.data.disabled ? 'Включить' : 'Отключить'}
            </button>
        </div>
    );
};
