import React, { createContext, useContext, ReactNode } from 'react';

interface EnvContextType {
    baseUrl: string;
    maxFileLimit: number;
}

const EnvContext = createContext<EnvContextType | undefined>(undefined);

export const EnvProvider = ({ children }: { children: ReactNode }) => {
    const envValues: EnvContextType = {
        baseUrl: import.meta.env.VITE_API_URL || '',
        maxFileLimit: parseInt(import.meta.env.VITE_MAX_FILE_SIZE || '0', 10),
    };

    return (
        <EnvContext.Provider value={envValues}>
            {children}
        </EnvContext.Provider>
    );
};

export const useEnv = (): EnvContextType => {
    const context = useContext(EnvContext);
    if (!context) {
        throw new Error('useEnv must be used within an EnvProvider');
    }
    return context;
};
