
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import api from '../../../../src/lib/api';

export default function KitchenLoginPage() {
    const router = useRouter();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const res = await api.post('/auth/login', { username, password });

            // Verify role is kitchen or admin
            if (res.data.role !== 'kitchen' && res.data.role !== 'admin') {
                setError("Access denied. Kitchen staff only.");
                setLoading(false);
                return;
            }

            localStorage.setItem('token', res.data.access_token);
            localStorage.setItem('refreshToken', res.data.refresh_token);
            localStorage.setItem('role', res.data.role);

            // Dispatch event for Navbar update
            window.dispatchEvent(new Event('auth-change'));

            router.push('/kds');
        } catch (err: any) {
            setError(err.response?.data?.message || 'Login failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-900 px-4">
            <div className="max-w-md w-full glass-card p-8 rounded-2xl border border-gray-700">
                <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold text-white mb-2">Kitchen Display System</h1>
                    <p className="text-gray-400">Staff Access Terminal</p>
                </div>

                {error && (
                    <div className="bg-red-500/10 border border-red-500/50 text-red-500 p-3 rounded mb-4 text-center">
                        {error}
                    </div>
                )}

                <form onSubmit={handleLogin} className="space-y-6">
                    <div>
                        <label className="block text-gray-300 mb-2">Station ID / Username</label>
                        <input
                            type="text"
                            className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                            placeholder="e.g. kitchen01"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-gray-300 mb-2">Access Code / Password</label>
                        <input
                            type="password"
                            className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                            placeholder="••••••••"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>

                    <button
                        disabled={loading}
                        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition-transform active:scale-95 flex justify-center items-center"
                    >
                        {loading ? (
                            <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        ) : "Access KDS"}
                    </button>
                </form>

                <div className="mt-6 text-center">
                    <Link href="/" className="text-gray-500 hover:text-gray-300 text-sm">
                        ← Back to Main Menu
                    </Link>
                </div>
            </div>
        </div>
    );
}
