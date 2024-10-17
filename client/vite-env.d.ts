/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_API_URL: string;
    readonly VITE_MAX_FILE_SIZE: string;
    readonly VITE_HOST: string;
    readonly VITE_PORT: string;
}

interface ImportMeta {
    readonly env: ImportMetaEnv;
}
