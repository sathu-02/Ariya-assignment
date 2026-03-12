import { BrainCircuit } from "lucide-react";

function Navbar() {
  return (
    <header className="w-full border-b border-slate-800 backdrop-blur bg-slate-950/60 sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo + Title */}
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-indigo-600/20 border border-indigo-500/30">
            <BrainCircuit size={22} className="text-indigo-400" />
          </div>

          <span className="font-semibold text-lg tracking-tight">
            Career Intelligence Agent
          </span>
        </div>

        {/* Right Side Info */}
        <div className="text-sm text-gray-400 hidden md:block">
          AI Portfolio Analysis
        </div>
      </div>
    </header>
  );
}

export default Navbar;
