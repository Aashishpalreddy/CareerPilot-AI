import { api } from "@/services/api";
import type { Resume } from "@/types/resume";


// Get all resumes
export const getResumes = async (): Promise<Resume[]> => {
  const response = await api.get<Resume[]>("/resumes");
  return response.data;
};


// Get single resume
export const getResume = async (resumeId: number): Promise<Resume> => {
  const response = await api.get<Resume>(`/resumes/${resumeId}`);
  return response.data;
};


// Upload resume
export const uploadResume = async (file: File) => {
  const formData = new FormData();

  formData.append(
    "title",
    file.name.replace(/\.[^/.]+$/, "")
  );

  formData.append("file", file);

  const response = await api.post(
    "/resumes/upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};


// Delete resume
export const deleteResume = async (resumeId: number) => {
  const response = await api.delete(`/resumes/${resumeId}`);

  return response.data;
};


// Set default resume
export const setDefaultResume = async (resumeId: number) => {
  const response = await api.patch(
    `/resumes/${resumeId}/default`
  );

  return response.data;
};


// Parse resume using AI
export const parseResume = async (resumeId: number) => {
  const response = await api.post(
    `/resumes/${resumeId}/parse`
  );

  return response.data;
};


// Get parsed resume
export const getParsedResume = async (resumeId: number) => {
  const response = await api.get(
    `/resumes/parsed/${resumeId}`
  );

  return response.data;
};


// Generate ATS score
export const getATSScore = async (resumeId: number) => {
  const response = await api.post(
    `/resumes/${resumeId}/ats`
  );

  return response.data;
};


// Download resume
export const downloadResume = async (resumeId: number) => {
  const response = await api.get(
    `/resumes/${resumeId}/download`,
    {
      responseType: "blob",
    }
  );

  return response.data;
};