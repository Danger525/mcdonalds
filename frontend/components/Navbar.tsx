
'use client';

import { useEffect, useState } from 'react';

import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useCart } from '../src/context/CartContext';

export default function Navbar() {
    const { cart } = useCart();
    const router = useRouter();
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    const itemCount = cart.reduce((acc, item) => acc + item.quantity, 0);

    useEffect(() => {
        // Initial check
        const checkAuth = () => {
            const token = localStorage.getItem('token');
            setIsLoggedIn(!!token);
        };

        checkAuth();

        // Listen for storage events (login/logout in other tabs)
        window.addEventListener('storage', checkAuth);

        // Custom event for same-tab login updates
        window.addEventListener('auth-change', checkAuth);

        return () => {
            window.removeEventListener('storage', checkAuth);
            window.removeEventListener('auth-change', checkAuth);
        };
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        setIsLoggedIn(false);
        router.push('/');
        window.dispatchEvent(new Event('auth-change'));
    };


    return (
        <nav className="glass flex items-center justify-between p-4 sticky top-0 z-50">

            <Link href="/" className="text-xl font-bold text-gray-800 dark:text-white">
                SmartMenu
            </Link>
            <div className="flex gap-4 items-center">
                <Link href="/menu" className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
                    Menu
                </Link>

                {isLoggedIn ? (
                    <button
                        onClick={handleLogout}
                        className="text-red-500 hover:text-red-700 font-semibold"
                    >
                        Logout
                    </button>
                ) : (
                    <Link href="/auth/login" className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
                        Login
                    </Link>
                )}

                {isLoggedIn && (
                    <Link href="/admin" className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
                        Admin
                    </Link>
                )}

                <Link href="/cart" className="relative text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
                    </svg>
                    {itemCount > 0 && (
                        <span className="absolute -top-2 -right-2 bg-orange-600 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                            {itemCount}
                        </span>
                    )}
                </Link>
            </div>
        </nav>
    );
}

