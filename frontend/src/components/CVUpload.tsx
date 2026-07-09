import { useState } from "react";

import api from "../api/api";

import DashboardLayout from "../layouts/DashboardLayout";


export default function UploadCV(){

    const [file,setFile] = useState<File | null>(null);

    const [result,setResult] = useState<any>(null);

    const [loading,setLoading] = useState(false);



    async function uploadCV(){


        if(!file){
            return;
        }


        try{

            setLoading(true);


            const formData = new FormData();

            formData.append(
                "file",
                file
            );


            const response =
                await api.post(
                    "/match-cv",
                    formData,
                    {
                        headers:{
                            "Content-Type":
                            "multipart/form-data"
                        }
                    }
                );


            setResult(response.data);


        }
        catch(error){

            console.log(error);

        }
        finally{

            setLoading(false);

        }


    }



    return (

        <DashboardLayout>


            <h1 className="text-3xl font-bold mb-6">
                Upload CV
            </h1>



            <div className="bg-white p-6 rounded shadow">


                <input

                    type="file"

                    accept=".pdf"

                    onChange={
                        e=>setFile(
                            e.target.files?.[0] || null
                        )
                    }

                />



                <button

                    onClick={uploadCV}

                    className="mt-5 bg-blue-600 text-white px-6 py-2 rounded"

                >

                    Analyze CV

                </button>


            </div>




            {
                loading &&

                <p className="mt-5">
                    AI is analyzing your CV...
                </p>
            }





            {
                result &&

                <div className="mt-8 space-y-5">


                    <div className="bg-white p-6 rounded shadow">

                        <h2 className="text-xl font-bold">

                            CV Summary

                        </h2>


                        <p>
                            Characters:
                            {" "}
                            {
                            result.cv_summary.characters
                            }
                        </p>


                        <p>
                            Skills:
                            {" "}
                            {
                            result.cv_summary.skills_found.join(", ")
                            }
                        </p>


                    </div>





                    <div className="bg-white p-6 rounded shadow">


                        <h2 className="text-xl font-bold">

                            AI Career Analysis

                        </h2>


                        <p className="text-3xl">

                            {
                            result.career_analysis.overall_match
                            }%

                        </p>


                        <h3 className="font-bold mt-4">
                            Strengths
                        </h3>


                        <ul>

                        {
                        result.career_analysis.strengths.map(
                            (item:string)=>(

                                <li key={item}>
                                    {item}
                                </li>

                            )
                        )
                        }

                        </ul>



                        <h3 className="font-bold mt-4">
                            Missing Skills
                        </h3>


                        <ul>

                        {
                        result.career_analysis.missing_skills.map(
                            (item:string)=>(

                                <li key={item}>
                                    {item}
                                </li>

                            )
                        )
                        }

                        </ul>


                    </div>


                </div>

            }


        </DashboardLayout>

    );

}