"use client";

import Link from "next/link";
import { useAuth } from "@/context/auth-context";
import { Button } from "@/components/ui/button";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {

  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen flex">

      {/* Sidebar */}
      <aside className="w-64 border-r p-6">

        <h1 className="text-xl font-bold mb-8">
          CareerPilot AI
        </h1>


        <nav className="space-y-4">

          <Link href="/dashboard">
            Dashboard
          </Link>

          <Link href="/resumes">
            Resumes
          </Link>

          <Link href="/jobs">
            Jobs
          </Link>

          <Link href="/saved-jobs">
            Saved Jobs
          </Link>

        </nav>

      </aside>


      {/* Main */}
      <main className="flex-1">


        <header className="h-16 border-b flex items-center justify-between px-8">

          <div>
            Welcome, {user?.full_name}
          </div>


          <Button
            variant="outline"
            onClick={logout}
          >
            Logout
          </Button>


        </header>


        <section className="p-8">

          {children}

        </section>


      </main>

    </div>
  );
}