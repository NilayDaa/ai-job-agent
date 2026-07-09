import { useState } from "react";

import api from "../api/api";

import JobCard from "../components/JobCard";

import DashboardLayout from "../layouts/DashboardLayout";

import type { Job } from "../types/job";


export default function Jobs(){


const [query,setQuery]=useState("");

const [jobs,setJobs]=useState<Job[]>([]);

const [loading,setLoading]=useState(false);



async function searchJobs(){


try{


setLoading(true);


const response =
await api.get(
    "/semantic-search",
    {
        params:{
            query,
            k:10
        }
    }
);


setJobs(response.data);


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

AI Job Search

</h1>



<div className="flex gap-3">


<input

className="border p-3 flex-1 rounded"

placeholder="Search jobs e.g. Python developer"

value={query}

onChange={
e=>setQuery(e.target.value)
}

/>



<button

onClick={searchJobs}

className="bg-blue-600 text-white px-6 rounded"

>

Search

</button>


</div>



{
loading &&

<p className="mt-5">
Searching AI jobs...
</p>
}



<div className="grid gap-5 mt-8">


{
jobs.map(job=>(

<JobCard

key={job.id}

job={job}

/>

))

}


</div>



</DashboardLayout>

);


}