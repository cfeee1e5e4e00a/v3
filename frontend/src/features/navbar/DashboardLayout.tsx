import { Navbar } from '@/features/navbar/Navbar';
import { Outlet } from 'react-router-dom';

export const DashboardLayout = () => {
    return (
        <div className="flex h-full w-full flex-row">
            <Navbar />
            <div className="h-full w-full p-4">
                <Outlet />
            </div>
        </div>
    );
};
