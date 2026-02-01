
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '../../../src/lib/api';

export default function LoginPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const router = useRouter();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        try {
            const res = await api.post('/auth/login', { username, password });


            localStorage.setItem('token', res.data.access_token);
            localStorage.setItem('refreshToken', res.data.refresh_token);
            localStorage.setItem('role', res.data.role);

            // Notify Navbar to update
            window.dispatchEvent(new Event('auth-change'));



            if (res.data.role === 'admin' || res.data.role === 'manager') {
                router.push('/admin');
            } else if (res.data.role === 'kitchen') {
                router.push('/kds');
            } else {
                router.push('/menu');
            }

        } catch (err: any) {
            console.error(err);
            setError('Invalid credentials');
        }
    };

    return (
        <div className="flex justify-center items-center min-h-[60vh]">
            <div className="w-full max-w-md p-8 bg-white rounded-lg shadow-md dark:bg-gray-800">
                <h2 className="text-2xl font-bold mb-6 text-center text-gray-800 dark:text-white">Login</h2>

                {error && <p className="text-red-500 mb-4 text-center">{error}</p>}

                <form onSubmit={handleLogin} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Username</label>
                        <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="mt-1 block w-full px-3 py-2 border rounded-md shadow-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="mt-1 block w-full px-3 py-2 border rounded-md shadow-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-md transition-colors"
                    >
                        Sign In
                    </button>
                </form>
            </div>
        </div>
    );
}
