import { Link } from "react-router-dom";


export default function Sidebar(){

return (

<aside className="
w-64
bg-slate-900
text-white
min-h-screen
p-6
">


<h2 className="
text-xl
font-bold
mb-8
">
Menu
</h2>



<nav className="space-y-3">


<Link
className="
block
p-3
rounded-lg
hover:bg-slate-700
"
to="/dashboard"
>
🏠 Dashboard
</Link>



<Link
className="
block
p-3
rounded-lg
hover:bg-slate-700
"
to="/jobs"
>
💼 Jobs
</Link>



<Link
className="
block
p-3
rounded-lg
hover:bg-slate-700
"
to="/upload"
>
📄 Upload CV
</Link>



<Link
className="
block
p-3
rounded-lg
hover:bg-slate-700
"
to="/profile"
>
👤 Profile
</Link>


</nav>


</aside>

);


}