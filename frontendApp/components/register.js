import React, { useState } from "react";
import { StyleSheet, Text, View, Pressable, TextInput } from "react-native";
import { styles } from "../style/mainStyle";

const RegisterScreen = ({ navigation }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [conPassword, setConPassword] = useState("");

  return (
    <View style={styles.cardContainer}>
      <View style={styles.card}>
        <Text style={styles.header}>Sign Up</Text>
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
        <TextInput
          style={styles.input}
          onChangeText={(value) => {
            if (value == password) console.log("passwords match");
            setConPassword(value);
          }}
          placeholder="Confirm Password"
          secureTextEntry={true}
        ></TextInput>
        <Pressable style={styles.button} onPress={() => console.log("lol")}>
          <Text style={{ color: "#ffffff" }}>Submit</Text>
        </Pressable>
        <Pressable onPress={() => navigation.navigate("Login")}>
          <Text style={{ color: "#292cff" }}>
            Already have an account? Sign In
          </Text>
        </Pressable>
      </View>
    </View>
  );
};

export default RegisterScreen;
