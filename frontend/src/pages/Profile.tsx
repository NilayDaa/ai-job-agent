import { useEffect, useState } from "react";

import api from "../api/api";

import DashboardLayout from "../layouts/DashboardLayout";

import { useAuth } from "../hooks/useAuth";


export default function Profile(){

    const [cv,setCv] = useState<any>(null);

    const [loading,setLoading] = useState(true);

    const { logout } = useAuth();



    async function getCV(){

        try{

            const response =
                await api.get("/my-cv");


            setCv(response.data);

        }
        catch(error){

            console.log(error);

        }
        finally{

            setLoading(false);

        }

    }



    useEffect(()=>{

        getCV();

    },[]);



    return (

        <DashboardLayout>


            <h1 className="text-3xl font-bold mb-6">
                Profile
            </h1>



            <div className="bg-white rounded shadow p-6">


                <h2 className="text-xl font-bold">
                    Account
                </h2>


                <p className="mt-3">
                    AI Job Agent User
                </p>


            </div>





            <div className="bg-white rounded shadow p-6 mt-6">


                <h2 className="text-xl font-bold">
                    CV Status
                </h2>



                {
                    loading &&

                    <p>
                        Loading...
                    </p>
                }




                {
                    !loading && cv?.message &&

                    <p className="mt-3 text-red-500">

                        No CV uploaded yet

                    </p>

                }





                {
                    !loading && cv?.filename &&

                    <div className="mt-3">


                        <p>
                            Uploaded file:
                            {" "}
                            {cv.filename}
                        </p>


                        <p className="text-green-600">

                            CV Ready for AI Analysis

                        </p>


                    </div>

                }


            </div>





            <button

                onClick={logout}

                className="mt-6 bg-red-600 text-white px-6 py-2 rounded"

            >

                Logout

            </button>



        </DashboardLayout>

    );

}