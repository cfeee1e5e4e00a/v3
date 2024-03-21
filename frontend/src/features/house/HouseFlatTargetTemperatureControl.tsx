import { FC, FormEvent, useState } from 'react';

import { useSetTargetTemperatureMutation } from '@/features/flat/useSetTargetTemperatureMutation';

type Props = {
    flat: number;
};

const DEFAULT_TEMPERATURE = 22.0;

export const HouseFlatTargetTemperatureControl: FC<Props> = ({ flat }) => {
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
        setTargetTemperatureMutation.trigger({
            flat,
            temperature,
        });
    };

    return (
        <div className="flex w-full flex-row items-center justify-center rounded-xl bg-white p-1">
            <label className="form-control w-full max-w-xs">
                <div className="label w-full pb-1 pt-0">
                    <span className="label-text text-md font-medium text-gray-500">
                        {`Установить температуру в квартире ${flat}`}
                    </span>
                </div>
                <div className="flex w-full flex-row gap-1">
                    <input
                        type="text"
                        placeholder="Температура"
                        className="input input-bordered input-sm w-full"
                        onInput={onInputTemperature}
                    />
                    <button
                        onClick={onSetClick}
                        className="btn btn-primary btn-sm"
                    >
                        Установить
                    </button>
                </div>
            </label>
        </div>
    );
};
