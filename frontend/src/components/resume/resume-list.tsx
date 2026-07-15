"use client";

import ResumeCard from "./resume-card";

import { useResumes } from "@/hooks/resumes/use-resumes";
import { useDeleteResume } from "@/hooks/resumes/use-delete-resume";
import { useParseResume } from "@/hooks/resumes/use-parse-resume";
import { useATSScore } from "@/hooks/resumes/use-ats-score";
import { useSetDefaultResume } from "@/hooks/resumes/use-set-default-resume";


export default function ResumeList() {

  const {
    data: resumes,
    isLoading,
    error,
  } = useResumes();


  const deleteMutation = useDeleteResume();

  const parseMutation = useParseResume();

  const atsMutation = useATSScore();

  const defaultMutation = useSetDefaultResume();



  if (isLoading) {
    return (
      <p>
        Loading resumes...
      </p>
    );
  }


  if (error) {
    return (
      <p>
        Failed to load resumes.
      </p>
    );
  }



  if (!resumes || resumes.length === 0) {
    return (
      <p>
        No resumes uploaded yet.
      </p>
    );
  }



  return (
    <div className="grid gap-4">

      {resumes.map((resume: any) => (

        <ResumeCard
          key={resume.id}
          resume={resume}

          onDelete={(id) =>
            deleteMutation.mutate(id)
          }

          onParse={(id) =>
            parseMutation.mutate(id)
          }

          onATS={(id) =>
            atsMutation.mutate(id)
          }

          onSetDefault={(id) =>
            defaultMutation.mutate(id)
          }

        />

      ))}

    </div>
  );
}