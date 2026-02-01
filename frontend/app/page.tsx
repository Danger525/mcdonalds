
import Link from 'next/link';
import Image from 'next/image';

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="relative h-[90vh] flex items-center justify-center overflow-hidden">
        {/* Background Image with Overlay */}
        <div className="absolute inset-0 z-0">
          <Image
            src="https://images.unsplash.com/photo-1544148103-0773bf10d330?q=80&w=3870&auto=format&fit=crop"
            alt="Delicious Food"
            fill
            className="object-cover"
            priority
          />
          <div className="absolute inset-0 bg-black/40 backdrop-blur-[2px]" />
        </div>

        {/* Content */}
        <div className="relative z-10 text-center px-4 max-w-4xl mx-auto space-y-8">
          <h1 className="text-5xl md:text-7xl font-extrabold text-white tracking-tight drop-shadow-lg leading-tight animate-fade-in-up">
            Taste the <span className="text-orange-500">Fastest</span> Future of Dining
          </h1>
          <p className="text-xl md:text-2xl text-gray-200 max-w-2xl mx-auto font-light drop-shadow-md">
            Skip the line. Order from your phone. Enjoy the food.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mt-8">

            <Link
              href="/menu"
              className="px-8 py-4 bg-orange-600 hover:bg-orange-500 text-white text-lg font-bold rounded-full shadow-xl transition-all hover:scale-105 hover:shadow-2xl flex items-center gap-2"
            >
              <span>Browse Menu</span>
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
              </svg>
            </Link>

          </div>
        </div>

        {/* Scroll Indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce text-white/80">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-8 h-8">
            <path strokeLinecap="round" strokeLinejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
          </svg>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 bg-background dark:bg-slate-900">
        <div className="container mx-auto max-w-6xl">
          <h2 className="text-3xl font-bold text-center mb-12 text-foreground">Why SmartMenu?</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="glass-card p-8 rounded-2xl text-center hover:-translate-y-2 transition-transform duration-300">
              <div className="w-16 h-16 bg-orange-100 text-orange-600 rounded-full flex items-center justify-center mx-auto mb-6 text-2xl">
                ⚡
              </div>
              <h3 className="text-xl font-bold mb-3 text-gray-800 dark:text-white">Lightning Fast</h3>
              <p className="text-gray-600 dark:text-gray-400">Order in seconds directly from your table. No waiting for waiters.</p>
            </div>

            {/* Feature 2 */}
            <div className="glass-card p-8 rounded-2xl text-center hover:-translate-y-2 transition-transform duration-300">
              <div className="w-16 h-16 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mx-auto mb-6 text-2xl">
                🥘
              </div>
              <h3 className="text-xl font-bold mb-3 text-gray-800 dark:text-white">Live Kitchen Sync</h3>
              <p className="text-gray-600 dark:text-gray-400">Watch your order status update in real-time as the kitchen prepares it.</p>
            </div>

            {/* Feature 3 */}
            <div className="glass-card p-8 rounded-2xl text-center hover:-translate-y-2 transition-transform duration-300">
              <div className="w-16 h-16 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center mx-auto mb-6 text-2xl">
                📱
              </div>
              <h3 className="text-xl font-bold mb-3 text-gray-800 dark:text-white">Contactless</h3>
              <p className="text-gray-600 dark:text-gray-400">Safe, clean, and digital. The modern way to dine out.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

