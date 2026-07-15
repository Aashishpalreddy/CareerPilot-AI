export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: number;
  full_name: string;
  email: string;
  is_active: boolean;
}

export interface RegisterRequest {
  full_name: string;
  email: string;
  password: string;
}