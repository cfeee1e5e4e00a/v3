import { SignInForm } from '@/features/sign-in/SignInForm';

export const SignInPage = () => {
    return (
        <main className="flex h-full w-full flex-col items-center justify-center gap-12">
            <div className="flex flex-col items-center justify-center gap-12 rounded-xl bg-white p-8">
                <h1 className="text-3xl">С возвращением!</h1>
                <SignInForm />
            </div>
        </main>
    );
};
