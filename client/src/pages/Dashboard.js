import React, { useEffect, useState } from "react";
import axios from "axios";

const Dashboard = () => {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const { data } = await axios.get(
          `${process.env.REACT_APP_API_BASE_URL}/profile`
        );
        console.log("Profile data:", data);
        setProfile(data);
      } catch (error) {
        console.error("Failed to fetch profile", error);
      }
    };

    fetchProfile();
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>
      {profile ? (
        <div>
          <p>Display Name: {profile.displayName}</p>
          <img src={profile.pictureUrl} alt="Profile" />
        </div>
      ) : (
        <p>Loading profile...</p>
      )}
    </div>
  );
};

export default Dashboard;
