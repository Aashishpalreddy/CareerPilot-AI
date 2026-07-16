"use client";

import { useParams, useRouter } from "next/navigation";
import { ArrowLeft, AlertCircle } from "lucide-react";

import ParsedResumeView from "@/components/resume/parsed-resume-view";
import { useParsedResume } from "@/hooks/resumes/use-parsed-resume";
import { Button } from "@/components/ui/button";

export default function ParsedResumePage() {
  const params = useParams();
  const router = useRouter();

  const resumeId = Number(params.id);

  const {
    data: parsedResume,
    isLoading,
    error,
  } = useParsedResume(resumeId);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4"></div>
        <p className="text-slate-400">Loading parsed resume...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-center">
        <AlertCircle className="h-16 w-16 text-red-500 mb-4" />
        <h2 className="text-2xl font-bold text-slate-100 mb-2">Failed to load parsed resume</h2>
        <p className="text-slate-400 mb-6">There was an error retrieving the parsed data. It may not exist or parsing failed.</p>
        <Button onClick={() => router.push('/resumes')} variant="outline">
          <ArrowLeft className="mr-2 h-4 w-4" /> Back to Resumes
        </Button>
      </div>
    );
  }

  if (!parsedResume) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-center">
        <AlertCircle className="h-16 w-16 text-yellow-500 mb-4" />
        <h2 className="text-2xl font-bold text-slate-100 mb-2">Parsed resume not found</h2>
        <p className="text-slate-400 mb-6">No parsing data is available for this resume yet.</p>
        <Button onClick={() => router.push('/resumes')} variant="outline">
          <ArrowLeft className="mr-2 h-4 w-4" /> Back to Resumes
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => router.push('/resumes')}>
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div>
          <h1 className="text-3xl font-bold text-slate-100">
            Parsed Resume
          </h1>
          <p className="text-slate-400">
            AI extracted information from your resume.
          </p>
        </div>
      </div>

      <ParsedResumeView
        parsedResume={parsedResume}
      />
    </div>
  );
}