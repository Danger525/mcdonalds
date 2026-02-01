
'use client';

import { useEffect, useState } from 'react';
import api from '../../../src/lib/api';
import { useParams } from 'next/navigation';

export default function OrderStatusPage() {
    const { id } = useParams();
    const [order, setOrder] = useState<any>(null);

    useEffect(() => {
        if (id) {
            fetchOrder();
            const interval = setInterval(fetchOrder, 5000); // Poll every 5s
            return () => clearInterval(interval);
        }
    }, [id]);

    const fetchOrder = async () => {
        try {
            const res = await api.get(`/orders/${id}`);
            setOrder(res.data);
        } catch (err) {
            console.error("Failed to fetch order");
        }
    };

    if (!order) return <div className="p-10 text-center">Loading Order...</div>;

    const statusColors: Record<string, string> = {
        pending: 'bg-yellow-100 text-yellow-800',
        confirmed: 'bg-blue-100 text-blue-800',
        preparing: 'bg-purple-100 text-purple-800',
        ready: 'bg-green-100 text-green-800',
        completed: 'bg-gray-100 text-gray-800',
        cancelled: 'bg-red-100 text-red-800'
    };

    return (
        <div className="max-w-2xl mx-auto p-8 text-center">
            <h1 className="text-3xl font-bold mb-4">Order #{id}</h1>

            <div className={`inline-block px-6 py-2 rounded-full text-xl font-bold mb-8 uppercase tracking-wide ${statusColors[order.status] || 'bg-gray-100'}`}>
                {order.status}
            </div>


            <div className="bg-white p-6 rounded-lg shadow-lg dark:bg-gray-800 text-left">
                <h2 className="text-xl font-semibold mb-4 border-b pb-2">Order Details</h2>
                <div className="space-y-3 mb-6">
                    {order.items.map((item: any, idx: number) => (
                        <div key={idx} className="flex justify-between">
                            <span>{item.quantity}x {item.name}</span>
                            <span>₹{item.total.toFixed(2)}</span>
                        </div>
                    ))}
                </div>
                <div className="flex justify-between text-xl font-bold border-t pt-4">
                    <span>Total</span>
                    <span>₹{order.total.toFixed(2)}</span>
                </div>
            </div>


            <p className="mt-8 text-gray-500">
                This page will automatically update when your order status changes.
            </p>
        </div>
    );
}
