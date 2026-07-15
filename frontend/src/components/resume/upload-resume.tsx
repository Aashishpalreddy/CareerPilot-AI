"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import { useUploadResume } from "@/hooks/resumes/use-upload-resume";


export default function UploadResume() {

  const [file, setFile] = useState<File | null>(null);

  const uploadMutation = useUploadResume();


  const handleFileChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {

    const selectedFile = event.target.files?.[0];

    if (selectedFile) {
      setFile(selectedFile);
    }

  };


  const handleUpload = () => {

    if (!file) {
      return;
    }

    uploadMutation.mutate(file);

  };


  return (
    <div className="space-y-4">


      <Input
        type="file"
        accept=".pdf,.doc,.docx"
        onChange={handleFileChange}
      />


      {file && (
        <p className="text-sm text-muted-foreground">
          Selected file: {file.name}
        </p>
      )}



      <Button
        onClick={handleUpload}
        disabled={!file || uploadMutation.isPending}
      >

        {uploadMutation.isPending
          ? "Uploading..."
          : "Upload Resume"
        }

      </Button>


    </div>
  );
}