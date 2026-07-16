export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen flex bg-slate-950 text-slate-100">
      {/* Left Side — Branding */}
      <div className="hidden lg:flex w-1/2 bg-gradient-to-br from-slate-900 via-slate-900 to-blue-950 text-white items-center justify-center relative overflow-hidden">
        {/* Decorative gradient orbs */}
        <div className="absolute top-1/4 -left-20 w-64 h-64 bg-blue-600/20 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-10 w-48 h-48 bg-indigo-600/15 rounded-full blur-3xl" />
        
        <div className="max-w-md space-y-6 relative z-10">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
            CareerPilot AI
          </h1>

          <p className="text-lg text-slate-300 leading-relaxed">
            Your AI-powered career assistant for smarter resumes,
            better job matches, and faster applications.
          </p>

          <div className="space-y-3 pt-4">
            <div className="flex items-center gap-3 text-slate-400">
              <div className="h-8 w-8 rounded-lg bg-blue-500/10 flex items-center justify-center text-blue-400 text-sm">⚡</div>
              <span>AI-powered job discovery &amp; matching</span>
            </div>
            <div className="flex items-center gap-3 text-slate-400">
              <div className="h-8 w-8 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 text-sm">📄</div>
              <span>Automatic resume tailoring for 90+ ATS</span>
            </div>
            <div className="flex items-center gap-3 text-slate-400">
              <div className="h-8 w-8 rounded-lg bg-purple-500/10 flex items-center justify-center text-purple-400 text-sm">🚀</div>
              <span>One-click apply to supported career sites</span>
            </div>
          </div>
        </div>
      </div>

      {/* Right Side — Form */}
      <div className="flex flex-1 items-center justify-center p-8 bg-slate-950">
        <div className="w-full max-w-md">
          {children}
        </div>
      </div>
    </div>
  );
}