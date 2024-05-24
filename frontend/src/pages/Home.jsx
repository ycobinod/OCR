import React from 'react'
import { useState, useEffect } from 'react'
import axios from "axios"
import {  Link } from "react-router-dom";
import './Home.css'

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
  
    
  
  return (
    <div className="div-container">
      {isLoggedIn ? (
        <>
          <h2>Hi, {username}. Welcome to OCR</h2>
          <button><Link to="fileupload">FileUpload</Link></button>
          <button ><Link to ="search"> Search</Link></button>
          <button onClick={handleLogout}>Logout</button>
        </>
      ) : (
        <h2>Please Login first</h2>
      )}
    </div>
    
  )
}