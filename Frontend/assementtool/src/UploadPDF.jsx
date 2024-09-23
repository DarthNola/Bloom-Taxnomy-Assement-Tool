import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

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
    <div className="h-screen flex items-center justify-center flex-col bg-gray-900">
        <h1 className="text-6xl text-cyan-600 text-center mb-4">Bloom Assessment Tool Checker</h1>
      <div className="border border-gray-900 rounded-lg p-6 bg-gray-50 shadow-lg w-1/4 bg-slate-800">
        <h2 className="text-cyan-600 text-center text-2xl mb-4">Upload PDF</h2>
        <form onSubmit={handleSubmit} className="flex flex-col">
          <label className="custom-file-upload border border-gray-300 rounded-md bg-white p-2 text-center cursor-pointer hover:bg-gray-200 transition duration-300 mb-2">
            <input type="file" accept="application/pdf" onChange={handleFileChange} className="hidden" />
            Choose File
          </label>
          <button type="submit" disabled={loading} className="bg-cyan-400 text-neutral-50 py-2 rounded-md hover:bg-cyan-500 transition duration-300">
            Upload
          </button>
        </form>

        {loading && (
          <div className="flex justify-center items-center h-6 p-6">
            <div className="border-4 border-gray-200 border-l-blue-500 rounded-full w-10 h-10 animate-spin"></div>
          </div>
        )}

        {errorMessage && <p className="text-red-500 text-center">{errorMessage}</p>}
      </div>
    </div>
  );
};

export default UploadPDF;
