import type { Job } from "../types/job";


type Props = {
    job: Job;
};


export default function JobCard({job}:Props){

    return (

        <div className="bg-white rounded-lg shadow p-5">


            <h2 className="text-xl font-bold">
                {job.title}
            </h2>


            <p className="mt-2">
                Company: {job.company}
            </p>


            <p>
                Location: {job.location}
            </p>


            <p>
                AI Score:
                {" "}
                {(job.score * 100).toFixed(1)}%
            </p>


            <a
                href={job.link}
                target="_blank"
                className="inline-block mt-4 text-blue-600"
            >

                View Job

            </a>


        </div>

    );

}