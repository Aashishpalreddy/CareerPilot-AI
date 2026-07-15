import { useMutation } from "@tanstack/react-query";
import { useAuth } from "@/context/auth-context";

export function useLogin() {
  const { login } = useAuth();

  return useMutation({
    mutationFn: async ({
      email,
      password,
    }: {
      email: string;
      password: string;
    }) => {
      await login(email, password);
    },
  });
}