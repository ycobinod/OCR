import React from 'react'

const FileUpload = () => {
    return (
        <div>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleSubmit} disabled={!selectedFile || loading}>
                {loading ? 'Processing...' : 'Upload'}
            </button>
        </div>
    );
};

export default FileUpload