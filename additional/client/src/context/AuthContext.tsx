import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { api, UserProfile } from '../api/ApiClient';

interface AuthContextType {
    user: UserProfile | null;
    isLoading: boolean;
    setUser: (user: UserProfile | null) => void;
    refreshUser: () => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<UserProfile | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    const refreshUser = async () => {
        try {
            if (!localStorage.getItem('access_token')) {
                setUser(null);
                return;
            }
            const userData = await api.getUser();
            setUser(userData);
        } catch (e) {
            console.error('Failed to fetch user', e);
            setUser(null);
        } finally {
            setIsLoading(false);
        }
    };

    const logout = () => {
        api.clearToken();
        setUser(null);
    };

    useEffect(() => {
        refreshUser();
    }, []);

    return (
        <AuthContext.Provider value={{ user, isLoading, setUser, refreshUser, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
