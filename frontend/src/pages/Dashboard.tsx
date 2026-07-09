import DashboardLayout from "../layouts/DashboardLayout";


export default function Dashboard(){


return (

<DashboardLayout>


<h1 className="
text-4xl
font-bold
mb-8
">

Dashboard

</h1>



<div className="
grid
grid-cols-1
md:grid-cols-3
gap-6
">


<Card
title="Jobs Found"
value="120"
/>


<Card
title="CV Status"
value="Uploaded"
/>


<Card
title="AI Match"
value="85%"
/>


</div>




<div className="
mt-10
bg-white
rounded-xl
shadow
p-8
">


<h2 className="
text-2xl
font-bold
">

AI Career Assistant

</h2>


<p className="
mt-3
text-gray-600
">

Upload your CV and let AI find matching jobs and improve your career path.

</p>


</div>



</DashboardLayout>

);

}



function Card({
title,
value
}:{
title:string,
value:string
}){


return (

<div className="
bg-white
rounded-xl
shadow
p-6
">


<p className="
text-gray-500
">

{title}

</p>


<h2 className="
text-4xl
font-bold
mt-3
">

{value}

</h2>


</div>

);


}