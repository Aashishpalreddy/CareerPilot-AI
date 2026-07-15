import { api } from "@/services/api";
import type { LoginResponse, RegisterRequest, User } from "@/types/auth";

export const authService = {
  async login(
    email: string,
    password: string
  ): Promise<LoginResponse> {
    const body = new URLSearchParams();

    body.append("username", email);
    body.append("password", password);

    const response = await api.post<LoginResponse>(
      "/auth/login",
      body,
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      }
    );

    return response.data;
  },

  async register(
    data: RegisterRequest
  ): Promise<User> {
    const response = await api.post<User>(
      "/auth/register",
      data
    );

    return response.data;
  },

  async getMe(): Promise<User> {
    const response = await api.get<User>(
      "/users/me"
    );

    return response.data;
  },
};