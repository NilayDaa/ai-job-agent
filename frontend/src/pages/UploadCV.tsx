import { useState } from "react";

import DashboardLayout from "../layouts/DashboardLayout";
import api from "../api/api";

import type { MatchCVResponse } from "../types/cv";

export default function UploadCV() {

    const [file, setFile] = useState<File | null>(null);

    const [loading, setLoading] = useState(false);

    const [result, setResult] =
        useState<MatchCVResponse | null>(null);

    async function uploadCV() {

        if (!file) return;

        const formData = new FormData();

        formData.append("file", file);

        try {

            setLoading(true);

            const response =
                await api.post(
                    "/match-cv",
                    formData,
                    {
                        headers: {
                            "Content-Type":
                                "multipart/form-data",
                        },
                    }
                );

            setResult(response.data);

        } catch (error) {

            console.error(error);

        } finally {

            setLoading(false);

        }
    }

    return (

        <DashboardLayout>

            <h1 className="mb-6 text-3xl font-bold">
                Upload CV
            </h1>

            <div className="rounded-lg bg-white p-6 shadow">

                <input
                    type="file"
                    accept=".pdf"
                    onChange={(e) =>
                        setFile(
                            e.target.files
                                ? e.target.files[0]
                                : null
                        )
                    }
                />

                <button
                    onClick={uploadCV}
                    className="mt-4 rounded bg-blue-600 px-6 py-2 text-white"
                >
                    Upload
                </button>

            </div>

            {loading && (

                <div className="mt-6">

                    Analyzing your CV...

                </div>

            )}

            {result && (

                <div className="mt-8 space-y-6">

                    <div className="rounded-lg bg-white p-6 shadow">

                        <h2 className="mb-4 text-xl font-bold">

                            CV Summary

                        </h2>

                        <p>

                            Characters:

                            {result.cv_summary.characters}

                        </p>

                        <p>

                            Top Matches:

                            {result.cv_summary.top_matches}

                        </p>

                        <div className="mt-3">

                            {result.cv_summary.skills_found.map(
                                (skill) => (

                                    <span
                                        key={skill}
                                        className="mr-2 inline-block rounded bg-blue-100 px-3 py-1"
                                    >
                                        {skill}
                                    </span>

                                )
                            )}

                        </div>

                    </div>

                    <div className="rounded-lg bg-white p-6 shadow">

                        <h2 className="mb-4 text-xl font-bold">

                            AI Career Analysis

                        </h2>

                        <p>

                            Overall Match:

                            {result.career_analysis.overall_match}%

                        </p>

                        <h3 className="mt-4 font-semibold">

                            Strengths

                        </h3>

                        <ul className="list-disc pl-5">

                            {result.career_analysis.strengths?.map(
                                (item) => (
                                    <li key={item}>
                                        {item}
                                    </li>
                                )
                            )}

                        </ul>

                        <h3 className="mt-4 font-semibold">

                            Missing Skills

                        </h3>

                        <ul className="list-disc pl-5">

                            {result.career_analysis.missing_skills?.map(
                                (item) => (
                                    <li key={item}>
                                        {item}
                                    </li>
                                )
                            )}

                        </ul>

                        <h3 className="mt-4 font-semibold">

                            Recommendation

                        </h3>

                        <p>

                            {
                                result.career_analysis
                                    .recommendation
                            }

                        </p>

                    </div>

                    <div className="
bg-white
rounded-xl
shadow
p-6
">


<h2 className="
text-2xl
font-bold
mb-5
">

Recommended Jobs

</h2>



<div className="
space-y-4
">


{
result.recommendations.map(
(job:any)=>(


<div

key={job.id}

className="
border
rounded-lg
p-5
hover:shadow-md
transition
"


>


<h3 className="
text-xl
font-bold
">

{job.title}

</h3>



<p className="text-gray-600">

Company:
{" "}
{job.company}

</p>



<p className="text-gray-600">

Location:
{" "}
{job.location}

</p>




<p className="mt-2">

AI Match:

<span className="
ml-2
bg-green-100
text-green-700
px-3
py-1
rounded-full
">

{
(job.score * 100).toFixed(1)
}%

</span>

</p>




<a

href={job.link}

target="_blank"

className="
inline-block
mt-3
text-blue-600
font-semibold
"

>

View Job →

</a>



</div>


)

)

}


</div>


</div>

                </div>

            )}

        </DashboardLayout>

    );

}