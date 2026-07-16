import type { Metadata } from "next";
import { Inter } from "next/font/google";
import QueryProvider from "@/providers/query-provider";
import { AuthProvider } from "@/context/auth-context";
import { Toaster } from "sonner";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "CareerPilot AI",
  description: "AI-powered career assistant — smarter resumes, better job matches, faster applications.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${inter.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col font-sans">
        <QueryProvider>
          <AuthProvider>
            {children}
            <Toaster
              position="top-right"
              richColors
              closeButton
              theme="dark"
            />
          </AuthProvider>
        </QueryProvider>
      </body>
    </html>
  );
}