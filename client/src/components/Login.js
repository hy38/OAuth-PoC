import React from "react";
import axios from "axios";

const Login = () => {
  const handleLogin = async () => {
    const { data } = await axios.get('/login');
    
    console.log("Redirecting to URL:", data.url);

    window.location.href = data.url; // Redirect to the LINE login page
  };

  return <button onClick={handleLogin}>Login with LINE</button>;
};

export default Login;
