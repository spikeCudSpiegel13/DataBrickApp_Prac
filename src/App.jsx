import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("Loading API…");

  useEffect(() => {
    axios
      .get("/api/health")
      .then((response) => setMessage(response.data.message))
      .catch(() => setMessage("Could not connect to the API"));
  }, []);

  return (
    <main>
      <h1>Practice Security Manager</h1>
      <p>Backend says: {message}</p>
    </main>
  );
}

export default App;