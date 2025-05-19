import React, { useEffect, useState } from "react";
import axios from "axios";

const Operation = ({ token }) => {
  const [message, setMessage] = useState("");

  useEffect(() => {
    axios
      .post(
        "http://localhost:8080/operation",
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )
      .then((res) => {
        setMessage("Authorized operation: Success");
      })
      .catch((err) => {
        setMessage("Operation failed: " + (err.response?.data || err.message));
      });
  }, [token]);

  return <p>{message}</p>;
};

export default Operation;