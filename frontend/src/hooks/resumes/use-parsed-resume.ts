import { useQuery } from "@tanstack/react-query";

import { getParsedResume } from "@/services/resume/resume.service";


export const useParsedResume = (resumeId: number) => {
  return useQuery({
    queryKey: ["parsed-resume", resumeId],
    queryFn: () => getParsedResume(resumeId),
    enabled: !!resumeId,
  });
};