"use client";

import Link from "next/link";
import { ArrowLeft, Briefcase } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { useCreateJob } from "@/hooks/jobs/use-jobs";

export default function NewJobPage() {
  const router = useRouter();
  const createJob = useCreateJob();
  
  const [title, setTitle] = useState("");
  const [company, setCompany] = useState("");
  const [url, setUrl] = useState("");

  const handleSave = async () => {
    if (!title || !company) {
      alert("Please enter at least a title and company.");
      return;
    }
    
    // The backend just expects raw_text right now for jobs, which gets parsed.
    // We'll bundle the info into raw_text so it can be parsed later.
    const raw_text = `Job Title: ${title}\nCompany: ${company}\nJob URL: ${url}\n\nManual Entry`;
    
    createJob.mutate(
      { title, company, job_url: url, raw_text },
      {
        onSuccess: () => {
          router.push("/jobs");
        }
      }
    );
  };
  return (
    <div className="space-y-8 max-w-3xl mx-auto">
      <div className="flex items-center gap-4">
        <Link href="/jobs">
          <Button variant="ghost" size="icon" className="hover:bg-slate-800">
            <ArrowLeft className="h-5 w-5" />
          </Button>
        </Link>
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
            Add Manual Job
          </h1>
          <p className="text-slate-400 mt-1">Track a job application manually.</p>
        </div>
      </div>

      <Card className="bg-slate-900/50 border-slate-800">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Briefcase className="h-5 w-5 text-blue-400" />
            Job Details
          </CardTitle>
          <CardDescription>
            Enter the details of the job you want to track.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-4">
            <div className="grid gap-2">
              <label className="text-sm font-medium text-slate-300">Job Title</label>
              <Input 
                placeholder="e.g. Software Engineer" 
                className="bg-slate-800/50 border-slate-700" 
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />
            </div>
            
            <div className="grid gap-2">
              <label className="text-sm font-medium text-slate-300">Company</label>
              <Input 
                placeholder="e.g. Acme Corp" 
                className="bg-slate-800/50 border-slate-700" 
                value={company}
                onChange={(e) => setCompany(e.target.value)}
              />
            </div>

            <div className="grid gap-2">
              <label className="text-sm font-medium text-slate-300">Job URL</label>
              <Input 
                placeholder="https://..." 
                className="bg-slate-800/50 border-slate-700" 
                value={url}
                onChange={(e) => setUrl(e.target.value)}
              />
            </div>

            <Button 
              className="w-full bg-blue-600 hover:bg-blue-700 mt-4" 
              onClick={handleSave}
              disabled={createJob.isPending}
            >
              {createJob.isPending ? "Saving..." : "Save Job"}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
