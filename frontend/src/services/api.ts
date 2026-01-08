import axios from 'axios';
import { LoginData, RegisterData, User, AIToolRequest, AIToolResponse, CreditTransaction } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

interface APIResponse {
  access_token: string
}

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth APIs
export const authAPI = {
  register: async (data: RegisterData) => {
    const response = await api.post('/auth/register', data);
    return response.data;
  },
  
  login: async (data: LoginData) => {
    const response = await api.post<APIResponse>('/auth/login', data);
    return response.data;
  },
  
  googleAuth: async (token: string) => {
    const response = await api.post<APIResponse>('/auth/google', { token });
    return response.data;
  },
};

// User APIs
export const userAPI = {
  getCurrentUser: async (): Promise<User> => {
    const response = await api.get<User>('/users/me');
    return response.data;
  },
};

// AI Tool APIs
export const aiAPI = {
  chat: async (input_text: string): Promise<AIToolResponse> => {
    const response = await api.post<AIToolResponse>('/ai/chat', { tool_name: 'chat', input_text });
    return response.data;
  },
  
  summarize: async (input_text: string): Promise<AIToolResponse> => {
    const response = await api.post<AIToolResponse>('/ai/summarize', { tool_name: 'summarizer', input_text });
    return response.data;
  },
  
  generate: async (input_text: string): Promise<AIToolResponse> => {
    const response = await api.post<AIToolResponse>('/ai/generate', { tool_name: 'generator', input_text });
    return response.data;
  },
  
  codeHelp: async (input_text: string): Promise<AIToolResponse> => {
    const response = await api.post<AIToolResponse>('/ai/code-help', { tool_name: 'code_helper', input_text });
    return response.data;
  },
  
  analyze: async (input_text: string): Promise<AIToolResponse> => {
    const response = await api.post<AIToolResponse>('/ai/analyze', { tool_name: 'analyzer', input_text });
    return response.data;
  },
};

// Credit APIs
export const creditAPI = {
  getBalance: async () => {
    const response = await api.get('/credits/balance');
    return response.data;
  },
  
  getTransactions: async (): Promise<CreditTransaction[]> => {
    const response = await api.get<CreditTransaction[]>('/credits/transactions');
    return response.data;
  },
};

export default api;