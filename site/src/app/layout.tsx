import type { Metadata } from "next";
import { Nunito } from "next/font/google";
import "./globals.css";
import { Header, Footer } from "./page";

const inter = Nunito({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Takbuff | About",
  icons: '/logo_takbuff_84.png',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Header />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
