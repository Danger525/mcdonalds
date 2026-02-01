
'use client';

import { useCart } from '../../src/context/CartContext';
import api from '../../src/lib/api';
import { useRouter } from 'next/navigation';
import { useState } from 'react';


import Toast from '../../components/Toast';

export default function CartPage() {
    const { cart, removeFromCart, clearCart, total } = useCart();
    const router = useRouter();
    const [tableNumber, setTableNumber] = useState('');
    const [loading, setLoading] = useState(false);

    const [toastMsg, setToastMsg] = useState('');
    const [showToast, setShowToast] = useState(false);

    const showNotification = (msg: string) => {
        setToastMsg(msg);
        setShowToast(true);
    };



    const handleCheckout = async () => {
        if (!tableNumber) return showNotification("Please enter a table number");
        setLoading(true);

        try {
            const orderData = {
                table_number: parseInt(tableNumber),
                items: cart.map(item => ({
                    menu_item_id: item.id,
                    quantity: item.quantity
                }))
            };


            const res = await api.post('/orders/', orderData);
            console.log("Order Response:", res.data); // DEBUG
            showNotification(`Order placed! Order Number: ${res.data.order_number}`);
            clearCart();

            const redirectUrl = `/orders/${res.data.order_id}`;
            console.log("Redirecting to:", redirectUrl); // DEBUG

            // Delay redirect slightly to show toast
            setTimeout(() => {
                router.push(redirectUrl);
            }, 1000);

        } catch (err) {
            console.error(err);
            showNotification("Failed to place order. Ensure you are logged in if required.");
        } finally {
            setLoading(false);
        }
    };


    if (cart.length === 0) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[50vh]">
                <h1 className="text-2xl font-bold mb-4">Your Cart is Empty</h1>
                <button
                    onClick={() => router.push('/menu')}
                    className="bg-orange-600 text-white px-6 py-2 rounded hover:bg-orange-700"
                >
                    In Go To Menu
                </button>
            </div>
        );
    }

    return (
        <div className="max-w-2xl mx-auto p-4">
            <h1 className="text-3xl font-bold mb-8">Your Order</h1>

            <div className="space-y-4 mb-8">
                {cart.map(item => (
                    <div key={item.id} className="flex justify-between items-center bg-white p-4 rounded shadow dark:bg-gray-800">
                        <div>
                            <h3 className="font-bold">{item.name}</h3>
                            <p className="text-sm text-gray-500">₹{item.price} x {item.quantity}</p>
                        </div>
                        <div className="flex items-center gap-4">
                            <span className="font-bold">₹{(item.price * item.quantity).toFixed(2)}</span>

                            <button
                                onClick={() => removeFromCart(item.id)}
                                className="text-red-500 hover:text-red-700"
                            >
                                Remove
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            <div className="border-t pt-4 mb-8">
                <div className="flex justify-between text-xl font-bold">
                    <span>Total:</span>
                    <span>₹{total.toFixed(2)}</span>
                </div>

            </div>

            <div className="bg-gray-100 p-6 rounded-lg dark:bg-gray-800">
                <label className="block text-sm font-medium mb-2">Table Number</label>
                <input
                    type="number"
                    className="w-full p-2 border rounded mb-4"
                    value={tableNumber}
                    onChange={e => setTableNumber(e.target.value)}
                    placeholder="e.g. 12"
                />
                <button
                    onClick={handleCheckout}
                    disabled={loading}
                    className="w-full bg-green-600 text-white py-3 rounded font-bold hover:bg-green-700 disabled:opacity-50"
                >
                    {loading ? 'Processing...' : 'Place Order'}
                </button>
            </div>


            <Toast
                message={toastMsg}
                isVisible={showToast}
                onClose={() => setShowToast(false)}
            />
        </div>
    );


}
