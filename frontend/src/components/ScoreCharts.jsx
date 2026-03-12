import { PieChart, Pie, Cell, ResponsiveContainer, RadialBarChart, RadialBar } from "recharts";

const COLORS = {
  indigo: "#818cf8",
  violet: "#a78bfa",
  emerald: "#34d399",
  amber: "#fbbf24",
  rose: "#fb7185",
  cyan: "#22d3ee",
  blue: "#60a5fa",
};

function getScoreColor(score) {
  if (score >= 80) return "#34d399";
  if (score >= 60) return "#818cf8";
  if (score >= 40) return "#fbbf24";
  return "#fb7185";
}

function getScoreLabel(score) {
  if (score >= 80) return "Excellent";
  if (score >= 60) return "Good";
  if (score >= 40) return "Average";
  return "Needs Work";
}

function ScoreCharts({ scores }) {
  if (!scores) return null;

  const overallScore = scores.overall || 0;
  const scoreColor = getScoreColor(overallScore);

  // Radial gauge data
  const gaugeData = [
    { name: "Score", value: overallScore, fill: scoreColor },
  ];

  // Category breakdown for bar chart
  const categories = [
    { name: "Technical Skills", score: scores.technical_skills || 0, fill: COLORS.indigo },
    { name: "Projects", score: scores.projects || 0, fill: COLORS.violet },
    { name: "Experience", score: scores.experience || 0, fill: COLORS.emerald },
    { name: "GitHub Activity", score: scores.github || 0, fill: COLORS.cyan },
    { name: "Role Fit", score: scores.role_fit || 0, fill: COLORS.blue },
  ];

  // Pie chart for skill distribution
  const skillDistribution = [
    { name: "Matched", value: scores.skills_matched || 0, color: COLORS.emerald },
    { name: "Missing", value: scores.skills_missing || 0, color: COLORS.rose },
  ];

  return (
    <div className="space-y-6">
      {/* Top Row: Overall Score + Category Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

        {/* Overall Score - Radial Gauge */}
        <div className="bg-slate-900/70 border border-slate-800 rounded-xl p-6 shadow-xl backdrop-blur flex flex-col items-center justify-center">
          <h3 className="text-sm font-medium text-gray-400 mb-2 tracking-wide uppercase">Career Readiness</h3>
          <div className="relative w-44 h-44">
            <ResponsiveContainer width="100%" height="100%">
              <RadialBarChart
                innerRadius="75%"
                outerRadius="100%"
                data={gaugeData}
                startAngle={225}
                endAngle={-45}
                barSize={12}
              >
                <RadialBar
                  dataKey="value"
                  cornerRadius={10}
                  background={{ fill: "#1e293b" }}
                />
              </RadialBarChart>
            </ResponsiveContainer>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-4xl font-bold" style={{ color: scoreColor }}>
                {overallScore}
              </span>
              <span className="text-xs text-gray-400 mt-0.5">{getScoreLabel(overallScore)}</span>
            </div>
          </div>
        </div>

        {/* Category Breakdown - Horizontal Bars */}
        <div className="md:col-span-2 bg-slate-900/70 border border-slate-800 rounded-xl p-6 shadow-xl backdrop-blur">
          <h3 className="text-sm font-medium text-gray-400 mb-4 tracking-wide uppercase">Score Breakdown</h3>
          <div className="space-y-3">
            {categories.map((cat) => (
              <div key={cat.name} className="flex items-center gap-3">
                <span className="text-xs text-gray-400 w-28 text-right shrink-0">{cat.name}</span>
                <div className="flex-1 bg-slate-800 rounded-full h-3 overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-700 ease-out"
                    style={{ width: `${cat.score}%`, backgroundColor: cat.fill }}
                  />
                </div>
                <span className="text-xs font-semibold w-8 text-right" style={{ color: cat.fill }}>
                  {cat.score}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Row: Skills Match Pie + Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

        {/* Skills Match Donut */}
        <div className="bg-slate-900/70 border border-slate-800 rounded-xl p-6 shadow-xl backdrop-blur flex flex-col items-center">
          <h3 className="text-sm font-medium text-gray-400 mb-2 tracking-wide uppercase">Skill Match</h3>
          <div className="w-36 h-36">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={skillDistribution}
                  innerRadius={40}
                  outerRadius={60}
                  paddingAngle={4}
                  dataKey="value"
                  animationBegin={200}
                  animationDuration={800}
                >
                  {skillDistribution.map((entry, i) => (
                    <Cell key={i} fill={entry.color} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex gap-4 mt-2">
            <div className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: COLORS.emerald }} />
              <span className="text-xs text-gray-400">Matched ({scores.skills_matched || 0})</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: COLORS.rose }} />
              <span className="text-xs text-gray-400">Missing ({scores.skills_missing || 0})</span>
            </div>
          </div>
        </div>

        {/* Stat Cards */}
        <div className="md:col-span-2 grid grid-cols-2 gap-4">
          <StatCard label="Experience Level" value={scores.experience_level || "N/A"} color={COLORS.amber} />
          <StatCard label="Target Roles" value={`${scores.target_roles_count || 0} roles`} color={COLORS.violet} />
          <StatCard label="GitHub Repos" value={scores.repo_count || "0"} color={COLORS.cyan} />
          <StatCard label="Portfolio Score" value={`${scores.portfolio_score || 0}%`} color={COLORS.indigo} />
        </div>
      </div>
    </div>
  );
}

function StatCard({ label, value, color }) {
  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-xl p-5 shadow-lg backdrop-blur flex flex-col justify-between">
      <span className="text-xs text-gray-500 uppercase tracking-wide">{label}</span>
      <span className="text-2xl font-bold mt-2" style={{ color }}>{value}</span>
    </div>
  );
}

export default ScoreCharts;
