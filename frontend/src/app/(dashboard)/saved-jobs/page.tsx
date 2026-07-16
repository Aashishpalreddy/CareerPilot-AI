"use client";

import Link from "next/link";
import { useSavedJobs, useUpdateSavedJobStatus, useDismissSavedJob } from "@/hooks/saved-jobs/use-saved-jobs";
import { savedJobService } from "@/services/saved-job/saved-job.service";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Loader2, CheckCircle, XCircle, Send, Download, Star, Sparkles, Building, MapPin } from "lucide-react";
import { toast } from "sonner";
import type { SavedJob } from "@/types/job";

function getMatchColor(score: number) {
  if (score >= 75) return "text-green-400";
  if (score >= 50) return "text-yellow-400";
  return "text-slate-400";
}

function getMatchBadgeStyle(score: number) {
  if (score >= 75) return "bg-green-500/20 text-green-400 border-green-500/30";
  if (score >= 50) return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30";
  return "bg-slate-500/20 text-slate-400 border-slate-500/30";
}

function handleDownloadResume(id: number) {
  const url = savedJobService.getDownloadResumeUrl(id);
  const token = localStorage.getItem("careerpilot_token");
  
  // Open download in a new window with auth header via fetch
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
      a.download = `tailored_resume_${id}.docx`;
      a.click();
      URL.revokeObjectURL(a.href);
      toast.success("Resume downloaded!");
    })
    .catch(() => toast.error("No tailored resume available for this job."));
}

function handleDownloadCoverLetter(id: number) {
  const url = savedJobService.getDownloadCoverLetterUrl(id);
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
      a.download = `cover_letter_${id}.docx`;
      a.click();
      URL.revokeObjectURL(a.href);
      toast.success("Cover letter downloaded!");
    })
    .catch(() => toast.error("No cover letter available for this job."));
}


function JobCard({ savedJob, onDismiss, onApply }: { 
  savedJob: SavedJob;
  onDismiss: (id: number) => void;
  onApply: (savedJob: SavedJob) => void;
}) {
  return (
    <div className="flex flex-col p-5 rounded-xl bg-slate-800/50 border border-slate-700 hover:border-slate-600 transition-all duration-200 hover:shadow-lg hover:shadow-blue-500/5">
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-3 mb-1.5">
            <h3 className="font-semibold text-lg text-slate-100 truncate">{savedJob.job?.title || "Unknown Title"}</h3>
            <span className={`shrink-0 px-2.5 py-0.5 rounded-full text-xs font-bold border ${getMatchBadgeStyle(savedJob.match_score)}`}>
              {savedJob.match_score}% Match
            </span>
          </div>
          <div className="text-slate-400 text-sm flex items-center gap-2">
            <Building className="h-3.5 w-3.5" />
            {savedJob.job?.company || "Unknown Company"}
            {savedJob.job?.location && (
              <>
                <span className="text-slate-600">•</span>
                <MapPin className="h-3.5 w-3.5" />
                {savedJob.job.location}
              </>
            )}
          </div>
        </div>
      </div>

      {/* Tags */}
      <div className="flex flex-wrap gap-2 mb-4">
        {savedJob.auto_apply_eligible && (
          <span className="px-2 py-1 bg-purple-500/10 text-purple-400 border border-purple-500/20 rounded text-xs font-medium">
            ⚡ Auto-Apply Eligible
          </span>
        )}
        {savedJob.tailored_resume_text && (
          <span className="px-2 py-1 bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded text-xs font-medium">
            📄 Resume Ready
          </span>
        )}
        {savedJob.cover_letter_text && (
          <span className="px-2 py-1 bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded text-xs font-medium">
            ✉️ Cover Letter Ready
          </span>
        )}
        {savedJob.status === "ready" && (
          <span className="px-2 py-1 bg-amber-500/10 text-amber-400 border border-amber-500/20 rounded text-xs font-medium">
            📝 Form Pre-Filled — Review &amp; Submit
          </span>
        )}
        {savedJob.status === "applied" && (
          <span className="px-2 py-1 bg-green-500/10 text-green-400 border border-green-500/20 rounded text-xs font-medium">
            ✅ Applied
          </span>
        )}
      </div>

      {/* Actions */}
      <div className="flex flex-wrap items-center gap-2 pt-3 border-t border-slate-700/50">
        <Button 
          size="sm"
          variant="outline"
          className="border-blue-500/30 text-blue-400 hover:bg-blue-500/10 hover:text-blue-300"
          onClick={() => handleDownloadResume(savedJob.id)}
        >
          <Download className="mr-1.5 h-3.5 w-3.5" />
          Get Resume
        </Button>
        <Button 
          size="sm"
          variant="outline"
          className="border-indigo-500/30 text-indigo-400 hover:bg-indigo-500/10 hover:text-indigo-300"
          onClick={() => handleDownloadCoverLetter(savedJob.id)}
        >
          <Download className="mr-1.5 h-3.5 w-3.5" />
          Get Cover Letter
        </Button>

        {savedJob.status !== "applied" ? (
          <Button 
            size="sm"
            className="bg-blue-600 hover:bg-blue-700 ml-auto"
            onClick={() => onApply(savedJob)}
          >
            <Send className="mr-1.5 h-3.5 w-3.5" />
            Apply
          </Button>
        ) : (
          <Button 
            size="sm"
            className="bg-green-600/20 text-green-400 border border-green-500/30 ml-auto cursor-default"
            disabled
          >
            <CheckCircle className="mr-1.5 h-3.5 w-3.5" />
            Applied
          </Button>
        )}

        <Link href={`/saved-jobs/${savedJob.id}`}>
          <Button size="sm" variant="ghost" className="text-slate-400 hover:text-white hover:bg-slate-700">
            Details
          </Button>
        </Link>
        
        {savedJob.status !== "applied" && (
          <Button 
            size="sm"
            variant="ghost"
            className="text-slate-500 hover:text-red-400 hover:bg-red-400/10"
            onClick={() => onDismiss(savedJob.id)}
          >
            <XCircle className="h-3.5 w-3.5" />
          </Button>
        )}
      </div>
    </div>
  );
}

