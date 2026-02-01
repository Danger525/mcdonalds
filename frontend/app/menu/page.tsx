
'use client';

import { useEffect, useState } from 'react';

import api from '../../src/lib/api';
import MenuCard from '../../components/MenuCard';
import SkeletonCard from '../../components/SkeletonCard';
import Toast from '../../components/Toast';
import { useCart } from '../../src/context/CartContext';

interface MenuItem {
    id: number;
    name: string;
    description: string;
    price: number;
    category: string;
    image_url: string;
    calories?: number;
}

export default function MenuPage() {
    const [items, setItems] = useState<MenuItem[]>([]);
    const [categories, setCategories] = useState<string[]>([]);
    const [selectedCategory, setSelectedCategory] = useState<string>('All');
    const [loading, setLoading] = useState(true);
    const { addToCart } = useCart();

    // Toast State
    const [toastMsg, setToastMsg] = useState('');
    const [showToast, setShowToast] = useState(false);

    useEffect(() => {
        fetchMenu();
    }, []);

    const fetchMenu = async () => {
        try {
            const res = await api.get('/menu/');
            setItems(res.data);

            const cats = Array.from(new Set(res.data.map((i: MenuItem) => i.category))) as string[];
            setCategories(['All', ...cats]);
        } catch (err) {
            console.error("Failed to load menu", err);
        } finally {
            // Fake delay to show off the nice skeletons
            setTimeout(() => setLoading(false), 800);
        }
    };

    const handleAddToCart = (item: MenuItem) => {
        addToCart({
            id: item.id,
            name: item.name,
            price: item.price,
            quantity: 1
        });
        setToastMsg(`Added ${item.name} to order`);
        setShowToast(true);
    };

    const filteredItems = selectedCategory === 'All'
        ? items
        : items.filter(i => i.category === selectedCategory);

    return (
        <div className="min-h-screen relative pb-20">
            <h1 className="text-4xl font-extrabold mb-8 text-center bg-clip-text text-transparent bg-gradient-to-r from-orange-600 to-orange-400 py-2">
                Our Menu
            </h1>

            {/* Category Filter */}
            <div className="sticky top-[72px] z-40 bg-background/80 backdrop-blur-md py-4 mb-8 border-b border-gray-200 dark:border-gray-800">
                <div className="flex gap-3 overflow-x-auto justify-center px-4 no-scrollbar">
                    {categories.map(cat => (
                        <button
                            key={cat}
                            onClick={() => setSelectedCategory(cat)}
                            className={`px-5 py-2 rounded-full whitespace-nowrap transition-all duration-300 font-medium border ${selectedCategory === cat
                                ? 'bg-orange-600 text-white border-orange-600 shadow-md scale-105'
                                : 'bg-white text-gray-600 border-gray-200 hover:border-orange-400 hover:text-orange-600 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-700'
                                }`}
                        >
                            {cat}
                        </button>
                    ))}
                    {loading && categories.length === 0 && (
                        // Skeleton for categories
                        Array(4).fill(0).map((_, i) => (
                            <div key={i} className="h-10 w-24 bg-gray-200 dark:bg-gray-700 rounded-full animate-pulse" />
                        ))
                    )}
                </div>
            </div>

            {/* Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 px-4">
                {loading ? (
                    Array(8).fill(0).map((_, i) => <SkeletonCard key={i} />)
                ) : (
                    filteredItems.map((item, index) => (
                        <div key={item.id} className="animate-fade-in-up" style={{ animationDelay: `${index * 50}ms` }}>
                            <MenuCard item={item} onAdd={() => handleAddToCart(item)} />
                        </div>
                    ))
                )}
            </div>

            <Toast
                message={toastMsg}
                isVisible={showToast}
                onClose={() => setShowToast(false)}
            />

            {!loading && filteredItems.length === 0 && (
                <div className="text-center text-gray-500 mt-20">
                    <p className="text-xl">No items found in this category.</p>
                </div>
            )}
        </div>
    );
}

