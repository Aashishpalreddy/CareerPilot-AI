import { useMutation, useQueryClient } from "@tanstack/react-query";
import { pipelineService } from "@/services/pipeline/pipeline.service";
import { savedJobKeys } from "@/hooks/saved-jobs/use-saved-jobs";
import { jobKeys } from "@/hooks/jobs/use-jobs";
import { toast } from "sonner";
import type { PipelineRunRequest, SavedJob } from "@/types/job";

export function useRunPipeline() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: PipelineRunRequest) => pipelineService.runDailyPipeline(data),
    onSuccess: (data: SavedJob[]) => {
      queryClient.invalidateQueries({ queryKey: savedJobKeys.lists() });
      queryClient.invalidateQueries({ queryKey: jobKeys.lists() });
      toast.success(`Pipeline completed. Found ${data.length} matching jobs.`);
    },
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || "Pipeline run failed");
    },
  });
}