export default function SavedJobsPage() {
  const { data: savedJobs, isLoading } = useSavedJobs();
  const updateStatus = useUpdateSavedJobStatus();
  const dismissMutation = useDismissSavedJob();

  const handleApply = (savedJob: SavedJob) => {
    if (savedJob.apply_url) {
      window.open(savedJob.apply_url, "_blank");
      updateStatus.mutate({ id: savedJob.id, status: "applied" });
    } else {
      toast.error("No application URL found for this job.");
    }
  };

  const handleDismiss = (id: number) => {
    dismissMutation.mutate(id);
  };

  // Filter and categorize
  const activeJobs = savedJobs?.filter(j => j.status !== "dismissed") || [];
  const highMatchJobs = activeJobs.filter(j => j.match_score >= 75).sort((a, b) => b.match_score - a.match_score);
  const otherJobs = activeJobs.filter(j => j.match_score < 75).sort((a, b) => b.match_score - a.match_score);
  const appliedJobs = savedJobs?.filter(j => j.status === "applied") || [];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
          Saved Matches
        </h1>
        <p className="text-slate-400 mt-1">High-quality job matches discovered by AI, with tailored materials ready.</p>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-16">
          <Loader2 className="h-10 w-10 animate-spin text-blue-500" />
        </div>
      ) : activeJobs.length === 0 && appliedJobs.length === 0 ? (
        <Card className="bg-slate-900/50 border-slate-800">
          <CardContent className="py-16">
            <div className="text-center text-slate-400">
              <Sparkles className="h-12 w-12 mx-auto mb-4 text-slate-600" />
              <p className="text-lg mb-2">No matches yet.</p>
              <p className="text-sm mb-4">Run the AI Job Discovery pipeline to find matching jobs.</p>
              <Link href="/jobs">
                <Button className="bg-blue-600 hover:bg-blue-700">
                  Discover Jobs
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      ) : (
        <>
          {/* 75+ Score Section */}
          {highMatchJobs.length > 0 && (
            <Card className="bg-slate-900/50 border-slate-800 border-l-4 border-l-green-500">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Star className="h-5 w-5 text-green-400" />
                  High Match (75%+)
                  <span className="text-sm font-normal text-slate-400 ml-2">
                    {highMatchJobs.length} {highMatchJobs.length === 1 ? "job" : "jobs"}
                  </span>
                </CardTitle>
                <CardDescription>
                  These jobs are highly matched to your profile. Tailored resumes and cover letters are ready.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {highMatchJobs.map((savedJob) => (
                    <JobCard 
                      key={savedJob.id} 
                      savedJob={savedJob}
                      onDismiss={handleDismiss}
                      onApply={handleApply}
                    />
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Other Matches */}
          {otherJobs.length > 0 && (
            <Card className="bg-slate-900/50 border-slate-800">
              <CardHeader>
                <CardTitle>Other Matches</CardTitle>
                <CardDescription>
                  Jobs below the 75% threshold. Review and apply if interested.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {otherJobs.map((savedJob) => (
                    <JobCard 
                      key={savedJob.id} 
                      savedJob={savedJob}
                      onDismiss={handleDismiss}
                      onApply={handleApply}
                    />
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Applied Section */}
          {appliedJobs.length > 0 && (
            <Card className="bg-slate-900/50 border-slate-800 border-l-4 border-l-green-500/50">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <CheckCircle className="h-5 w-5 text-green-500" />
                  Applied
                  <span className="text-sm font-normal text-slate-400 ml-2">
                    {appliedJobs.length} {appliedJobs.length === 1 ? "job" : "jobs"}
                  </span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {appliedJobs.map((savedJob) => (
                    <div 
                      key={savedJob.id}
                      className="flex items-center justify-between p-4 rounded-lg bg-slate-800/30 border border-slate-700/50"
                    >
                      <div>
                        <div className="font-medium text-slate-200">{savedJob.job?.title}</div>
                        <div className="text-sm text-slate-400">{savedJob.job?.company} • {savedJob.job?.location}</div>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className={`text-sm font-bold ${getMatchColor(savedJob.match_score)}`}>
                          {savedJob.match_score}%
                        </span>
                        <Link href={`/saved-jobs/${savedJob.id}`}>
                          <Button size="sm" variant="ghost" className="text-slate-400 hover:text-white">
                            View
                          </Button>
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </>
      )}
    </div>
  );
}
