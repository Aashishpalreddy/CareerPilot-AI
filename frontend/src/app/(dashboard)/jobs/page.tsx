"use client";

import { useState } from "react";
import Link from "next/link";
import { useJobs, useDeleteJob } from "@/hooks/jobs/use-jobs";
import { useRunPipeline } from "@/hooks/pipeline/use-pipeline";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Loader2, Plus, Trash2, Search, Zap, ExternalLink, SlidersHorizontal, MapPin, Building, Clock } from "lucide-react";

export default function JobsPage() {
  const { data: jobs, isLoading } = useJobs();
  const deleteJob = useDeleteJob();
  const runPipeline = useRunPipeline();
  
  const [isPipelineRunning, setIsPipelineRunning] = useState(false);
  const [keywords, setKeywords] = useState("");
  const [location, setLocation] = useState("");
  const [jobType, setJobType] = useState("");
  const [experienceLevel, setExperienceLevel] = useState("");
  const [workArrangement, setWorkArrangement] = useState("");
  const [showFilters, setShowFilters] = useState(false);

  const handleRunPipeline = async () => {
    if (!keywords.trim()) {
      alert("Please enter at least one keyword (e.g., 'software engineer').");
      return;
    }
    
    setIsPipelineRunning(true);
    try {
      await runPipeline.mutateAsync({
        keywords: keywords.split(",").map(k => k.trim()),
        location: location || undefined,
        remote_only: workArrangement === "remote",
        job_type: jobType || undefined,
        experience_level: experienceLevel || undefined,
        work_arrangement: workArrangement || undefined,
      });
    } finally {
      setIsPipelineRunning(false);
    }
  };

  return (
    <div className="space-y-8">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
            Jobs
          </h1>
          <p className="text-slate-400 mt-1">Manage tracked jobs and discover new opportunities.</p>
        </div>
      </div>

      {/* Discovery Tool */}
      <Card className="bg-slate-900/50 border-slate-800 border-l-4 border-l-blue-500">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Zap className="h-5 w-5 text-blue-400" />
            AI Job Discovery
          </CardTitle>
          <CardDescription>
            Enter keywords to scan job boards, filter matches against your resume, and auto-tailor materials.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Keywords Input */}
          <div className="flex flex-col sm:flex-row gap-3">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-3 h-4 w-4 text-slate-500" />
              <Input 
                placeholder="Keywords (e.g. Frontend, React, Next.js)" 
                className="pl-9 bg-slate-800/50 border-slate-700"
                value={keywords}
                onChange={(e) => setKeywords(e.target.value)}
                disabled={isPipelineRunning || runPipeline.isPending}
                onKeyDown={(e) => e.key === "Enter" && handleRunPipeline()}
              />
            </div>
            <Button
              variant="outline"
              className="border-slate-700 bg-slate-800/50 hover:bg-slate-700 text-slate-300"
              onClick={() => setShowFilters(!showFilters)}
            >
              <SlidersHorizontal className="mr-2 h-4 w-4" />
              Filters
            </Button>
          </div>

          {/* Filter Panel */}
          {showFilters && (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 p-4 bg-slate-800/30 rounded-lg border border-slate-700/50 animate-in fade-in slide-in-from-top-2 duration-200">
              {/* Location */}
              <div className="space-y-1.5">
                <label className="text-xs text-slate-400 font-medium flex items-center gap-1.5">
                  <MapPin className="h-3 w-3" />
                  Location
                </label>
                <Input
                  placeholder="e.g. San Francisco, NYC"
                  className="bg-slate-800/50 border-slate-700 h-9 text-sm"
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                />
              </div>
              
              {/* Job Type */}
              <div className="space-y-1.5">
                <label className="text-xs text-slate-400 font-medium flex items-center gap-1.5">
                  <Building className="h-3 w-3" />
                  Job Type
                </label>
                <select
                  value={jobType}
                  onChange={(e) => setJobType(e.target.value)}
                  className="w-full h-9 rounded-md border border-slate-700 bg-slate-800/50 px-3 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/40"
                >
                  <option value="">All Types</option>
                  <option value="full-time">Full-Time</option>
                  <option value="contract">Contract</option>
                  <option value="part-time">Part-Time</option>
                </select>
              </div>
              
              {/* Experience Level */}
              <div className="space-y-1.5">
                <label className="text-xs text-slate-400 font-medium flex items-center gap-1.5">
                  <Clock className="h-3 w-3" />
                  Experience Level
                </label>
                <select
                  value={experienceLevel}
                  onChange={(e) => setExperienceLevel(e.target.value)}
                  className="w-full h-9 rounded-md border border-slate-700 bg-slate-800/50 px-3 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/40"
                >
                  <option value="">All Levels</option>
                  <option value="entry">Entry Level</option>
                  <option value="mid">Mid Level</option>
                  <option value="senior">Senior Level</option>
                </select>
              </div>
              
              {/* Work Arrangement */}
              <div className="space-y-1.5">
                <label className="text-xs text-slate-400 font-medium flex items-center gap-1.5">
                  <MapPin className="h-3 w-3" />
                  Work Arrangement
                </label>
                <select
                  value={workArrangement}
                  onChange={(e) => setWorkArrangement(e.target.value)}
                  className="w-full h-9 rounded-md border border-slate-700 bg-slate-800/50 px-3 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/40"
                >
                  <option value="">Any</option>
                  <option value="remote">Remote</option>
                  <option value="hybrid">Hybrid</option>
                  <option value="onsite">On-site</option>
                </select>
              </div>
            </div>
          )}

          {/* Run Button */}
          <Button 
            className="bg-blue-600 hover:bg-blue-700 w-full sm:w-auto"
            onClick={handleRunPipeline}
            disabled={isPipelineRunning || runPipeline.isPending}
          >
            {(isPipelineRunning || runPipeline.isPending) ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Running Pipeline...
              </>
            ) : (
              <>
                <Search className="mr-2 h-4 w-4" />
                Discover Jobs
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {/* Jobs List */}
      <Card className="bg-slate-900/50 border-slate-800">
        <CardHeader className="flex flex-row items-center justify-between">
          <div>
            <CardTitle>Tracked Jobs</CardTitle>
            <CardDescription>All jobs in your system (manually added or discovered)</CardDescription>
          </div>
          <Link href="/jobs/new">
            <Button variant="outline" className="border-slate-700 text-slate-300">
              <Plus className="mr-2 h-4 w-4" /> Add Manual Job
            </Button>
          </Link>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex justify-center py-12">
              <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
            </div>
          ) : !jobs || jobs.length === 0 ? (
            <div className="text-center py-12 text-slate-400 bg-slate-800/30 rounded-lg border border-dashed border-slate-700">
              <p>No jobs tracked yet.</p>
              <p className="text-sm mt-2">Run the AI Job Discovery tool above to find matches.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {jobs.map((job) => (
                <div 
                  key={job.id} 
                  className="flex flex-col sm:flex-row justify-between p-4 rounded-lg bg-slate-800/50 border border-slate-700 hover:border-slate-600 transition-colors"
                >
                  <div className="mb-4 sm:mb-0">
                    <h3 className="font-semibold text-lg">{job.title}</h3>
                    <div className="text-slate-400 flex items-center gap-2 mt-1">
                      <span>{job.company || "Unknown Company"}</span>
                      {job.location && (
                        <>
                          <span className="text-slate-600">•</span>
                          <span>{job.location}</span>
                        </>
                      )}
                      {job.source && (
                        <>
                          <span className="text-slate-600">•</span>
                          <span className="text-xs px-1.5 py-0.5 rounded bg-slate-700/50 text-slate-400">{job.source}</span>
                        </>
                      )}
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-3">
                    {job.job_url && (
                      <a href={job.job_url} target="_blank" rel="noopener noreferrer">
                        <Button variant="ghost" size="sm" className="text-blue-400 hover:text-blue-300 hover:bg-blue-400/10">
                          <ExternalLink className="h-4 w-4 mr-2" />
                          View Post
                        </Button>
                      </a>
                    )}
                    <Link href={`/jobs/${job.id}`}>
                      <Button variant="ghost" size="sm" className="text-blue-400 hover:text-blue-300 hover:bg-blue-400/10">
                        View Details
                      </Button>
                    </Link>
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      onClick={() => {
                        if (confirm("Are you sure you want to delete this job?")) {
                          deleteJob.mutate(job.id);
                        }
                      }}
                      disabled={deleteJob.isPending}
                      className="text-red-400 hover:text-red-300 hover:bg-red-400/10"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
