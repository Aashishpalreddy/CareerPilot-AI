import { useQuery } from "@tanstack/react-query";

import { getResumes } from "@/services/resume/resume.service";


export const useResumes = () => {
  return useQuery({
    queryKey: ["resumes"],
    queryFn: getResumes,
  });
};