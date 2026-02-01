
'use client';


import { useEffect, useState } from 'react';
import api from '../../src/lib/api';
import { socket } from '../../src/lib/socket';
import { useRouter } from 'next/navigation';
import Toast from '../../components/Toast';

export default function KDSPage() {
    const [orders, setOrders] = useState<any[]>([]);
    const router = useRouter();

    // Toast State
    const [toastMsg, setToastMsg] = useState('');
    const [showToast, setShowToast] = useState(false);

    const showNotification = (msg: string) => {
        setToastMsg(msg);
        setShowToast(true);
    };



    useEffect(() => {
        // Check auth
        if (!localStorage.getItem('token')) {
            router.push('/auth/login');
            return;
        }

        fetchOrders();

        // POLL every 5 seconds (since Socket.IO is disabled)
        const interval = setInterval(() => {
            fetchOrders();
        }, 5000);

        return () => clearInterval(interval);
    }, []);

    const fetchOrders = async () => {
        try {
            const res = await api.get('/orders/');
            setOrders(res.data);
        } catch (err) {
            console.error("Failed to load orders");
        }
    };

    const updateStatus = async (id: number, status: string) => {
        try {
            await api.put(`/orders/${id}/status`, { status });
            fetchOrders(); // Immediate reload

        } catch (err) {
            console.error("Update failed", err);
            showNotification("Failed to update status");
        }
    };


    // Group orders
    // Include 'confirmed' in pending list so they don't disappear
    const pending = orders.filter(o => o.status === 'pending' || o.status === 'confirmed');

    const preparing = orders.filter(o => o.status === 'preparing');
    const ready = orders.filter(o => o.status === 'ready');

    return (
        <div className="min-h-screen bg-gray-900 text-white p-4">

            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold">Kitchen Display System</h1>
                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2 text-sm text-green-400">
                        <span className="relative flex h-3 w-3">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
                        </span>
                        Live (Polling)
                    </div>
                    <button
                        onClick={() => fetchOrders()}
                        className="bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded text-sm font-semibold"
                    >
                        Refresh
                    </button>
                </div>
            </div>


            <div className="grid grid-cols-3 gap-6 h-[85vh]">
                {/* NEW ORDERS */}
                <div className="bg-gray-800 rounded-lg p-4 overflow-y-auto">
                    <h2 className="text-xl font-bold text-yellow-400 mb-4 sticky top-0 bg-gray-800 py-2 border-b border-gray-700">New Orders ({pending.length})</h2>
                    <div className="space-y-4">
                        {pending.map(order => (
                            <div key={order.id} className="bg-gray-700 p-4 rounded border-l-4 border-yellow-500">
                                <div className="flex justify-between font-bold text-lg mb-2">
                                    <span>#{order.order_number || order.id}</span>
                                    <span>Table {order.table_number}</span>
                                </div>
                                <div className="text-sm text-gray-300 mb-4 space-y-1">
                                    {order.items.map((item: any, i: number) => (
                                        <div key={i}>{item.quantity}x {item.menu_item_name}</div>
                                    ))}
                                </div>
                                <button
                                    onClick={() => updateStatus(order.id, 'preparing')}
                                    className="w-full bg-blue-600 hover:bg-blue-700 py-2 rounded font-semibold"
                                >
                                    Start Preparing
                                </button>
                            </div>
                        ))}
                    </div>
                </div>

                {/* PREPARING */}
                <div className="bg-gray-800 rounded-lg p-4 overflow-y-auto">
                    <h2 className="text-xl font-bold text-blue-400 mb-4 sticky top-0 bg-gray-800 py-2 border-b border-gray-700">Cooking ({preparing.length})</h2>
                    <div className="space-y-4">
                        {preparing.map(order => (
                            <div key={order.id} className="bg-gray-700 p-4 rounded border-l-4 border-blue-500">
                                <div className="flex justify-between font-bold text-lg mb-2">
                                    <span>#{order.order_number || order.id}</span>
                                    <span>Table {order.table_number}</span>
                                </div>
                                <div className="text-sm text-gray-300 mb-4 space-y-1">
                                    {order.items.map((item: any, i: number) => (
                                        <div key={i}>{item.quantity}x {item.menu_item_name}</div>
                                    ))}
                                </div>
                                <button
                                    onClick={() => updateStatus(order.id, 'ready')}
                                    className="w-full bg-green-600 hover:bg-green-700 py-2 rounded font-semibold"
                                >
                                    Mark Ready
                                </button>
                            </div>
                        ))}
                    </div>
                </div>

                {/* READY */}
                <div className="bg-gray-800 rounded-lg p-4 overflow-y-auto">
                    <h2 className="text-xl font-bold text-green-400 mb-4 sticky top-0 bg-gray-800 py-2 border-b border-gray-700">Ready to Serve ({ready.length})</h2>
                    <div className="space-y-4">
                        {ready.map(order => (
                            <div key={order.id} className="bg-gray-700 p-4 rounded border-l-4 border-green-500 opacity-80">
                                <div className="flex justify-between font-bold text-lg mb-2">
                                    <span>#{order.order_number || order.id}</span>
                                    <span>Table {order.table_number}</span>
                                </div>
                                <div className="text-sm text-gray-300 mb-4 space-y-1">
                                    {order.items.map((item: any, i: number) => (
                                        <div key={i}>{item.quantity}x {item.menu_item_name}</div>
                                    ))}
                                </div>
                                <button
                                    onClick={() => updateStatus(order.id, 'completed')}
                                    className="w-full bg-gray-600 hover:bg-gray-500 py-2 rounded font-semibold"
                                >
                                    Complete
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            </div>


            <Toast
                message={toastMsg}
                isVisible={showToast}
                onClose={() => setShowToast(false)}
            />
        </div>
    );


}
