import { useState } from "react";
import Navbar from "./components/Navbar";
import PortfolioForm from "./components/PortfolioForm";
import ResultPanel from "./components/ResultPanel";
import LoadingSpinner from "./components/LoadingSpinner";

function App() {
  const [loading, setLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";
  const analyzePortfolio = async (cvText, githubUrl, fileObj, experienceLevel, targetRoles) => {
    setLoading(true);
    setAnalysisResult(null);

    try {
      const formData = new FormData();
      if (fileObj) {
        formData.append("resume", fileObj);
      }
      if (cvText.trim() !== "") formData.append("cv_text", cvText);
      if (githubUrl.trim() !== "") formData.append("github_url", githubUrl);
      if (experienceLevel) formData.append("experience_level", experienceLevel);
      if (targetRoles && targetRoles.length > 0) {
        formData.append("target_roles", JSON.stringify(targetRoles));
      }

      const response = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Server error");
      }

      setAnalysisResult(data);
    } catch (error) {
      console.error("Analysis failed:", error);
      alert("Failed to analyze portfolio. Please try again.");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-black text-white">
      <Navbar />

      <main className="max-w-6xl mx-auto px-6 py-12">
        {/* Hero Section */}
        <div className="text-center mb-14">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Career Portfolio Intelligence Agent
          </h1>

          <p className="text-gray-400 max-w-2xl mx-auto text-lg">
            Upload your CV and GitHub profile to receive AI-powered insights on
            your career readiness, skill gaps, and improvement strategy.
          </p>
        </div>

        {/* Input Form */}
        <div className="mb-10">
          <PortfolioForm onAnalyze={analyzePortfolio} />
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex justify-center mt-12">
            <LoadingSpinner />
          </div>
        )}

        {/* Result Panel */}
        {analysisResult && !loading && (
          <div className="mt-12">
            <ResultPanel result={analysisResult} />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
