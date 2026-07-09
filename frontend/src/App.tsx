import {
    BrowserRouter,
    Routes,
    Route
}
from "react-router-dom";


import Login from "./pages/Login";

import Dashboard from "./pages/Dashboard";

import Jobs from "./pages/Jobs";

import UploadCV from "./pages/UploadCV";

import Profile from "./pages/Profile";

import { Navigate } from "react-router-dom";

import ProtectedRoute
from "./components/ProtectedRoute";



export default function App(){


return (

<BrowserRouter>


<Routes>


<Route
path="/"
element={<Login />}
/>


<Route
path="/login"
element={<Login />}
/>



<Route
path="/dashboard"
element={

<ProtectedRoute>

<Dashboard />

</ProtectedRoute>

}

/>

<Route
    path="*"
    element={
        <Navigate to="/dashboard" />
    }
/>


<Route
path="/jobs"
element={
<ProtectedRoute>
<Jobs/>
</ProtectedRoute>
}
/>

<Route
    path="/profile"
    element={
        <ProtectedRoute>
            <Profile />
        </ProtectedRoute>
    }
/>


<Route
path="/upload"
element={
<ProtectedRoute>
<UploadCV/>
</ProtectedRoute>
}
/>


</Routes>


</BrowserRouter>

);


}