import { useMutation } from "@tanstack/react-query";
import { authService } from "@/services/auth/auth.service";
import type { RegisterRequest } from "@/types/auth";
import { useAuth } from "@/context/auth-context";

export function useRegister() {
  const { login } = useAuth();

  return useMutation({
    mutationFn: async (data: RegisterRequest) => {
      await authService.register(data);
      // Auto-login after successful registration
      await login(data.email, data.password);
    },
  });
}
