
import Image from 'next/image';


interface MenuItem {
    id: number;
    name: string;
    description: string;
    price: number;
    category: string;
    image_url: string;
    calories?: number;
}


interface MenuCardProps {
    item: MenuItem;
    onAdd: () => void;
}

export default function MenuCard({ item, onAdd }: MenuCardProps) {
    // const { addToCart } = useCart(); // Handled by parent


    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow border border-gray-100 dark:border-gray-700">
            <div className="relative h-48 w-full bg-gray-200">
                {item.image_url ? (
                    <img
                        src={item.image_url}
                        alt={item.name}
                        className="w-full h-full object-cover"
                    />
                ) : (
                    <div className="flex items-center justify-center h-full text-gray-400">No Image</div>
                )}
            </div>
            <div className="p-4">
                <div className="flex justify-between items-start mb-2">
                    <h3 className="text-lg font-bold text-gray-900 dark:text-white line-clamp-1">{item.name}</h3>
                    <span className="bg-orange-100 text-orange-800 text-xs px-2 py-1 rounded-full font-semibold">
                        ₹{item.price.toFixed(2)}
                    </span>

                </div>
                <p className="text-gray-600 dark:text-gray-300 text-sm mb-4 line-clamp-2 h-10">
                    {item.description}
                </p>

                <button
                    onClick={onAdd}
                    className="w-full bg-orange-600 hover:bg-orange-700 text-white font-medium py-2 px-4 rounded transition-colors active:scale-95"
                >
                    Add to Order
                </button>

            </div>
        </div>
    );
}
