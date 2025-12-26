interface TokenResponse {
    access_token: string;
    token_type: string;
}

interface ErrorResponse {
    error: string;
    message: string;
}

export interface UserProfile {
    email: string;
    first_name: string;
    last_name: string;
    patronymic: string;
}

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

export class ApiClient {
    private baseUrl: string;
    private accessToken: string | null = null;
    private isRefreshing: boolean = false;
    private refreshSubscribers: ((token: string) => void)[] = [];

    private userProfile: UserProfile | null = null;

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
        this.accessToken = localStorage.getItem('access_token');
    }

    public setToken(token: string) {
        this.accessToken = token;
        localStorage.setItem('access_token', token);
        this.userProfile = null;
    }

    public clearToken() {
        this.accessToken = null;
        localStorage.removeItem('access_token');
        this.userProfile = null;
    }

    public async getUser(): Promise<UserProfile | null> {
        if (this.userProfile) {
            return this.userProfile;
        }

        if (!this.accessToken) {
            return null;
        }

        try {
            const user = await this.request<UserProfile>('/api/v1/users/me');
            this.userProfile = user;
            return user;
        } catch (error) {
            console.error("Failed to fetch user, logging out", error);
            this.clearToken();
            return null;
        }
    }

    public async request<T>(endpoint: string, method: HttpMethod = 'GET', body?: any): Promise<T> {
        const url = `${this.baseUrl}${endpoint}`;

        const headers: HeadersInit = {
            'Content-Type': 'application/json',
        };

        if (this.accessToken) {
            headers['Authorization'] = `Bearer ${this.accessToken}`;
        }

        const config: RequestInit = {
            method,
            headers,
            credentials: 'include',
        };

        if (body) {
            config.body = JSON.stringify(body);
        }

        try {
            let response = await fetch(url, config);

            if (response.status === 401 || response.status === 403) {
                const isRefreshEndpoint = endpoint === '/api/v1/auth/token';

                if (!isRefreshEndpoint) {
                    try {
                        const newToken = await this.refreshAccessToken();

                        if (config.headers) {
                            (config.headers as Record<string, string>)['Authorization'] = `Bearer ${newToken}`;
                        }

                        response = await fetch(url, config);
                    } catch (refreshError) {
                        this.handleAuthError();
                        throw refreshError;
                    }
                }
            }

            if (!response.ok) {
                const errorData: ErrorResponse = await response.json().catch(() => ({}));
                throw new Error(errorData.message || `API Error: ${response.status}`);
            }

            return response.json();
        } catch (error) {
            throw error;
        }
    }

    private async refreshAccessToken(): Promise<string> {
        if (this.isRefreshing) {
            return new Promise((resolve) => {
                this.refreshSubscribers.push(resolve);
            });
        }

        this.isRefreshing = true;

        try {
            const response = await this.request<TokenResponse>('/api/v1/auth/token', 'POST');

            const newToken = response.access_token;
            this.setToken(newToken);

            this.refreshSubscribers.forEach((callback) => callback(newToken));
            this.refreshSubscribers = [];

            return newToken;
        } catch (error) {
            this.clearToken();
            throw error;
        } finally {
            this.isRefreshing = false;
        }
    }

    private handleAuthError() {
        this.clearToken();
        if (window.location.pathname !== '/' && window.location.pathname !== '/authorization') {
            window.location.href = '/';
        }
    }
}

export const api = new ApiClient('');
