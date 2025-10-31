import React, { createContext, useContext, useState, ReactNode, useEffect } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { onAuthStateChanged, User } from "firebase/auth";
import { auth } from "@/firebaseConfig"; // adjust import path

type AppStateContextType = {
  user: User | null;
  loading: boolean;
  hasSeenOnboarding: boolean;
  setHasSeenOnboarding: (value: boolean) => Promise<void>;
};

const AppStateContext = createContext<AppStateContextType>({
  user: null,
  loading: true,
  hasSeenOnboarding: false,
  setHasSeenOnboarding: async () => {},
});

export const AppStateProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [hasSeenOnboarding, setHasSeenOnboardingState] = useState(false);

  useEffect(() => {
    const init = async () => {
      const onboarded = await AsyncStorage.getItem("hasSeenOnboarding");
      setHasSeenOnboardingState(onboarded === "true");
    };
    init();

    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user);
      setLoading(false);
    });

    return unsubscribe;
  }, []);

  const setHasSeenOnboarding = async (value: boolean) => {
    setHasSeenOnboardingState(value);
    await AsyncStorage.setItem("hasSeenOnboarding", value ? "true" : "false");
  };

  return (
    <AppStateContext.Provider value={{ user, loading, hasSeenOnboarding, setHasSeenOnboarding }}>
      {children}
    </AppStateContext.Provider>
  );
};

export const useAppState = () => useContext(AppStateContext);