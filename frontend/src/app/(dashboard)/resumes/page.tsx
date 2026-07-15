"use client";

import UploadResume from "@/components/resume/upload-resume";
import ResumeList from "@/components/resume/resume-list";


export default function ResumesPage() {

  return (
    <div className="space-y-6">

      <div>
        <h1 className="text-3xl font-bold">
          Resume Management
        </h1>

        <p className="text-muted-foreground">
          Upload, manage, and analyze your resumes using AI.
        </p>
      </div>



      <div>
        <UploadResume />
      </div>



      <div>
        <ResumeList />
      </div>


    </div>
  );
}