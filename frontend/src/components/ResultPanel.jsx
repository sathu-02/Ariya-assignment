import ReactMarkdown from "react-markdown";
import ScoreCharts from "./ScoreCharts";

function ResultPanel({ result }) {
  if (!result || !result.career_strategy) {
    return null;
  }

  return (
    <div className="space-y-8">
      {/* Score Charts Section */}
      {result.scores && (
        <ScoreCharts scores={result.scores} />
      )}

      {/* Detailed Report */}
      <div className="bg-slate-900/70 border border-slate-800 rounded-xl p-8 shadow-xl backdrop-blur">
        <h2 className="text-2xl font-semibold mb-6 text-center text-white">
          AI Career Intelligence Report
        </h2>
        <div className="prose prose-invert prose-indigo max-w-none text-gray-300 prose-headings:text-white prose-strong:text-gray-200 prose-li:text-gray-300">
          <ReactMarkdown>{result.career_strategy}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
}

export default ResultPanel;
