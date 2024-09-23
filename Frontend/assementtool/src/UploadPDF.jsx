import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Upload.css'; // Import the CSS file

const UploadPDF = () => {
  const [file, setFile] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!file) {
      setErrorMessage('Please select a file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      setLoading(true);

      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const responseData = response.data;
      navigate('/dashboard', { state: { data: responseData } });
      
    } catch (error) {
      console.error('Error uploading file:', error);
      setErrorMessage('Error uploading file. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <h1>Bloom Assessment Tool Checker</h1>
      <div className='container'>
        <div className='upload-card'>
          <h2>Upload PDF</h2>
          <form onSubmit={handleSubmit}>
            <label className="custom-file-upload">
              <input type="file" accept="application/pdf" onChange={handleFileChange} />
              Choose File
            </label>
            <button type="submit" disabled={loading}>Upload</button>
          </form>

          {loading && (
            <div className="spinner-container">
              <div className="spinner"></div>
            </div>
          )}

          {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
        </div>
      </div>
    </>
  );
};

export default UploadPDF;
