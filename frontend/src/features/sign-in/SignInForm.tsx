import { FC } from 'react';
import { useNavigate } from 'react-router-dom';
import clsx from 'clsx';

import { useSignInMutation } from '@/features/sign-in/useSignIn';
import {
    SignInFormValidationSchema,
    useSignInFormValidation,
} from '@/features/sign-in/useSignInFormValidation';

export const SignInForm: FC = () => {
    const formValidation = useSignInFormValidation();
    const signInMutation = useSignInMutation();
    const navigate = useNavigate();

    const {
        formState: { errors },
    } = formValidation;

    const onValidSubmit = async (data: SignInFormValidationSchema) => {
        await signInMutation.trigger(data);
        navigate('/dashboard');
    };

    const disableSubmit = Boolean(errors.password || errors.username);

    return (
        <form
            onSubmit={formValidation.handleSubmit(onValidSubmit)}
            className="flex w-72 flex-col items-center gap-6"
        >
            <label className="form-control w-full max-w-xs">
                <input
                    type="text"
                    className="input input-bordered w-full max-w-xs"
                    placeholder="Логин"
                    {...formValidation.register('username')}
                />
                <div className="label">
                    <span
                        className={clsx('label-text-alt', {
                            ['invisible']: !errors.username?.message,
                        })}
                    >
                        {String(errors.username?.message)}
                    </span>
                </div>
            </label>
            <label className="form-control w-full max-w-xs">
                <input
                    type="password"
                    className="input input-bordered w-full max-w-xs"
                    placeholder="Пароль"
                    {...formValidation.register('password')}
                />
                <div className="label">
                    <span
                        className={clsx('label-text-alt', {
                            ['invisible']: !errors.password?.message,
                        })}
                    >
                        {String(errors.password?.message)}
                    </span>
                </div>
            </label>
            <button
                disabled={disableSubmit}
                type="submit"
                className="btn btn-primary w-full text-lg"
            >
                Войти
            </button>
        </form>
    );
};
