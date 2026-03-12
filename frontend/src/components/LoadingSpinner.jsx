import { Loader2 } from "lucide-react";

function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center gap-4 py-10">
      {/* Spinner */}
      <Loader2 size={40} className="animate-spin text-indigo-400" />

      {/* Text */}
      <p className="text-gray-400 text-sm">
        Analyzing your portfolio with AI...
      </p>
    </div>
  );
}

export default LoadingSpinner;
