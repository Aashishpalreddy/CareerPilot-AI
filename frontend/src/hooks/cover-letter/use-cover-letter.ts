import { useMutation } from "@tanstack/react-query";
import { coverLetterService } from "@/services/cover-letter/cover-letter.service";
import { toast } from "sonner";

export function useGenerateCoverLetter() {
  return useMutation({
    mutationFn: ({ resumeId, jobId }: { resumeId: number; jobId: number }) =>
      coverLetterService.generate(resumeId, jobId),
    onSuccess: () => {
      toast.success("Cover letter generated successfully");
    },
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || "Failed to generate cover letter");
    },
  });
}
