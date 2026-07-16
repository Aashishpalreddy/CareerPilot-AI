import { api } from "@/services/api";
import type {
  Job,
  JobCreateRequest,
  ParsedJob,
  MatchResponse,
  TailorResponse,
  ATSScoreResponse,
  KeywordGapResponse,
} from "@/types/job";

export const jobService = {
  async list(): Promise<Job[]> {
    const response = await api.get<Job[]>("/jobs");
    return response.data;
  },

  async getById(id: number): Promise<Job> {
    const response = await api.get<Job>(`/jobs/${id}`);
    return response.data;
  },

  async create(data: JobCreateRequest): Promise<Job> {
    const response = await api.post<Job>("/jobs", data);
    return response.data;
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/jobs/${id}`);
  },

  async getParsed(jobId: number): Promise<ParsedJob> {
    const response = await api.get<ParsedJob>(`/jobs/parsed/${jobId}`);
    return response.data;
  },

  async match(resumeId: number, jobId: number): Promise<MatchResponse> {
    const response = await api.get<MatchResponse>(
      `/resume-match/${resumeId}/${jobId}`
    );
    return response.data;
  },

  async tailor(resumeId: number, jobId: number): Promise<TailorResponse> {
    const response = await api.post<TailorResponse>(
      `/resume-tailor/${resumeId}/${jobId}`
    );
    return response.data;
  },

  async getATSScore(resumeId: number): Promise<ATSScoreResponse> {
    const response = await api.get<ATSScoreResponse>(
      `/resumes/ats/${resumeId}`
    );
    return response.data;
  },

  async getKeywordGap(
    resumeId: number,
    jobId: number
  ): Promise<KeywordGapResponse> {
    const response = await api.get<KeywordGapResponse>(
      `/keyword-gap/${resumeId}/${jobId}`
    );
    return response.data;
  },
};
