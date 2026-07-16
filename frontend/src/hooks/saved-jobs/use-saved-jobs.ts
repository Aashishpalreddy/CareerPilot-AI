import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { savedJobService } from "@/services/saved-job/saved-job.service";
import { toast } from "sonner";
import type { SavedJob } from "@/types/job";

export const savedJobKeys = {
  all: ["saved-jobs"] as const,
  lists: () => [...savedJobKeys.all, "list"] as const,
  details: () => [...savedJobKeys.all, "detail"] as const,
  detail: (id: number) => [...savedJobKeys.details(), id] as const,
};

export function useSavedJobs() {
  return useQuery({
    queryKey: savedJobKeys.lists(),
    queryFn: () => savedJobService.list(),
  });
}

export function useSavedJob(id: number) {
  return useQuery({
    queryKey: savedJobKeys.detail(id),
    queryFn: () => savedJobService.getById(id),
    enabled: !!id,
  });
}

export function useUpdateSavedJobStatus() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, status }: { id: number; status: "saved" | "applied" | "dismissed" }) =>
      savedJobService.updateStatus(id, status),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: savedJobKeys.lists() });
      queryClient.invalidateQueries({ queryKey: savedJobKeys.detail(variables.id) });
      toast.success(`Job marked as ${variables.status}`);
    },
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || "Failed to update job status");
    },
  });
}

export function useMarkApplied() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => savedJobService.markApplied(id),
    onSuccess: (data: SavedJob) => {
      queryClient.invalidateQueries({ queryKey: savedJobKeys.lists() });
      queryClient.invalidateQueries({ queryKey: savedJobKeys.detail(data.id) });
      toast.success("Job marked as applied!");
    },
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || "Failed to mark as applied");
    },
  });
}

export function useProcessJob() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (jobId: number) => savedJobService.processJob(jobId),
    onSuccess: (data: SavedJob) => {
      queryClient.invalidateQueries({ queryKey: savedJobKeys.lists() });
      queryClient.invalidateQueries({ queryKey: savedJobKeys.detail(data.id) });
      toast.success(
        data.status === "ready"
          ? "Tailored, and the application form was pre-filled — review and submit it yourself."
          : "Resume and cover letter tailored for this job."
      );
    },
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || "Failed to tailor this job");
    },
  });
}

export function useDismissSavedJob() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => savedJobService.dismiss(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: savedJobKeys.lists() });
      toast.success("Job dismissed");
    },
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || "Failed to dismiss job");
    },
  });
}
