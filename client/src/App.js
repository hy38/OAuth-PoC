import React from "react";
import Login from "./components/Login";
import Dashboard from "./pages/Dashboard";

function App() {
  return (
    <div>
      <h1>Welcome to my LINE OAuth 2.0 PoC App</h1>
      <Login />
      <Dashboard />
    </div>
  );
}

export default App;