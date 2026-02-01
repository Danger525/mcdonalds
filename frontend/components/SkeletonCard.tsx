
export default function SkeletonCard() {
    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden border border-gray-100 dark:border-gray-700 animate-pulse">
            <div className="h-48 w-full bg-gray-300 dark:bg-gray-700" />
            <div className="p-4 space-y-3">
                <div className="flex justify-between items-center">
                    <div className="h-6 w-2/3 bg-gray-300 dark:bg-gray-700 rounded" />
                    <div className="h-6 w-12 bg-gray-300 dark:bg-gray-700 rounded-full" />
                </div>
                <div className="space-y-2">
                    <div className="h-4 w-full bg-gray-300 dark:bg-gray-700 rounded" />
                    <div className="h-4 w-5/6 bg-gray-300 dark:bg-gray-700 rounded" />
                </div>
                <div className="h-10 w-full bg-gray-300 dark:bg-gray-700 rounded mt-4" />
            </div>
        </div>
    );
}
