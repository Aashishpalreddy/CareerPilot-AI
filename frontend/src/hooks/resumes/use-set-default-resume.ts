import { useMutation, useQueryClient } from "@tanstack/react-query";

import { setDefaultResume } from "@/services/resume/resume.service";


export const useSetDefaultResume = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: setDefaultResume,

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["resumes"],
      });
    },
  });
};