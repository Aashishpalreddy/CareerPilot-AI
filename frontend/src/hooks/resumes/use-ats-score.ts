import { useMutation, useQueryClient } from "@tanstack/react-query";

import { getATSScore } from "@/services/resume/resume.service";


export const useATSScore = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: getATSScore,

    onSuccess: (_, resumeId) => {
      queryClient.invalidateQueries({
        queryKey: ["ats-score", resumeId],
      });
    },
  });
};