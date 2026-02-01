
'use client';


import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '../../src/lib/api';
import Toast from '../../components/Toast';

export default function AdminPage() {
    const router = useRouter();
    const [items, setItems] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    // Toast State
    const [toastMsg, setToastMsg] = useState('');
    const [showToast, setShowToast] = useState(false);

    const showNotification = (msg: string) => {
        setToastMsg(msg);
        setShowToast(true);
    };

    // Form State
    const [newItem, setNewItem] = useState({

        name: '',
        description: '',
        price: '',
        category: '',
        image_url: ''
    });

    useEffect(() => {
        checkAuth();
        fetchMenu();
    }, []);

    const checkAuth = () => {
        const role = localStorage.getItem('role');
        if (role !== 'admin' && role !== 'manager') {
            router.push('/auth/login');
        }
    };

    const fetchMenu = async () => {
        try {
            const res = await api.get('/menu/');
            setItems(res.data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };


    const handleDelete = async (id: number) => {
        if (!confirm("Are you sure?")) return;
        try {
            await api.delete(`/menu/${id}`);
            fetchMenu(); // Reload
            showNotification("Item deleted");
        } catch (err) {
            showNotification("Failed to delete");
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await api.post('/menu/', {
                ...newItem,
                price: parseFloat(newItem.price)
            });
            setNewItem({ name: '', description: '', price: '', category: '', image_url: '' });
            fetchMenu();
            showNotification("Item added successfully!");
        } catch (err) {
            showNotification("Failed to add item");
        }
    };


    if (loading) return <div className="p-8">Loading Admin...</div>;

    return (
        <div className="max-w-4xl mx-auto">
            <div className="flex justify-between items-center mb-8">
                <h1 className="text-3xl font-bold">Admin Dashboard</h1>
                <button
                    onClick={() => {
                        localStorage.clear();
                        router.push('/');
                    }}
                    className="text-red-600 hover:text-red-800 font-medium"
                >
                    Logout
                </button>
            </div>

            <div className="grid md:grid-cols-2 gap-8">
                {/* Add Item Form */}
                <div className="bg-white p-6 rounded-lg shadow dark:bg-gray-800 h-fit">
                    <h2 className="text-xl font-semibold mb-4">Add New Item</h2>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <input
                            placeholder="Item Name"
                            className="w-full p-2 border rounded dark:bg-gray-700"
                            value={newItem.name}
                            onChange={e => setNewItem({ ...newItem, name: e.target.value })}
                            required
                        />
                        <input
                            placeholder="Description"
                            className="w-full p-2 border rounded dark:bg-gray-700"
                            value={newItem.description}
                            onChange={e => setNewItem({ ...newItem, description: e.target.value })}
                        />
                        <div className="flex gap-4">
                            <input
                                placeholder="Price"
                                type="number"
                                step="0.01"
                                className="w-full p-2 border rounded dark:bg-gray-700"
                                value={newItem.price}
                                onChange={e => setNewItem({ ...newItem, price: e.target.value })}
                                required
                            />
                            <input
                                placeholder="Category"
                                className="w-full p-2 border rounded dark:bg-gray-700"
                                value={newItem.category}
                                onChange={e => setNewItem({ ...newItem, category: e.target.value })}
                                required
                            />
                        </div>
                        <input
                            placeholder="Image URL"
                            className="w-full p-2 border rounded dark:bg-gray-700"
                            value={newItem.image_url}
                            onChange={e => setNewItem({ ...newItem, image_url: e.target.value })}
                        />
                        <button className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700">
                            Add Item
                        </button>
                    </form>
                </div>

                {/* Existing Items List */}
                <div className="bg-white p-6 rounded-lg shadow dark:bg-gray-800">
                    <h2 className="text-xl font-semibold mb-4">Current Menu ({items.length})</h2>
                    <div className="space-y-2 max-h-[500px] overflow-y-auto">
                        {items.map(item => (
                            <div key={item.id} className="flex justify-between items-center p-3 border-b dark:border-gray-700">
                                <div>

                                    <p className="font-medium">{item.name}</p>
                                    <p className="text-sm text-gray-500">₹{item.price.toFixed(2)} - {item.category}</p>
                                </div>

                                <div className="flex gap-2">
                                    {/* Edit would go here */}
                                    <button
                                        onClick={() => handleDelete(item.id)}
                                        className="text-red-500 hover:text-red-700 text-sm"
                                    >
                                        Delete
                                    </button>
                                </div>
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
