import { useState } from "react";

import api from "../api/api";

import { useAuth } from "../hooks/useAuth";



export default function Login(){


    const [email,setEmail] = useState("");

    const [password,setPassword] = useState("");

    const [error,setError] = useState("");

    const {login} = useAuth();



    async function handleLogin(){


        try{


            setError("");

            const response = await api.post(
                "/login",
                {
                    email,
                    password
                }
            );


            login(
                response.data.access_token
            );


            window.location.href="/dashboard";


        }
        catch(error){

            console.log(error);

            setError(
                "Invalid email or password"
            );

        }


    }



    return (

<div className="
min-h-screen
bg-gray-100
flex
items-center
justify-center
">


<div className="
bg-white
w-full
max-w-md
p-8
rounded-2xl
shadow-xl
">


<h1 className="
text-3xl
font-bold
text-center
text-blue-600
">

AI Job Agent

</h1>



<p className="
text-center
text-gray-500
mt-2
mb-8
">

Login to find your AI matched jobs

</p>





{
error &&

<div className="
bg-red-100
text-red-600
p-3
rounded
mb-4
">

{error}

</div>

}





<label className="block mb-2">

Email

</label>


<input

className="
w-full
border
rounded-lg
p-3
mb-5
focus:outline-none
focus:ring-2
focus:ring-blue-500
"

placeholder="email@example.com"

value={email}

onChange={
e=>setEmail(e.target.value)
}

/>





<label className="block mb-2">

Password

</label>



<input

className="
w-full
border
rounded-lg
p-3
mb-6
focus:outline-none
focus:ring-2
focus:ring-blue-500
"

type="password"

placeholder="********"

value={password}

onChange={
e=>setPassword(e.target.value)
}

/>





<button

onClick={handleLogin}

className="
w-full
bg-blue-600
text-white
py-3
rounded-lg
font-semibold
hover:bg-blue-700
transition
"

>

Login

</button>



<p className="
text-center
text-sm
text-gray-500
mt-6
">

AI powered career assistant

</p>



</div>


</div>

    );

}