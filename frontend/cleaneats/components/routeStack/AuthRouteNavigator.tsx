import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { useAuth } from "@/lib/useAuth";
import { AuthStack } from "./AuthStack";
import { AppStack } from "./AppStack";
import { ActivityIndicator, View } from "react-native";

const RootNavigator = () => {
  const { user, loading } = useAuth();

  if (loading) {
    // optional splash or loading indicator
    return (
      <View>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  return (
    <NavigationContainer>
      {user ? <AppStack /> : <AuthStack />}
    </NavigationContainer>
  );
};

export default RootNavigator;