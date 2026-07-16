"use client";

import Link from "next/link";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import ResumeList from "@/components/resume/resume-list";

export default function ResumesPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
            Resume Management
          </h1>
          <p className="text-muted-foreground mt-1">
            Upload, manage, and analyze your resumes using AI.
          </p>
        </div>
        <Link href="/resumes/new">
          <Button className="bg-blue-600 hover:bg-blue-700">
            <Plus className="mr-2 h-4 w-4" />
            Upload Resume
          </Button>
        </Link>
      </div>

      <div>
        <ResumeList />
      </div>
    </div>
  );
}