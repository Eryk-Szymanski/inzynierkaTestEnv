import { StyleSheet } from "react-native";
import { Dimensions } from "react-native";

const windowHeight = Dimensions.get("window").height;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#222222",
    justifyContent: "center",
  },
  cardContainer: {
    height: windowHeight,
    justifyContent: "center",
    alignItems: "center",
  },
  card: {
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 2,
    borderColor: "#444444",
    borderRadius: 10,
    paddingHorizontal: 45,
    paddingVertical: 30,
    backgroundColor: "#333333",
  },
  header: {
    fontSize: 30,
    padding: 5,
    color: "#ffffff",
  },
  input: {
    backgroundColor: "#222222",
    borderRadius: 20,
    margin: 5,
    paddingHorizontal: 20,
    paddingVertical: 10,
    color: "#ffffff",
  },
  button: {
    borderColor: "#ffffff",
    borderWidth: 3,
    borderRadius: 20,
    backgroundColor: "#111111",
    paddingHorizontal: 30,
    paddingVertical: 10,
    margin: 15,
  },
});

export { styles };
