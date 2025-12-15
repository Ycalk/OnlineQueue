interface TokenResponse {
  access_token: string;
  token_type: string;
}

interface ErrorResponse {
  error: string;
  message: string;
}

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

export class ApiClient {
  private baseUrl: string;
  private accessToken: string | null = null;
  private isRefreshing: boolean = false;
  private refreshSubscribers: ((token: string) => void)[] = [];
  // Слушатели изменения статуса авторизации (вход/выход)
  private authListeners: (() => void)[] = [];

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
    this.accessToken = localStorage.getItem('access_token');
  }

  // --- Методы управления токеном ---

  public setToken(token: string) {
    this.accessToken = token;
    localStorage.setItem('access_token', token);
    this.notifyAuthChange(); // Уведомляем подписчиков о входе
  }

  public clearToken() {
    this.accessToken = null;
    localStorage.removeItem('access_token');
    this.notifyAuthChange(); // Уведомляем подписчиков о выходе
  }

  // --- Методы Event Bus (подписка на изменения авторизации) ---

  /**
   * Подписаться на изменения состояния авторизации.
   * Возвращает функцию для отписки.
   */
  public onAuthChange(listener: () => void): () => void {
    this.authListeners.push(listener);
    return () => {
      this.authListeners = this.authListeners.filter(l => l !== listener);
    };
  }

  private notifyAuthChange() {
    this.authListeners.forEach(listener => listener());
  }

  // --- Основной метод запроса ---

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

      if (response.status === 401) {
        const isRefreshEndpoint = endpoint === '/api/v1/auth/token';
        const isLoginEndpoint = endpoint === '/api/v1/auth/login';

        if (!isRefreshEndpoint && !isLoginEndpoint) {
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

export const api = new ApiClient('https://online-queue.ycalk.tech');
