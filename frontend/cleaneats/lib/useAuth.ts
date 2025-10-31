import { AuthContext } from "@/components/auth/AuthProvider"
import { useContext } from "react"

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error("User is not currently logged in")
    }
    return context;
}