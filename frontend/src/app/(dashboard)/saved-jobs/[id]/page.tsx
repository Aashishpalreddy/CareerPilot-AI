"use client";

import { use } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useSavedJob, useUpdateSavedJobStatus, useDismissSavedJob } from "@/hooks/saved-jobs/use-saved-jobs";
import { savedJobService } from "@/services/saved-job/saved-job.service";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Loader2, ArrowLeft, ExternalLink, CheckCircle, FileText, Send, Building, Download, MapPin, Star } from "lucide-react";
import { toast } from "sonner";

function handleDownloadFile(url: string, filename: string, label: string) {
  const token = localStorage.getItem("careerpilot_token");
  
  fetch(url, {
    headers: { Authorization: `Bearer ${token}` },
  })
    .then((res) => {
      if (!res.ok) throw new Error("Download failed");
      return res.blob();
    })
    .then((blob) => {
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = filename;
      a.click();
      URL.revokeObjectURL(a.href);
      toast.success(`${label} downloaded!`);
    })
    .catch(() => toast.error(`No ${label.toLowerCase()} available for this job.`));
}

export default function SavedJobDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  const id = parseInt(resolvedParams.id, 10);
  const router = useRouter();
  
  const { data: savedJob, isLoading } = useSavedJob(id);
  const updateStatus = useUpdateSavedJobStatus();
  const dismissMutation = useDismissSavedJob();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <Loader2 className="h-12 w-12 animate-spin text-blue-500" />
      </div>
    );
  }

  if (!savedJob) {
    return (
      <div className="text-center py-20">
        <h2 className="text-2xl font-bold mb-4">Job Not Found</h2>
        <Link href="/saved-jobs">
          <Button variant="outline">Back to Saved Jobs</Button>
        </Link>
      </div>
    );
  }

  const handleApply = () => {
    if (savedJob.apply_url) {
      window.open(savedJob.apply_url, '_blank');
      updateStatus.mutate({ id: savedJob.id, status: "applied" });
    } else {
      toast.error("No application URL found for this job.");
    }
  };

  const handleDismiss = () => {
    dismissMutation.mutate(savedJob.id, {
      onSuccess: () => router.push("/saved-jobs"),
    });
  };

  return (
    <div className="space-y-6 pb-20">
      {/* Header & Back Button */}
      <div className="flex items-center gap-4">
        <Link href="/saved-jobs">
          <Button variant="ghost" size="icon" className="text-slate-400 hover:text-white hover:bg-slate-800">
            <ArrowLeft className="h-5 w-5" />
          </Button>
        </Link>
        <div>
          <h1 className="text-3xl font-bold">{savedJob.job?.title}</h1>
          <div className="text-slate-400 flex items-center gap-2 mt-1">
            <Building className="h-4 w-4" />
            {savedJob.job?.company}
            {savedJob.job?.location && (
              <>
                <span className="text-slate-600">•</span>
                <MapPin className="h-4 w-4" />
                <span>{savedJob.job.location}</span>
              </>
            )}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Column: Job & Match Details */}
        <div className="lg:col-span-1 space-y-6">
          <Card className="bg-slate-900/50 border-slate-800">
            <CardHeader>
              <CardTitle>Match Analysis</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-center p-6 bg-slate-800/30 rounded-xl border border-slate-700/50 mb-6">
                <div className="text-center">
                  <div className={`text-5xl font-extrabold ${
                    savedJob.match_score >= 75 ? 'text-green-400' : 
                    savedJob.match_score >= 50 ? 'text-yellow-400' : 
                    'text-slate-400'
                  }`}>
                    {savedJob.match_score}%
                  </div>
                  <div className="text-slate-400 mt-2 text-sm font-medium">Match Score</div>
                  {savedJob.match_score >= 75 && (
                    <div className="flex items-center gap-1 mt-2 text-green-400 text-xs">
                      <Star className="h-3.5 w-3.5" />
                      High Match
                    </div>
                  )}
                </div>
              </div>

              {/* Download Buttons */}
              <div className="space-y-3 mb-6">
                <Button 
                  variant="outline" 
                  className="w-full border-blue-500/30 text-blue-400 hover:bg-blue-500/10 hover:text-blue-300 h-11"
                  onClick={() => handleDownloadFile(
                    savedJobService.getDownloadResumeUrl(savedJob.id),
                    `tailored_resume_${savedJob.id}.docx`,
                    "Tailored resume"
                  )}
                >
                  <Download className="mr-2 h-4 w-4" />
                  Get Tailored Resume (.docx)
                </Button>
                <Button 
                  variant="outline" 
                  className="w-full border-indigo-500/30 text-indigo-400 hover:bg-indigo-500/10 hover:text-indigo-300 h-11"
                  onClick={() => handleDownloadFile(
                    savedJobService.getDownloadCoverLetterUrl(savedJob.id),
                    `cover_letter_${savedJob.id}.docx`,
                    "Cover letter"
                  )}
                >
                  <Download className="mr-2 h-4 w-4" />
                  Get Cover Letter (.docx)
                </Button>
              </div>

              {/* Apply / Status Actions */}
              <div className="space-y-3">
                {savedJob.status === "applied" ? (
                  <Button 
                    className="w-full bg-green-600 hover:bg-green-700 h-12 text-lg text-white"
                    disabled
                  >
                    <CheckCircle className="mr-2 h-5 w-5" />
                    Applied
                  </Button>
                ) : (
                  <Button 
                    className="w-full bg-blue-600 hover:bg-blue-700 h-12 text-lg"
                    onClick={handleApply}
                  >
                    <Send className="mr-2 h-5 w-5" />
                    Apply Now
                  </Button>
                )}
                
                {savedJob.status !== "dismissed" && savedJob.status !== "applied" && (
                  <Button 
                    variant="outline" 
                    className="w-full border-slate-700 hover:bg-slate-800 text-slate-300"
                    onClick={handleDismiss}
                  >
                    Dismiss this match
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Recruiter Links if any */}
          {savedJob.recruiter_links && Object.keys(savedJob.recruiter_links).length > 0 && (
            <Card className="bg-slate-900/50 border-slate-800">
              <CardHeader>
                <CardTitle>Find Recruiters</CardTitle>
                <CardDescription>Reach out to hiring managers directly</CardDescription>
              </CardHeader>
              <CardContent className="space-y-2">
                {Object.entries(savedJob.recruiter_links).map(([platform, url]) => (
                  <a key={platform} href={url as string} target="_blank" rel="noopener noreferrer" className="block">
                    <Button variant="outline" className="w-full justify-start border-slate-700 hover:bg-slate-800 hover:border-slate-600">
                      <ExternalLink className="mr-2 h-4 w-4 text-blue-400" />
                      Search on {platform}
                    </Button>
                  </a>
                ))}
              </CardContent>
            </Card>
          )}
        </div>

        {/* Right Column: Generated Materials */}
        <div className="lg:col-span-2 space-y-6">
          
          <Card className="bg-slate-900/50 border-slate-800 border-t-4 border-t-indigo-500">
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5 text-indigo-400" />
                  Tailored Cover Letter
                </CardTitle>
                <CardDescription>AI-generated for {savedJob.job?.company}</CardDescription>
              </div>
              <Button 
                variant="secondary" 
                size="sm" 
                className="bg-slate-800 hover:bg-slate-700 text-slate-200"
                onClick={() => handleDownloadFile(
                  savedJobService.getDownloadCoverLetterUrl(savedJob.id),
                  `cover_letter_${savedJob.id}.docx`,
                  "Cover letter"
                )}
              >
                <Download className="mr-1.5 h-3.5 w-3.5" />
                Download .docx
              </Button>
            </CardHeader>
            <CardContent>
              <div className="bg-slate-950 p-6 rounded-lg border border-slate-800 whitespace-pre-wrap text-slate-300 font-serif leading-relaxed h-[300px] overflow-y-auto">
                {savedJob.cover_letter_text || "No cover letter generated."}
              </div>
            </CardContent>
          </Card>

          <Card className="bg-slate-900/50 border-slate-800 border-t-4 border-t-blue-500">
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5 text-blue-400" />
                  Tailored Resume Profile
                </CardTitle>
                <CardDescription>Key sections rewritten to beat the ATS</CardDescription>
              </div>
              <Button 
                variant="secondary" 
                size="sm" 
                className="bg-slate-800 hover:bg-slate-700 text-slate-200"
                onClick={() => handleDownloadFile(
                  savedJobService.getDownloadResumeUrl(savedJob.id),
                  `tailored_resume_${savedJob.id}.docx`,
                  "Tailored resume"
                )}
              >
                <Download className="mr-1.5 h-3.5 w-3.5" />
                Download .docx
              </Button>
            </CardHeader>
            <CardContent>
              <div className="bg-slate-950 p-6 rounded-lg border border-slate-800 whitespace-pre-wrap text-slate-300 font-serif leading-relaxed h-[300px] overflow-y-auto">
                {savedJob.tailored_resume_text || "No tailored resume generated."}
              </div>
            </CardContent>
          </Card>

        </div>
      </div>
    </div>
  );
}
