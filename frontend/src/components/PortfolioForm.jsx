import { useState, useCallback } from "react";
import { Github, FileText, Sparkles, UploadCloud, File, X, Briefcase, Clock, Plus } from "lucide-react";

const EXPERIENCE_LEVELS = [
  "Fresher",
  "1 Year",
  "2 Years",
  "3 Years",
  "4 Years",
  "5+ Years",
  "7+ Years",
  "10+ Years",
];

function PortfolioForm({ onAnalyze }) {
  const [cvText, setCvText] = useState("");
  const [githubUrl, setGithubUrl] = useState("");
  const [fileName, setFileName] = useState("");
  const [fileObj, setFileObj] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [experienceLevel, setExperienceLevel] = useState("");
  const [targetRoles, setTargetRoles] = useState([]);
  const [roleInput, setRoleInput] = useState("");

  const processFile = (file) => {
    if (!file) return;

    if (
      file.type === "application/pdf" ||
      file.name.toLowerCase().endsWith(".pdf") ||
      file.type === "application/vnd.openxmlformats-officedocument.wordprocessingml.document" ||
      file.name.toLowerCase().endsWith(".docx")
    ) {
      setFileName(file.name);
      setFileObj(file);
      setCvText("");
    } else {
      alert("Please upload a PDF or DOCX file.");
      setFileName("");
      setFileObj(null);
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    processFile(file);
  };

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      processFile(e.dataTransfer.files[0]);
    }
  }, []);

  const clearFile = () => {
    setFileName("");
    setFileObj(null);
  };

  const addRole = () => {
    const role = roleInput.trim();
    if (!role) return;
    if (targetRoles.length >= 5) {
      alert("You can add up to 5 target roles.");
      return;
    }
    if (targetRoles.includes(role)) {
      alert("This role is already added.");
      return;
    }
    setTargetRoles([...targetRoles, role]);
    setRoleInput("");
  };

  const removeRole = (index) => {
    setTargetRoles(targetRoles.filter((_, i) => i !== index));
  };

  const handleRoleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      addRole();
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!fileObj && !cvText.trim()) {
      alert("Please provide your CV by uploading a file or pasting the text.");
      return;
    }

    onAnalyze(cvText, githubUrl, fileObj, experienceLevel, targetRoles);
  };

  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-xl p-8 shadow-xl backdrop-blur">
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* CV Input Section */}
        <div>
          <label className="flex items-center gap-2 text-sm font-medium text-gray-300 mb-2">
            <FileText size={16} />
            CV / Resume
          </label>
          
          {/* File Upload Area */}
          <div 
            className={`mb-4 w-full border-2 border-dashed rounded-lg p-6 text-center transition-colors cursor-pointer
              ${isDragging ? 'border-indigo-500 bg-indigo-500/10' : 'border-slate-700 bg-slate-950/50 hover:bg-slate-900'}
              ${fileName ? 'hidden' : 'block'}
            `}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => document.getElementById('cv-upload').click()}
          >
            <input 
              type="file" 
              id="cv-upload" 
              className="hidden" 
              accept=".pdf,.docx"
              onChange={handleFileUpload}
            />
            <div className="flex flex-col items-center justify-center space-y-2">
              <UploadCloud className="text-gray-400" size={32} />
              <p className="text-sm text-gray-300">
                <span className="text-indigo-400 font-medium">Click to upload</span> or drag and drop
              </p>
              <p className="text-xs text-gray-500">PDF or DOCX (Max 5MB)</p>
            </div>
          </div>

          {/* Selected File Indicator */}
          {fileName && (
            <div className="mb-4 flex items-center justify-between bg-slate-800 border border-slate-700 rounded-lg px-4 py-3">
              <div className="flex items-center gap-3 overflow-hidden">
                <File className="text-indigo-400 flex-shrink-0" size={20} />
                <span className="text-sm text-gray-200 truncate">{fileName}</span>
              </div>
              <button 
                type="button" 
                onClick={clearFile}
                className="text-gray-400 hover:text-red-400 transition-colors p-1"
                title="Remove file"
              >
                <X size={16} />
              </button>
            </div>
          )}

          {/* Textarea Fallback */}
          <div className="relative">
            <label className="text-xs text-gray-500 mb-1 block">
              {fileName ? "Extracted Text Preview (Edit if needed)" : "Or paste your resume text manually"}
            </label>
            <textarea
              value={cvText}
              onChange={(e) => setCvText(e.target.value)}
              placeholder="Paste your resume or CV text here..."
              rows={fileName ? 4 : 8}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-3 text-sm text-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-y"
            />
          </div>
        </div>

        {/* Experience Level + GitHub URL - Side by Side */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {/* Experience Level */}
          <div>
            <label className="flex items-center gap-2 text-sm font-medium text-gray-300 mb-2">
              <Clock size={16} />
              Experience Level
            </label>
            <select
              value={experienceLevel}
              onChange={(e) => setExperienceLevel(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-3 text-sm text-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent appearance-none cursor-pointer"
            >
              <option value="" className="bg-slate-950">Select experience level</option>
              {EXPERIENCE_LEVELS.map((level) => (
                <option key={level} value={level} className="bg-slate-950">{level}</option>
              ))}
            </select>
          </div>

          {/* GitHub URL */}
          <div>
            <label className="flex items-center gap-2 text-sm font-medium text-gray-300 mb-2">
              <Github size={16} />
              GitHub Profile URL
            </label>
            <input
              type="text"
              value={githubUrl}
              onChange={(e) => setGithubUrl(e.target.value)}
              placeholder="https://github.com/yourusername"
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-3 text-sm text-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* Target Roles */}
        <div>
          <label className="flex items-center gap-2 text-sm font-medium text-gray-300 mb-2">
            <Briefcase size={16} />
            Target Job Titles
            <span className="text-xs text-gray-500 font-normal ml-1">
              ({targetRoles.length}/5)
            </span>
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              value={roleInput}
              onChange={(e) => setRoleInput(e.target.value)}
              onKeyDown={handleRoleKeyDown}
              placeholder="e.g. Full Stack Developer, Data Scientist..."
              disabled={targetRoles.length >= 5}
              className="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-4 py-3 text-sm text-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:opacity-50"
            />
            <button
              type="button"
              onClick={addRole}
              disabled={targetRoles.length >= 5}
              className="bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-700 disabled:cursor-not-allowed text-white px-4 py-3 rounded-lg transition-colors flex items-center gap-1"
            >
              <Plus size={16} />
              Add
            </button>
          </div>

          {/* Role Tags */}
          {targetRoles.length > 0 && (
            <div className="flex flex-wrap gap-2 mt-3">
              {targetRoles.map((role, index) => (
                <span
                  key={index}
                  className="inline-flex items-center gap-1.5 bg-indigo-500/20 border border-indigo-500/30 text-indigo-300 px-3 py-1.5 rounded-full text-xs font-medium"
                >
                  {role}
                  <button
                    type="button"
                    onClick={() => removeRole(index)}
                    className="hover:text-red-400 transition-colors"
                  >
                    <X size={12} />
                  </button>
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Submit Button */}
        <div className="flex justify-center pt-4">
          <button
            type="submit"
            className="flex items-center gap-2 transition-all px-8 py-3.5 rounded-lg font-medium text-white shadow-lg bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 hover:shadow-indigo-500/25 hover:shadow-xl"
          >
            <Sparkles size={18} />
            Analyze Portfolio
          </button>
        </div>
      </form>
    </div>
  );
}

export default PortfolioForm;
