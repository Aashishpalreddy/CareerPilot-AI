"use client";

import { useParams } from "next/navigation";

import ParsedResumeView from "@/components/resume/parsed-resume-view";
import { useParsedResume } from "@/hooks/resumes/use-parsed-resume";

export default function ParsedResumePage() {
  const params = useParams();

  const resumeId = Number(params.id);

  const {
    data: parsedResume,
    isLoading,
    error,
  } = useParsedResume(resumeId);

  if (isLoading) {
    return <p>Loading parsed resume...</p>;
  }

  if (error) {
    return <p>Failed to load parsed resume.</p>;
  }

  if (!parsedResume) {
    return <p>Parsed resume not found.</p>;
  }

  return (
    <div className="space-y-6">

      <div>
        <h1 className="text-3xl font-bold">
          Parsed Resume
        </h1>

        <p className="text-muted-foreground">
          AI extracted information from your resume.
        </p>
      </div>

      <ParsedResumeView
        parsedResume={parsedResume}
      />

    </div>
  );
}