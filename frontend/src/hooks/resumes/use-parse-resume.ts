import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";

import { parseResume } from "@/services/resume/resume.service";


export const useParseResume = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: parseResume,

    onSuccess: (_, resumeId) => {
      queryClient.invalidateQueries({
        queryKey: ["parsed-resume", resumeId],
      });
    },

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    onError: (error: any) => {
      toast.error(
        error.response?.data?.detail || "Failed to parse resume"
      );
    },
  });
};