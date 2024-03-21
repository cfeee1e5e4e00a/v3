import { FC, FormEvent, useState } from 'react';

import { useSetTargetTemperatureMutation } from '@/features/flat/useSetTargetTemperatureMutation';
import { useUser } from '@/features/user/useUser';

const DEFAULT_TEMPERATURE = 22.0;

export const FlatTargetTemperatureControl: FC = () => {
    const user = useUser();
    const setTargetTemperatureMutation = useSetTargetTemperatureMutation();

    const [temperature, setTemperature] = useState(DEFAULT_TEMPERATURE);

    const onInputTemperature = (event: FormEvent<HTMLInputElement>) => {
        const value = Number(event.currentTarget.value);

        if (Number.isNaN(value)) {
            return;
        }

        setTemperature(value);
    };

    const onSetClick = () => {
        if (!user.data) {
            return;
        }

        setTargetTemperatureMutation.trigger({
            flat: user.data.flat,
            temperature,
        });
    };

    return (
        <div className="flex w-full flex-row items-center justify-center gap-4 rounded-xl bg-white p-4">
            {user.data && (
                <label className="form-control w-full max-w-xs">
                    <div className="label w-full pt-0">
                        <span className="label-text text-lg font-medium text-gray-500">
                            Установить температуру
                        </span>
                    </div>
                    <div className="flex w-full flex-row gap-4">
                        <input
                            type="text"
                            placeholder="Температура"
                            className="input input-bordered w-full"
                            onInput={onInputTemperature}
                        />
                        <button
                            onClick={onSetClick}
                            className="btn btn-primary"
                        >
                            Установить
                        </button>
                    </div>
                </label>
            )}
        </div>
    );
};
