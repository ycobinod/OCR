import React, { useState } from 'react';
import axios from 'axios';
import './FileUpload.css'

const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');

    const onFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const onFileUpload = async () => {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://127.0.0.1:8000/pdf/upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                responseType: 'blob' 
            });

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', file.name); // Set the file name
            document.body.appendChild(link);
            link.click();
            setMessage('File processed and downloaded successfully');
        } catch (error) {
            console.error('There was an error uploading the file!', error);
            setMessage('Error uploading file');
        }
    };

    return (
        <div className="upload-container">
      <h2>Upload PDF</h2>
      <input type="file" onChange={onFileChange} />
      <button onClick={onFileUpload}>Upload</button>
      {message && <p>{message}</p>}
    </div>
    );
};

export default FileUpload;