"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { uploadResume } from "@/services/resume/resume.service";


export function useUploadResume() {

  const queryClient = useQueryClient();


  return useMutation({

    mutationFn: (file: File) => uploadResume(file),


    onSuccess: () => {

      queryClient.invalidateQueries({
        queryKey: ["resumes"],
      });

    },


    onError: (error) => {

      console.error("Resume upload failed:", error);

    },

  });

}