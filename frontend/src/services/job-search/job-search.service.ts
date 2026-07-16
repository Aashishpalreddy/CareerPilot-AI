import { api } from "@/services/api";
import type { JobSearchRequest, JobSearchResponse } from "@/types/job";

export const jobSearchService = {
  async search(data: JobSearchRequest): Promise<JobSearchResponse> {
    const response = await api.post<JobSearchResponse>("/job-search/", data);
    return response.data;
  },
};
