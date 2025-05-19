import React, { useEffect, useState } from "react";
import Login from "./Login";
import Operation from "./Operation";
import axios from "axios";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [authorized, setAuthorized] = useState(null); // null = unknown, true/false = checked

  useEffect(() => {
    const checkAuth = async () => {
      if (!token) {
        setAuthorized(false);
        return;
      }

      try {
        const res = await axios.post(
          "http://localhost:8080/operation",
          {}, // body
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        if (res.status === 200) {
          setAuthorized(true);
        } else {
          setAuthorized(false);
        }
      } catch (err) {
        console.error("Auth check failed:", err);
        setAuthorized(false);
      }
    };

    checkAuth();
  }, [token]);

  const handleLogin = (newToken) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
    setAuthorized(true);
  };

  return (
    <div>
      <h1>Simple Operation</h1>
      {authorized === null ? (
        <p>Loading...</p>
      ) : !authorized ? (
        <Login onLogin={handleLogin} />
      ) : (
        <Operation token={token} />
      )}
    </div>
  );
}

export default App;
