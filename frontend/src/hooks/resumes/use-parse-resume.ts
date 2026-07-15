import { useMutation, useQueryClient } from "@tanstack/react-query";

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
  });
};