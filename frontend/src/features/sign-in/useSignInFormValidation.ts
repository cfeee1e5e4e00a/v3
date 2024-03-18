import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';

const signInFormValidationSchema = z.object({
    username: z.string().min(1, { message: 'Обязательное поле' }),
    password: z.string().min(1, { message: 'Обязательное поле' }),
});

export type SignInFormValidationSchema = z.infer<
    typeof signInFormValidationSchema
>;

export function useSignInFormValidation() {
    return useForm<SignInFormValidationSchema>({
        resolver: zodResolver(signInFormValidationSchema),
    });
}
