"use client";

import Link from "next/link";
import { useResumes } from "@/hooks/resumes/use-resumes";
import { useJobs } from "@/hooks/jobs/use-jobs";
import { useSavedJobs } from "@/hooks/saved-jobs/use-saved-jobs";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FileText, Briefcase, Bookmark, Plus, Loader2 } from "lucide-react";

export default function DashboardPage() {
  
  const { data: resumes, isLoading: resumesLoading } = useResumes();
  const { data: jobs, isLoading: jobsLoading } = useJobs();
  const { data: savedJobs, isLoading: savedJobsLoading } = useSavedJobs();

  const isLoading = resumesLoading || jobsLoading || savedJobsLoading;

  return (
    <div className="space-y-8">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
            Dashboard
          </h1>
          <p className="text-slate-400 mt-1">Overview of your career automation pipeline.</p>
        </div>
        
        <div className="flex gap-3">
          <Link href="/resumes/new">
            <Button variant="outline" className="bg-slate-900 border-slate-700 hover:bg-slate-800">
              <Plus className="mr-2 h-4 w-4" />
              Upload Resume
            </Button>
          </Link>
          <Link href="/jobs">
            <Button className="bg-blue-600 hover:bg-blue-700">
              <Plus className="mr-2 h-4 w-4" />
              Add Job
            </Button>
          </Link>
        </div>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-20">
          <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
        </div>
      ) : (
        <>
          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card className="bg-slate-900/50 border-slate-800">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-slate-400">Total Resumes</CardTitle>
                <FileText className="h-4 w-4 text-slate-400" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">{resumes?.length || 0}</div>
              </CardContent>
            </Card>
            
            <Card className="bg-slate-900/50 border-slate-800">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-slate-400">Tracked Jobs</CardTitle>
                <Briefcase className="h-4 w-4 text-slate-400" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">{jobs?.length || 0}</div>
              </CardContent>
            </Card>
            
            <Card className="bg-slate-900/50 border-slate-800">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-slate-400">Saved Matches</CardTitle>
                <Bookmark className="h-4 w-4 text-slate-400" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">{savedJobs?.length || 0}</div>
              </CardContent>
            </Card>
          </div>

          {/* Recent Activity / Next Steps */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 pt-4">
            <Card className="bg-slate-900/50 border-slate-800">
              <CardHeader>
                <CardTitle>Recent Matches</CardTitle>
                <CardDescription>Top job matches discovered for you</CardDescription>
              </CardHeader>
              <CardContent>
                {!savedJobs || savedJobs.length === 0 ? (
                  <div className="text-center py-8 text-slate-400">
                    <p className="mb-4">No matches found yet.</p>
                    <Link href="/jobs">
                      <Button variant="outline" className="border-slate-700">Run Pipeline</Button>
                    </Link>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {savedJobs.slice(0, 4).map((job) => (
                      <div key={job.id} className="flex items-center justify-between p-4 rounded-lg bg-slate-800/50 border border-slate-700/50">
                        <div>
                          <div className="font-medium">{job.job?.title || "Unknown Title"}</div>
                          <div className="text-sm text-slate-400">{job.job?.company || "Unknown Company"}</div>
                        </div>
                        <div className="flex flex-col items-end">
                          <span className={`text-sm font-bold ${job.match_score > 70 ? 'text-green-400' : job.match_score > 50 ? 'text-yellow-400' : 'text-slate-400'}`}>
                            {job.match_score}% Match
                          </span>
                          <Link href={`/saved-jobs/${job.id}`} className="text-xs text-blue-400 hover:underline mt-1">
                            View details
                          </Link>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>

            <Card className="bg-slate-900/50 border-slate-800">
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
                <CardDescription>Common tasks to manage your applications</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Link href="/jobs" className="block p-4 rounded-lg border border-slate-700 hover:border-slate-500 hover:bg-slate-800/50 transition-colors group">
                  <div className="flex items-center">
                    <div className="h-10 w-10 rounded bg-blue-500/10 flex items-center justify-center mr-4 group-hover:bg-blue-500/20 transition-colors">
                      <Briefcase className="h-5 w-5 text-blue-400" />
                    </div>
                    <div>
                      <div className="font-medium">Discover New Jobs</div>
                      <div className="text-sm text-slate-400">Run the AI pipeline to find new matches</div>
                    </div>
                  </div>
                </Link>

                <Link href="/resumes" className="block p-4 rounded-lg border border-slate-700 hover:border-slate-500 hover:bg-slate-800/50 transition-colors group">
                  <div className="flex items-center">
                    <div className="h-10 w-10 rounded bg-indigo-500/10 flex items-center justify-center mr-4 group-hover:bg-indigo-500/20 transition-colors">
                      <FileText className="h-5 w-5 text-indigo-400" />
                    </div>
                    <div>
                      <div className="font-medium">Update Default Resume</div>
                      <div className="text-sm text-slate-400">Upload a fresh copy of your master resume</div>
                    </div>
                  </div>
                </Link>
              </CardContent>
            </Card>
          </div>
        </>
      )}
    </div>
  );
}