import React from "react";
import { Outlet, Link } from "react-router-dom";
import './Layout.css';
export default function Layout() {
	return (
		<>
			<nav>
                <ul>
                    <li>
                        <Link to="/">Home</Link>
                    </li>
                    <li>
                        <Link to="/login">Login</Link>
                    </li>
                    <li>
                        <Link to="/register">Register</Link>
                    </li>
                </ul>
            </nav>
            <Outlet/>
		</>
	);
}