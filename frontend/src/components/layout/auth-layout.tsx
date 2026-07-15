export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen flex">
      {/* Left Side */}
      <div className="hidden lg:flex w-1/2 bg-slate-900 text-white items-center justify-center">
        <div className="max-w-md space-y-6">
          <h1 className="text-5xl font-bold">
            CareerPilot AI
          </h1>

          <p className="text-lg text-slate-300">
            Your AI-powered career assistant for smarter resumes,
            better job matches, and faster applications.
          </p>
        </div>
      </div>

      {/* Right Side */}
      <div className="flex flex-1 items-center justify-center p-8">
        <div className="w-full max-w-md">
          {children}
        </div>
      </div>
    </div>
  );
}