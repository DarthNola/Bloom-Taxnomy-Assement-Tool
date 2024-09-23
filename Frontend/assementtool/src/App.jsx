import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import UploadPDF from './UploadPDF';
import Dashboard from './Dashboard';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<UploadPDF />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
};

export default App;
