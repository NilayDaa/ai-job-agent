import { useAuth } from "../hooks/useAuth";


export default function Navbar(){

    const {logout}=useAuth();


    return (

        <header className="
            h-16
            bg-white
            border-b
            flex
            items-center
            justify-between
            px-8
        ">

            <div>

                <h1 className="
                    text-2xl
                    font-bold
                    text-blue-600
                ">
                    AI Job Agent
                </h1>

                <p className="text-sm text-gray-500">
                    Smart career assistant
                </p>

            </div>



            <button

                onClick={logout}

                className="
                bg-red-500
                text-white
                px-5
                py-2
                rounded-lg
                hover:bg-red-600
                "

            >

                Logout

            </button>


        </header>

    );

}