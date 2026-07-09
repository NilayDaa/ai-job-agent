import type { ReactNode } from "react";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";


export default function DashboardLayout({
children
}:{
children:ReactNode
}){


return (

<div className="min-h-screen bg-gray-100">


<Navbar />


<div className="flex">


<Sidebar />


<main className="
flex-1
p-8
">

{children}

</main>


</div>


</div>

);

}