import { Navigate } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";

import type { ReactNode } from "react";


type Props = {

    children: ReactNode;

};



export default function ProtectedRoute({

    children

}:Props){


    const {token}=useAuth();



    if(!token){

        return (
            <Navigate
                to="/login"
                replace
            />
        );

    }



    return children;

}