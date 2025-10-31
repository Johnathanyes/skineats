import { DarkTheme, DefaultTheme, ThemeProvider } from "@react-navigation/native";
import { Stack } from "expo-router";
import { StatusBar } from "expo-status-bar";
import "react-native-reanimated";

import { useColorScheme } from "@/hooks/use-color-scheme";
import { AppStateProvider, useAppState } from "@/components/context/AppStateContext";

export const unstable_settings = {
  anchor: "(tabs)",
};

function RootNavigator() {
  const { user, loading, hasSeenOnboarding } = useAppState();

  if (loading) return null;

  // Navigation flow:
  // 1. Onboarding first time
  if (!hasSeenOnboarding) {
    return (
      <Stack>
        <Stack.Screen name="onboarding/index" options={{ headerShown: false }} />
      </Stack>
    );
  }

  // 2. Auth flow if not logged in
  if (!user) {
    return (
      <Stack>
        <Stack.Screen name="(auth)/login" options={{ headerShown: false }} />
      </Stack>
    );
  }

  // 3. Main app (tabs)
  return (
    <Stack>
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
      <Stack.Screen name="modal" options={{ presentation: "modal" }} />
    </Stack>
  );
}

export default function RootLayout() {
  const colorScheme = useColorScheme();

  return (
    <ThemeProvider value={colorScheme === "dark" ? DarkTheme : DefaultTheme}>
      <AppStateProvider>
        <RootNavigator />
        <StatusBar style="auto" />
      </AppStateProvider>
    </ThemeProvider>
  );
}