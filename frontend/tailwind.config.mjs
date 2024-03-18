import daisyui from 'daisyui';

/** @type {import('tailwindcss').Config} */
export default {
    content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
    theme: {
        extend: {},
    },
    daisyui: {
        themes: [
            {
                light: {
                    primary: '#004fff',
                    secondary: '#4ade80',
                    accent: '#6b21a8',
                    neutral: '#1e0402',
                    'base-100': '#f3f4f6',
                    info: '#7dd3fc',
                    success: '#a3e635',
                    warning: '#fbbf24',
                    error: '#f43f5e',
                },
                dark: {
                    primary: '#00b2ff',
                    secondary: '#0065bb',
                    accent: '#de9a00',
                    neutral: '#242a2d',
                    'base-100': '#292524',
                    info: '#00d0ff',
                    success: '#00f132',
                    warning: '#e9ab00',
                    error: '#ff8688',
                },
            },
        ],
    },
    plugins: [daisyui],
};
