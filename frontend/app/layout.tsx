
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { CartProvider } from "../src/context/CartContext";


const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Smart Menu",
  description: "Digital Menu & Ordering System",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className} suppressHydrationWarning={true}>

        <CartProvider>
          <div className="flex flex-col min-h-screen">
            <Navbar />
            <main className="container mx-auto p-4 flex-grow">
              {children}
            </main>
            <Footer />
          </div>
        </CartProvider>

      </body>
    </html>
  );
}
