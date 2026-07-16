"use client";

import Link from "next/link";
import { ArrowLeft, UploadCloud, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import UploadResume from "@/components/resume/upload-resume";

export default function NewResumePage() {
  return (
    <div className="space-y-8 max-w-3xl mx-auto">
      <div className="flex items-center gap-4">
        <Link href="/dashboard">
          <Button variant="ghost" size="icon" className="hover:bg-slate-800">
            <ArrowLeft className="h-5 w-5" />
          </Button>
        </Link>
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
            Upload New Resume
          </h1>
          <p className="text-slate-400 mt-1">Add a new resume to your CareerPilot AI.</p>
        </div>
      </div>

      <Card className="bg-slate-900/50 border-slate-800">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <UploadCloud className="h-5 w-5 text-blue-400" />
            Resume File
          </CardTitle>
          <CardDescription>
            Upload your resume in PDF or Word format. We&apos;ll automatically parse it and extract the key information.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="rounded-xl border border-dashed border-slate-700 bg-slate-800/20 p-8 flex flex-col items-center justify-center text-center">
            <div className="h-16 w-16 rounded-full bg-blue-500/10 flex items-center justify-center mb-4">
              <FileText className="h-8 w-8 text-blue-400" />
            </div>
            <h3 className="text-lg font-medium mb-2">Select your resume document</h3>
            <p className="text-sm text-slate-400 max-w-sm mb-6">
              Supported formats: .pdf, .doc, .docx. Maximum file size: 5MB.
            </p>
            
            <div className="w-full max-w-md bg-slate-900 p-4 rounded-lg border border-slate-800">
              <UploadResume />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
