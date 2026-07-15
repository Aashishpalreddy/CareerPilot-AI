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


        <nav className="flex flex-col gap-2">


          <Link
            href="/dashboard"
            className="w-full px-3 py-2 rounded-md hover:bg-gray-100"
          >
            Dashboard
          </Link>


          <Link
            href="/resumes"
            className="w-full px-3 py-2 rounded-md hover:bg-gray-100"
          >
            Resumes
          </Link>


          <Link
            href="/jobs"
            className="w-full px-3 py-2 rounded-md hover:bg-gray-100"
          >
            Jobs
          </Link>


          <Link
            href="/saved-jobs"
            className="w-full px-3 py-2 rounded-md hover:bg-gray-100"
          >
            Saved Jobs
          </Link>


        </nav>


      </aside>



      {/* Main Content */}
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