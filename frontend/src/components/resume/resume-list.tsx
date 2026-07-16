"use client";

import { useRouter } from "next/navigation";

import ResumeCard from "./resume-card";

import { useResumes } from "@/hooks/resumes/use-resumes";
import { useDeleteResume } from "@/hooks/resumes/use-delete-resume";
import { useParseResume } from "@/hooks/resumes/use-parse-resume";
import { useATSScore } from "@/hooks/resumes/use-ats-score";
import { useSetDefaultResume } from "@/hooks/resumes/use-set-default-resume";

export default function ResumeList() {
  const router = useRouter();

  const {
    data: resumes,
    isLoading,
    error,
  } = useResumes();

  const deleteMutation = useDeleteResume();
  const parseMutation = useParseResume();
  const atsMutation = useATSScore();
  const defaultMutation = useSetDefaultResume();

  const handleDelete = (id: number) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this resume?"
    );

    if (!confirmed) return;

    deleteMutation.mutate(id);
  };

  const handleParse = async (id: number) => {
    try {
      await parseMutation.mutateAsync(id);
      router.push(`/resumes/${id}/parsed`);
    } catch {
      // Error toast is handled inside useParseResume's onError.
    }
  };

  if (isLoading) {
    return <p>Loading resumes...</p>;
  }

  if (error) {
    return <p>Failed to load resumes.</p>;
  }

  if (!resumes || resumes.length === 0) {
    return <p>No resumes uploaded yet.</p>;
  }

  return (
    <div className="grid gap-4">
      {resumes.map((resume) => (
        <ResumeCard
          key={resume.id}
          resume={resume}
          onDelete={handleDelete}
          onParse={handleParse}
          onATS={(id) => atsMutation.mutate(id)}
          onSetDefault={(id) => defaultMutation.mutate(id)}
        />
      ))}
    </div>
  );
}