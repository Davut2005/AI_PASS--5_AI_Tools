export interface User {
  id: number;
  email: string;
  name: string;
  role: string;
  organization_id: number | null;
  credits: number;
  created_at: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  name: string;
  organization_name?: string;
}

export interface AIToolRequest {
  tool_name: string;
  input_text: string;
}

export interface AIToolResponse {
  output_text: string;
  credits_used: number;
  remaining_credits: number;
}

export interface CreditTransaction {
  id: number;
  amount: number;
  type: string;
  description: string;
  created_at: string;
}