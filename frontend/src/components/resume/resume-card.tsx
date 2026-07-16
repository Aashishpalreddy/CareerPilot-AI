import { useState } from "react";
import { FileText, Loader2, Target, CheckCircle2, XCircle, Lightbulb } from "lucide-react";
import { useQuery } from "@tanstack/react-query";

import { Resume } from "@/types/resume";
import { getATSScore } from "@/services/resume/resume.service";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
} from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

interface ResumeCardProps {
  resume: Resume;
  onDelete: (id: number) => void;
  onParse: (id: number) => void;
  onATS: (id: number) => void;
  onSetDefault: (id: number) => void;
}

export default function ResumeCard({
  resume,
  onDelete,
  onParse,
  onATS,
  onSetDefault,
}: ResumeCardProps) {
  const [isParsing, setIsParsing] = useState(false);
  const [isATSOpen, setIsATSOpen] = useState(false);
  const [isGeneratingATS, setIsGeneratingATS] = useState(false);

  // Fetch ATS score when dialog is open
  const { data: atsScore, isLoading: isATSFetching } = useQuery({
    queryKey: ["ats-score", resume.id],
    queryFn: () => getATSScore(resume.id),
    enabled: isATSOpen,
  });

  const handleParse = async () => {
    setIsParsing(true);
    try {
      await onParse(resume.id);
    } finally {
      setIsParsing(false);
    }
  };

  const handleATS = async () => {
    setIsATSOpen(true);
    if (!atsScore) {
      setIsGeneratingATS(true);
      try {
        await onATS(resume.id);
      } finally {
        setIsGeneratingATS(false);
      }
    }
  };

  return (
    <>
      <Card className="w-full transition-shadow hover:shadow-md bg-slate-900/50 border-slate-800">
        <CardHeader className="flex flex-row items-start justify-between">
          <div className="flex items-center gap-3">
            <FileText className="h-8 w-8 text-blue-500" />
            <div>
              <h3 className="text-lg font-semibold text-slate-100">
                {resume.original_filename}
              </h3>
              <p className="text-sm text-slate-400">
                Uploaded on{" "}
                {new Date(resume.created_at).toLocaleDateString("en-US", {
                  year: "numeric",
                  month: "long",
                  day: "numeric",
                })}
              </p>
            </div>
          </div>
          {resume.is_default && (
            <span className="rounded-full bg-green-500/20 px-3 py-1 text-xs font-medium text-green-400 border border-green-500/30">
              Default Resume
            </span>
          )}
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            <Button
              className="bg-blue-600 hover:bg-blue-700"
              onClick={handleParse}
              disabled={isParsing}
            >
              {isParsing ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
              {isParsing ? "Parsing..." : "Parse Resume"}
            </Button>
            <Button
              variant="secondary"
              className="bg-slate-800 hover:bg-slate-700 text-slate-200"
              onClick={handleATS}
              disabled={isGeneratingATS}
            >
              {isGeneratingATS ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
              {isGeneratingATS ? "Calculating..." : "ATS Score"}
            </Button>
            {!resume.is_default && (
              <Button
                variant="outline"
                className="border-slate-700 text-slate-300 hover:bg-slate-800"
                onClick={() => onSetDefault(resume.id)}
              >
                Set Default
              </Button>
            )}
            <Button
              variant="ghost"
              className="text-red-400 hover:bg-red-400/10 hover:text-red-300 ml-auto"
              onClick={() => onDelete(resume.id)}
            >
              Delete
            </Button>
          </div>
        </CardContent>
      </Card>

      <Dialog open={isATSOpen} onOpenChange={setIsATSOpen}>
        <DialogContent className="sm:max-w-[600px] bg-slate-900 border-slate-800 text-slate-100">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2 text-2xl">
              <Target className="h-6 w-6 text-blue-400" />
              ATS Analysis Report
            </DialogTitle>
            <DialogDescription className="text-slate-400">
              AI-powered resume evaluation for Applicant Tracking Systems.
            </DialogDescription>
          </DialogHeader>

          {(isGeneratingATS || isATSFetching) && !atsScore ? (
            <div className="flex flex-col items-center justify-center py-12 text-slate-400">
              <Loader2 className="h-10 w-10 animate-spin text-blue-500 mb-4" />
              <p>Analyzing resume with Gemini AI...</p>
            </div>
          ) : atsScore ? (
            <div className="space-y-6 mt-4">
              <div className="flex flex-col items-center justify-center p-6 bg-slate-800/50 rounded-xl border border-slate-700">
                <div className="text-5xl font-bold mb-2 flex items-baseline">
                  <span className={atsScore.score >= 80 ? "text-green-400" : atsScore.score >= 60 ? "text-yellow-400" : "text-red-400"}>
                    {atsScore.score}
                  </span>
                  <span className="text-2xl text-slate-500 ml-1">/100</span>
                </div>
                <p className="text-sm text-slate-400">Overall ATS Score</p>
              </div>

              <div className="space-y-4">
                {atsScore.strengths && atsScore.strengths.length > 0 && (
                  <div>
                    <h4 className="flex items-center gap-2 font-medium text-green-400 mb-2">
                      <CheckCircle2 className="h-4 w-4" /> Strengths
                    </h4>
                    <ul className="space-y-1 pl-6">
                      {atsScore.strengths.map((item: string, i: number) => (
                        <li key={i} className="text-sm text-slate-300 list-disc">{item}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {atsScore.weaknesses && atsScore.weaknesses.length > 0 && (
                  <div>
                    <h4 className="flex items-center gap-2 font-medium text-red-400 mb-2">
                      <XCircle className="h-4 w-4" /> Weaknesses
                    </h4>
                    <ul className="space-y-1 pl-6">
                      {atsScore.weaknesses.map((item: string, i: number) => (
                        <li key={i} className="text-sm text-slate-300 list-disc">{item}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {atsScore.suggestions && atsScore.suggestions.length > 0 && (
                  <div>
                    <h4 className="flex items-center gap-2 font-medium text-blue-400 mb-2">
                      <Lightbulb className="h-4 w-4" /> Suggestions for Improvement
                    </h4>
                    <ul className="space-y-1 pl-6">
                      {atsScore.suggestions.map((item: string, i: number) => (
                        <li key={i} className="text-sm text-slate-300 list-disc">{item}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="py-8 text-center text-slate-400">
              <p>Failed to load ATS analysis.</p>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </>
  );
}