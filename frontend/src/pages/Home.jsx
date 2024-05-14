import React from 'react'
import { useState, useEffect } from 'react'
import axios from "axios"
import { FaSearch } from 'react-icons/fa';
import { Document, Page } from 'react-pdf';

export default function Home() {
  
  const [username, setUsername] = useState("")
  const [isLoggedIn, setLoggedIn] = useState(false)
  
  useEffect (()=>{
    const checkLoggedInUser = async () =>{
      try{
        const token = localStorage.getItem("accessToken");
        if (token) {
          const config = {
            headers: {
              "Authorization":`Bearer ${token}`
            }
          };
          const response = await axios.get("http://127.0.0.1:8000/api/user/", config)
          setLoggedIn(true)
          setUsername(response.data.username)
        }
        else{
          setLoggedIn(false);
          setUsername("");
        }
      }
      catch(error){
        setLoggedIn(false);
        setUsername("");
      }
    };
    checkLoggedInUser()
  }, [])

  const handleLogout = async () => {
    try{
      const accessToken = localStorage.getItem("accessToken");
      const refreshToken = localStorage.getItem("refreshToken");

      if(accessToken && refreshToken) {
        const config = {
          headers: {
            "Authorization":`Bearer ${accessToken}`
          }
        };
        await axios.post("http://127.0.0.1:8000/api/logout/", {"refresh":refreshToken}, config)
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        setLoggedIn(false);
        setUsername("");
        console.log("Log out successful!")
      }
    }
    catch(error){
      console.error("Failed to logout", error.response?.data || error.message)
    }
  }
  
    const [numPages, setNumPages] = useState(null);
    const [pageNumber, setPageNumber] = useState(1);
    const [file, setFile] = useState(null);
  
    function onFileChange(event) {
      const uploadedFile = event.target.files[0];
      setFile(uploadedFile);
    }
  
    function onDocumentLoadSuccess({ numPages }) {
      setNumPages(numPages);
    }
  
  return (
    <div>
      
      {isLoggedIn ? (
        <>
        
      <h2>Hi, {username}. welcome to OCR</h2>
      <div>
      <div>
        <input type="file" onChange={onFileChange} accept=".pdf" />
      </div>
      {file && (
        <div>
          <Document file={file} onLoadSuccess={onDocumentLoadSuccess}>
            {[...Array(numPages).keys()].map((pageIndex) => (
              <Page key={`page_${pageIndex + 1}`} pageNumber={pageIndex + 1} />
            ))}
          </Document>
          <p>Page {pageNumber} of {numPages}</p>
        </div>
      )}
    </div>

      <button onClick={handleLogout}>Logout</button>
      </>
      ):(
      <h2>Please Login</h2>
    )}
    </div>
    
  )
}