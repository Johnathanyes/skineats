import { View, Text, Button } from "react-native";
import { useAppState } from "@/components/context/AppStateContext";

export default function OnboardingScreen() {
  const { setHasSeenOnboarding } = useAppState();

  return (
    <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
      <Text style={{ fontSize: 24, marginBottom: 20 }}>Welcome to MyApp 🎉</Text>
      <Button title="Get Started" onPress={() => setHasSeenOnboarding(true)} />
    </View>
  );
}