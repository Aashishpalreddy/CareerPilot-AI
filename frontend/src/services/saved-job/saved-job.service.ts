import { api, API_BASE_URL } from "@/services/api";
import type { SavedJob } from "@/types/job";

export const savedJobService = {
  async list(): Promise<SavedJob[]> {
    const response = await api.get<SavedJob[]>("/apply/saved-jobs");
    return response.data;
  },

  async getById(id: number): Promise<SavedJob> {
    const response = await api.get<SavedJob>(`/apply/saved-jobs/${id}`);
    return response.data;
  },

  async markApplied(id: number): Promise<SavedJob> {
    const response = await api.post<SavedJob>(`/apply/saved-jobs/${id}/mark-applied`);
    return response.data;
  },

  async processJob(jobId: number): Promise<SavedJob> {
    const response = await api.post<SavedJob>(`/apply/process-job/${jobId}`);
    return response.data;
  },

  async dismiss(id: number): Promise<void> {
    await api.delete(`/apply/saved-jobs/${id}`);
  },

  async updateStatus(id: number, status: "saved" | "applied" | "dismissed"): Promise<SavedJob | void> {
    if (status === "applied") {
      return this.markApplied(id);
    }
    if (status === "dismissed") {
      return this.dismiss(id);
    }
    // For "saved" — no endpoint, just refetch
  },

  getDownloadResumeUrl(id: number): string {
    return `${API_BASE_URL}/apply/saved-jobs/${id}/download-resume`;
  },

  getDownloadCoverLetterUrl(id: number): string {
    return `${API_BASE_URL}/apply/saved-jobs/${id}/download-cover-letter`;
  },
};
