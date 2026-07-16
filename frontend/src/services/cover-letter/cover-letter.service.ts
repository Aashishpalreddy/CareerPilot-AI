import { api } from "@/services/api";
import type { CoverLetterResponse } from "@/types/job";

export const coverLetterService = {
  async generate(resumeId: number, jobId: number): Promise<CoverLetterResponse> {
    const response = await api.post<CoverLetterResponse>(
      `/cover-letter/generate/${resumeId}/${jobId}`
    );
    return response.data;
  },
  
  // Note: Download uses standard browser navigation to the download URL
};
