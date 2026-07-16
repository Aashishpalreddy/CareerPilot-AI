"use client";

import { useRef, useState } from "react";
import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";

import { useUploadResume } from "@/hooks/resumes/use-upload-resume";

interface UploadResumeProps {
  onSuccessCallback?: () => void;
}

export default function UploadResume({ onSuccessCallback }: UploadResumeProps = {}) {
  const [file, setFile] = useState<File | null>(null);
  const router = useRouter();

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

  const handleUpload = async () => {
    if (!file) return;

    try {
      await uploadMutation.mutateAsync(file);
      if (onSuccessCallback) {
        onSuccessCallback();
      } else {
        router.push("/resumes");
      }
    } catch (error) {
      console.error("Upload failed", error);
    }
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