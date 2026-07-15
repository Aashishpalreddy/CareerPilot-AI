"use client";

import { useRouter } from "next/navigation";

import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

import { useLogin } from "@/hooks/auth/use-login";


const schema = z.object({
  email: z
    .string()
    .email("Enter a valid email"),

  password: z
    .string()
    .min(6, "Password must be at least 6 characters"),
});


type LoginFormData = z.infer<typeof schema>;



export default function LoginForm() {

  const router = useRouter();

  const loginMutation = useLogin();


  const {
    register,
    handleSubmit,
    formState:{
      errors,
    },
  } = useForm<LoginFormData>({

    resolver: zodResolver(schema),

    defaultValues:{
      email:"",
      password:"",
    }

  });



  async function onSubmit(
    data: LoginFormData
  ){

    try{

      await loginMutation.mutateAsync(data);


      router.push("/dashboard");


    }
    catch(error: any){

  console.error(
    "LOGIN FAILED",
    error
  );

  console.log(
    "STATUS:",
    error?.response?.status
  );

  console.log(
    "DATA:",
    error?.response?.data
  );

  alert(
    JSON.stringify(
      error?.response?.data || error.message
    )
  );

}

  }



  return (

    <Card>

      <CardHeader>

        <CardTitle className="text-2xl">
          Sign In
        </CardTitle>

      </CardHeader>


      <CardContent>


        <form
          onSubmit={
            handleSubmit(onSubmit)
          }

          className="space-y-5"
        >


          <div className="space-y-2">

            <Label>
              Email
            </Label>


            <Input

              type="email"

              placeholder="aashish@example.com"

              {...register("email")}

            />


            {
              errors.email && (

                <p className="text-sm text-red-500">

                  {errors.email.message}

                </p>

              )
            }


          </div>




          <div className="space-y-2">

            <Label>
              Password
            </Label>


            <Input

              type="password"

              placeholder="********"

              {...register("password")}

            />


            {
              errors.password && (

                <p className="text-sm text-red-500">

                  {errors.password.message}

                </p>

              )
            }


          </div>



          <Button

            type="submit"

            className="w-full"

            disabled={
              loginMutation.isPending
            }

          >

            {
              loginMutation.isPending
              ?
              "Signing in..."
              :
              "Sign In"
            }


          </Button>


        </form>


      </CardContent>


    </Card>

  );

}