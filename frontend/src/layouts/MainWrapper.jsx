import { useEffect, useState } from 'react';
import { setUser } from '../utils/auth';

const MainWrapper = ({ children }) => {
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const handler = async () => {
            setLoading(true);
            try {
                await setUser();
            } catch (error) {
                console.error("Error setting user:", error);
            }
            setLoading(false);
        };
        handler();
    }, []);

    return loading ? null : children; // Render children only when loading is false
};

export default MainWrapper;
