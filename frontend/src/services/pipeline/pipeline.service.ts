import { api } from "@/services/api";
import type { PipelineRunRequest, SavedJob } from "@/types/job";

export const pipelineService = {
  async runDailyPipeline(data: PipelineRunRequest): Promise<SavedJob[]> {
    const response = await api.post<SavedJob[]>("/apply/run", data);
    return response.data;
  },
};
