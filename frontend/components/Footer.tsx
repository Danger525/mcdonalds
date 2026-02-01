
export default function Footer() {
    return (
        <footer className="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800 py-12 mt-auto">
            <div className="container mx-auto px-4">
                <div className="grid md:grid-cols-4 gap-8 mb-8">
                    <div className="col-span-1 md:col-span-2">
                        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">SmartMenu</h2>
                        <p className="text-gray-600 dark:text-gray-400 max-w-sm">
                            The future of dining is here. Experience seamless ordering, real-time updates, and delicious food delivered fast.
                        </p>
                    </div>
                    <div>
                        <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Links</h3>

                        <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                            <li><a href="/" className="hover:text-orange-500">Home</a></li>
                            <li><a href="/menu" className="hover:text-orange-500">Menu</a></li>
                            <li><a href="/cart" className="hover:text-orange-500">Cart</a></li>
                            <li><a href="/auth/login" className="hover:text-orange-500">Login</a></li>
                            <li><a href="/auth/kitchen/login" className="hover:text-blue-500 text-sm mt-4 block">Kitchen Staff</a></li>
                        </ul>

                    </div>
                    <div>
                        <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Contact</h3>
                        <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                            <li>support@smartmenu.com</li>
                            <li>+1 (555) 123-4567</li>
                            <li>123 Foodie Lane</li>
                        </ul>
                    </div>
                </div>
                <div className="text-center pt-8 border-t border-gray-100 dark:border-gray-800 text-gray-500 text-sm">
                    © 2024 SmartMenu Inc. All rights reserved.
                </div>
            </div>
        </footer>
    );
}
