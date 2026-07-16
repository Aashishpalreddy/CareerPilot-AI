import { useMutation, useQueryClient } from "@tanstack/react-query";
import { jobSearchService } from "@/services/job-search/job-search.service";
import { jobKeys } from "@/hooks/jobs/use-jobs";
import { toast } from "sonner";
import type { JobSearchRequest, JobSearchResponse } from "@/types/job";

export function useSearchJobs() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: JobSearchRequest) => jobSearchService.search(data),
    onSuccess: (data: JobSearchResponse) => {
      queryClient.invalidateQueries({ queryKey: jobKeys.lists() });
      toast.success(`Found ${data.total_jobs} matching job${data.total_jobs === 1 ? "" : "s"}.`);
    },
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || "Job search failed");
    },
  });
}
