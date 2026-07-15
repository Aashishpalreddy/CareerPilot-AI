"use client";

import { useRef, useState } from "react";

import { Button } from "@/components/ui/button";

import { useUploadResume } from "@/hooks/resumes/use-upload-resume";

export default function UploadResume() {
  const [file, setFile] = useState<File | null>(null);

  const inputRef = useRef<HTMLInputElement>(null);

  const uploadMutation = useUploadResume();

  const handleChooseFile = () => {
    inputRef.current?.click();
  };

  const handleFileChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const selectedFile = event.target.files?.[0];

    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const handleUpload = () => {
    if (!file) return;

    uploadMutation.mutate(file);
  };

  return (
    <div className="space-y-4">

      {/* Hidden File Input */}
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.doc,.docx"
        className="hidden"
        onChange={handleFileChange}
      />

      {/* Buttons */}
      <div className="flex gap-3">
        <Button
          type="button"
          variant="outline"
          onClick={handleChooseFile}
        >
          Choose File
        </Button>

        <Button
          type="button"
          onClick={handleUpload}
          disabled={!file || uploadMutation.isPending}
        >
          {uploadMutation.isPending
            ? "Uploading..."
            : "Upload Resume"}
        </Button>
      </div>

      {/* Selected File */}
      {file ? (
        <p className="text-sm text-muted-foreground">
          Selected file: <span className="font-medium">{file.name}</span>
        </p>
      ) : (
        <p className="text-sm text-muted-foreground">
          No file selected
        </p>
      )}
    </div>
  );
}