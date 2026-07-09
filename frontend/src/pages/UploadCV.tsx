import { useState } from "react";
import axios from "axios";

const API = "http://localhost:8000";

export default function UploadCV() {
    const [file, setFile] = useState<File | null>(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);

    const uploadCV = async () => {
        if (!file) return;

        const token = localStorage.getItem("access_token");

        const formData = new FormData();
        formData.append("file", file);

        try {
            setLoading(true);

            const res = await axios.post(
                `${API}/match-cv`,
                formData,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        "Content-Type": "multipart/form-data",
                    },
                }
            );

            setResult(res.data);
        } catch (err) {
            console.error(err);
            alert("Upload failed.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-6xl mx-auto p-8">

            <h1 className="text-3xl font-bold mb-8">
                AI Resume Analyzer
            </h1>

            {/* Upload Card */}
            <div className="bg-white rounded-xl shadow p-8 mb-8">

                <input
                    type="file"
                    accept=".pdf,.doc,.docx"
                    onChange={(e) =>
                        setFile(e.target.files?.[0] || null)
                    }
                />

                <button
                    onClick={uploadCV}
                    disabled={loading}
                    className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg"
                >
                    {loading ? "Analyzing..." : "Upload CV"}
                </button>

            </div>

            {/* Loading */}
            {loading && (
                <div className="bg-white rounded-xl shadow p-6">
                    <h2 className="text-xl font-semibold">
                        AI is analyzing your resume...
                    </h2>

                    <p className="mt-2 text-gray-500">
                        Extracting skills...
                    </p>

                    <p className="text-gray-500">
                        Matching jobs...
                    </p>

                    <p className="text-gray-500">
                        Generating career advice...
                    </p>
                </div>
            )}

            {/* Results */}
            {result && (

                <div className="space-y-8">

                    {/* Summary */}

                    <div className="bg-white rounded-xl shadow p-6">

                        <h2 className="text-2xl font-bold mb-4">
                            Resume Summary
                        </h2>

                        <p>
                            Characters: {result.cv_summary.characters}
                        </p>

                        <div className="flex flex-wrap gap-2 mt-4">

                            {result.cv_summary.skills_found.map(
                                (skill: string) => (
                                    <span
                                        key={skill}
                                        className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full"
                                    >
                                        {skill}
                                    </span>
                                )
                            )}

                        </div>

                    </div>

                    {/* Match Score */}

                    <div className="bg-green-100 rounded-xl p-6">

                        <h2 className="text-2xl font-bold">
                            AI Match Score
                        </h2>

                        <div className="text-5xl font-bold mt-3">
                            {result.career_analysis.overall_match}%
                        </div>

                    </div>

                    {/* Top Matching Jobs */}

                    <div className="bg-white rounded-xl shadow p-6">

                        <h2 className="text-2xl font-bold mb-6">
                            Top Matching Jobs
                        </h2>

                        <div className="grid md:grid-cols-2 gap-5">

                            {result.recommendations.map((job: any) => (

                                <div
                                    key={job.id}
                                    className="border rounded-xl p-5 hover:shadow-lg transition"
                                >

                                    <h3 className="text-xl font-semibold">
                                        {job.title}
                                    </h3>

                                    <p className="text-gray-600 mt-2">
                                        🏢 {job.company}
                                    </p>

                                    <p className="text-gray-600">
                                        📍 {job.location}
                                    </p>

                                    <div className="mt-4 flex justify-between items-center">

                                        <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm">
                                            {(job.score * 100).toFixed(0)}% Match
                                        </span>

                                        <a
                                            href={job.link}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
                                        >
                                            Apply
                                        </a>

                                    </div>

                                </div>

                            ))}

                        </div>

                    </div>

                    {/* Strengths */}

                    <div className="bg-white rounded-xl shadow p-6">

                        <h2 className="text-2xl font-bold mb-5">
                            💪 Your Strengths
                        </h2>

                        <div className="grid md:grid-cols-2 gap-3">

                            {result.career_analysis.strengths.map((item: string) => (

                                <div
                                    key={item}
                                    className="bg-green-50 border border-green-200 rounded-lg p-4"
                                >
                                    ✅ {item}
                                </div>

                            ))}

                        </div>

                    </div>

                    {/* Missing Skills */}

                    <div className="bg-white rounded-xl shadow p-6">

                        <h2 className="text-2xl font-bold mb-5">
                            📚 Missing Skills
                        </h2>

                        <div className="flex flex-wrap gap-3">

                            {result.career_analysis.missing_skills.map((skill: string) => (

                                <span
                                    key={skill}
                                    className="bg-red-100 text-red-700 px-4 py-2 rounded-full"
                                >
                                    {skill}
                                </span>

                            ))}

                        </div>

                    </div>

                    {/* AI Recommendation */}

                    <div className="bg-blue-50 rounded-xl shadow p-6">

                        <h2 className="text-2xl font-bold mb-5">
                            💡 AI Career Recommendation
                        </h2>

                        <p className="text-lg leading-8 text-gray-700">
                            {result.career_analysis.recommendation}
                        </p>

                    </div>

                    {/* Learning Path */}

                    <div className="bg-white rounded-xl shadow p-6">

                        <h2 className="text-2xl font-bold mb-5">
                            🛣 Learning Roadmap
                        </h2>

                        <div className="space-y-4">

                            {result.career_analysis.learning_path.map(
                                (step: string, index: number) => (

                                    <div
                                        key={index}
                                        className="flex items-center gap-4"
                                    >

                                        <div className="w-10 h-10 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold">

                                            {index + 1}

                                        </div>

                                        <div className="bg-gray-100 rounded-lg p-4 flex-1">

                                            {step}

                                        </div>

                                    </div>

                                )
                            )}

                        </div>

                    </div>

                </div>

            )}

        </div>
    );
}