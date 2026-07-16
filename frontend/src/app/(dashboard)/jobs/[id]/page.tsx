"use client";

import { use } from "react";
import { useRouter } from "next/navigation";
import { useJob, useParsedJob } from "@/hooks/jobs/use-jobs";
import { useProcessJob } from "@/hooks/saved-jobs/use-saved-jobs";
import { savedJobService } from "@/services/saved-job/saved-job.service";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button, buttonVariants } from "@/components/ui/button";
import { ArrowLeft, Building2, MapPin, Globe, Loader2, Sparkles, Download, CheckCircle2 } from "lucide-react";
import { Badge } from "@/components/ui/badge";

export default function JobDetailsPage({ params }: { params: Promise<{ id: string }> }) {
  const router = useRouter();
  const { id } = use(params);
  const jobId = parseInt(id, 10);

  const { data: job, isLoading: isJobLoading } = useJob(jobId);
  const { data: parsedJob, isLoading: isParsedLoading } = useParsedJob(jobId);
  const processJob = useProcessJob();

  if (isJobLoading || isParsedLoading) {
    return (
      <div className="flex h-full items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
      </div>
    );
  }

  if (!job) {
    return (
      <div className="p-8">
        <Button variant="ghost" onClick={() => router.back()} className="mb-4">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Jobs
        </Button>
        <Card className="bg-slate-900 border-slate-800 text-center py-12">
          <CardContent>
            <h2 className="text-xl font-semibold mb-2">Job Not Found</h2>
            <p className="text-slate-400">The job you are looking for does not exist or has been deleted.</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex items-center space-x-2">
        <Button variant="ghost" onClick={() => router.back()}>
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        {/* Main Content Area */}
        <div className="md:col-span-2 space-y-6">
          <Card className="bg-slate-900 border-slate-800">
            <CardHeader>
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle className="text-2xl">{job.title || "Unknown Title"}</CardTitle>
                  <CardDescription className="flex items-center gap-4 mt-2 text-base">
                    <span className="flex items-center text-slate-300">
                      <Building2 className="w-4 h-4 mr-1" />
                      {job.company || "Unknown Company"}
                    </span>
                    {job.location && (
                      <span className="flex items-center text-slate-400">
                        <MapPin className="w-4 h-4 mr-1" />
                        {job.location}
                      </span>
                    )}
                  </CardDescription>
                </div>
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    className="border-purple-500/30 hover:bg-purple-500/10 text-purple-400"
                    onClick={() => processJob.mutate(jobId)}
                    disabled={processJob.isPending}
                  >
                    {processJob.isPending ? (
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    ) : (
                      <Sparkles className="w-4 h-4 mr-2" />
                    )}
                    Tailor & Apply
                  </Button>
                  {job.job_url && (
                    <a
                      href={job.job_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className={buttonVariants({ variant: "outline", className: "border-blue-500/30 hover:bg-blue-500/10 text-blue-400" })}
                    >
                      <Globe className="w-4 h-4 mr-2" />
                      Apply Here
                    </a>
                  )}
                </div>
              </div>
            </CardHeader>
          </Card>

          <Card className="bg-slate-900 border-slate-800">
            <CardHeader>
              <CardTitle>Job Description</CardTitle>
            </CardHeader>
            <CardContent>
              <div
                className="prose prose-invert prose-blue max-w-none prose-p:leading-relaxed prose-pre:bg-slate-800"
                dangerouslySetInnerHTML={{ __html: job.raw_text.replace(/\n/g, '<br/>') }}
              />
            </CardContent>
          </Card>

          {processJob.data && (
            <Card className="bg-slate-900 border-slate-800 border-t-4 border-t-purple-500">
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <Sparkles className="h-4 w-4 text-purple-400" />
                  Tailored Materials
                  <Badge variant="secondary" className="ml-2 bg-slate-800 text-slate-300">
                    Match {Math.round(processJob.data.match_score)}%
                  </Badge>
                  {processJob.data.status === "ready" && (
                    <Badge className="bg-amber-900/50 text-amber-300 flex items-center gap-1">
                      <CheckCircle2 className="h-3 w-3" />
                      Form Pre-Filled — Review &amp; Submit
                    </Badge>
                  )}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-5">
                {processJob.data.tailored_resume_text && (
                  <div>
                    <h4 className="text-sm font-medium text-slate-400 mb-2">Tailored Resume Summary</h4>
                    <p className="text-sm text-slate-300 whitespace-pre-line">
                      {processJob.data.tailored_resume_text}
                    </p>
                  </div>
                )}
                {processJob.data.cover_letter_text && (
                  <div>
                    <h4 className="text-sm font-medium text-slate-400 mb-2">Cover Letter</h4>
                    <p className="text-sm text-slate-300 whitespace-pre-line">
                      {processJob.data.cover_letter_text}
                    </p>
                  </div>
                )}
                <div className="flex flex-wrap gap-3 pt-2">
                  {processJob.data.tailored_resume_text && (
                    <a
                      href={savedJobService.getDownloadResumeUrl(processJob.data.id)}
                      className={buttonVariants({ variant: "outline", size: "sm", className: "border-slate-700 text-slate-300" })}
                    >
                      <Download className="h-4 w-4 mr-2" />
                      Download Resume
                    </a>
                  )}
                  {processJob.data.cover_letter_text && (
                    <a
                      href={savedJobService.getDownloadCoverLetterUrl(processJob.data.id)}
                      className={buttonVariants({ variant: "outline", size: "sm", className: "border-slate-700 text-slate-300" })}
                    >
                      <Download className="h-4 w-4 mr-2" />
                      Download Cover Letter
                    </a>
                  )}
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Sidebar / Metadata */}
        <div className="space-y-6">
          <Card className="bg-slate-900 border-slate-800">
            <CardHeader>
              <CardTitle className="text-lg">Metadata</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h4 className="text-sm font-medium text-slate-400 mb-1">Source</h4>
                <p className="text-sm">{job.source || "Unknown Source"}</p>
              </div>
              <div>
                <h4 className="text-sm font-medium text-slate-400 mb-1">Added On</h4>
                <p className="text-sm">
                  {new Date(job.created_at).toLocaleDateString(undefined, {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  })}
                </p>
              </div>
            </CardContent>
          </Card>

          {parsedJob && (
            <Card className="bg-slate-900 border-slate-800 border-t-4 border-t-purple-500">
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <Sparkles className="h-4 w-4 text-purple-400" />
                  AI Parsed Details
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {parsedJob.job_summary && (
                  <div>
                    <h4 className="text-sm font-medium text-slate-400 mb-2">Summary</h4>
                    <p className="text-sm text-slate-300">{parsedJob.job_summary}</p>
                  </div>
                )}
                
                {parsedJob.keywords && parsedJob.keywords.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-slate-400 mb-2">Keywords</h4>
                    <div className="flex flex-wrap gap-2">
                      {parsedJob.keywords.map((kw, i) => (
                        <Badge key={i} variant="secondary" className="bg-slate-800 hover:bg-slate-700 text-slate-300">
                          {kw}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
                
                {parsedJob.technologies && parsedJob.technologies.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-slate-400 mb-2">Technologies</h4>
                    <div className="flex flex-wrap gap-2">
                      {parsedJob.technologies.map((tech, i) => (
                        <Badge key={i} className="bg-blue-900/50 text-blue-300 hover:bg-blue-900/70">
                          {tech}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
