import React from 'react';
import { useLocation } from 'react-router-dom';

const Dashboard = () => {
  // Get the passed data from the navigation state
  const location = useLocation();
  const { data } = location.state || {};

  return (
    <div>
      <h2>Dashboard</h2>
      {data ? (
        <pre>{JSON.stringify(data, null, 2)}</pre> // Display the API response data
      ) : (
        <p>No data available</p>
      )}
    </div>
  );
};

export default Dashboard;
