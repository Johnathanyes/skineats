import { AuthContext } from "@/components/auth/AuthProvider"
import { useContext } from "react"


export const Auth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error("User is not currently logged in")
    }
    return context;
}