import React, { useState } from "react";
import axios from "axios";

const Login = ({ onLogin }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    
    try {
      
      const res = await axios.post(
        "http://localhost:8080/login",
        {},
        {
          auth: {
            username: email,
            password: password,
          },
        }
      );

      const token = res.data.token;
      onLogin(token);
    } catch (err) {
      alert("Login failed");
      console.error(err.response?.data || err.message);
    }
  };

  return (
    <form onSubmit={submit}>
      <input
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      /><br/>
      <input
        placeholder="Password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      /><br/>
      <button type="submit">Login</button>
    </form>
  );
};

export default Login;