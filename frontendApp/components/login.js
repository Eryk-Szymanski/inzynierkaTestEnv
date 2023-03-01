import React, { useState } from "react";
import { StyleSheet, Text, View, Pressable, TextInput } from "react-native";
import { styles } from "../style/mainStyle";

const LoginScreen = ({ navigation }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  return (
    <View style={styles.cardContainer}>
      <View style={styles.card}>
        <Text style={styles.header}>Sign In</Text>
        <TextInput
          style={styles.input}
          onChangeText={(value) => setEmail(value)}
          placeholder="Email"
        ></TextInput>
        <TextInput
          style={styles.input}
          onChangeText={(value) => setPassword(value)}
          placeholder="Password"
          secureTextEntry={true}
        ></TextInput>
        <Pressable style={styles.button} onPress={() => console.log("lol")}>
          <Text style={{ color: "#ffffff" }}>Submit</Text>
        </Pressable>
        <Pressable onPress={() => navigation.navigate("Register")}>
          <Text style={{ color: "#292cff" }}>
            Don't have an account? Sign Up
          </Text>
        </Pressable>
      </View>
    </View>
  );
};

export default LoginScreen;
