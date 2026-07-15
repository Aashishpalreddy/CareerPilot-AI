"use client";

import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";

import type { User } from "@/types/auth";

import { authService } from "@/services/auth/auth.service";

import {
  getToken,
  setToken,
  removeToken,
} from "@/lib/auth";


interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (
    email: string,
    password: string
  ) => Promise<void>;
  logout: () => void;
}


const AuthContext = createContext<
  AuthContextType | undefined
>(undefined);


export function AuthProvider({
  children,
}: {
  children: React.ReactNode;
}) {

  const [user, setUser] = useState<User | null>(null);

  const [loading, setLoading] = useState(true);



  async function loadUser() {

    try {

      const currentUser =
        await authService.getMe();

      setUser(currentUser);

    } catch {

      removeToken();

      setUser(null);

    } finally {

      setLoading(false);

    }

  }



  useEffect(() => {

    const token = getToken();

    if (token) {
      loadUser();
    } 
    else {
      setLoading(false);
    }

  }, []);




  async function login(
    email: string,
    password: string
  ) {

    const response =
      await authService.login(
        email,
        password
      );


    setToken(
      response.access_token
    );


    await loadUser();

  }




  function logout() {

    removeToken();

    setUser(null);

  }



  return (

    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        logout,
      }}
    >

      {children}

    </AuthContext.Provider>

  );

}



export function useAuth() {

  const context =
    useContext(AuthContext);


  if (!context) {

    throw new Error(
      "useAuth must be inside AuthProvider"
    );

  }


  return context;

}