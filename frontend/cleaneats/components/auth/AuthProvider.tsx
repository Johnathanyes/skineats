// AuthProvider.js
import React, { createContext, ReactNode, useEffect, useState } from "react";
import { User, onAuthStateChanged } from "firebase/auth";
import { auth } from "../../firebaseConfig";
import * as SecureStore from "expo-secure-store";

interface AuthContextType {
    user: User | null;
    loading: boolean;
  }
  
  interface AuthProviderProps {
    children: ReactNode;
  }
  
  // -----------------------------
  // Default context value
  // -----------------------------
  
  export const AuthContext = createContext<AuthContextType>({
    user: null,
    loading: true,
  });
  
  export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
  
    useEffect(() => {
      // Listen for Firebase auth state changes
      const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
        setUser(firebaseUser);
        setLoading(false);
  
        // Optionally store user ID securely
        if (firebaseUser) {
          await SecureStore.setItemAsync("lastUser", firebaseUser.uid);
        } else {
          await SecureStore.deleteItemAsync("lastUser");
        }
      });
  
      return unsubscribe;
    }, []);
  
    return (
      <AuthContext.Provider value={{ user, loading }}>
        {children}
      </AuthContext.Provider>
    );
  };


