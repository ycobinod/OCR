import './App.css'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home"
import Layout from './pages/Layout';
import Register from './pages/Register';
import Login from './pages/Login'
import FileUpload from './pages/FileUpload';
function App() {

  return (
   <BrowserRouter>
   <Routes>
    <Route path='/' element={<Layout/>}>
    <Route index element={<Home/>}/>
    <Route path="register" element={<Register/>}/>
    <Route path="login" element={<Login/>}/>
    <Route path="fileupload" element={<FileUpload/>}/>

    </Route>
   </Routes>
   
   </BrowserRouter> 
  )
}

export default App