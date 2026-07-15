import { FileText } from "lucide-react";

import { Resume } from "@/types/resume";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
} from "@/components/ui/card";

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
  return (
    <Card className="w-full transition-shadow hover:shadow-md">
      <CardHeader className="flex flex-row items-start justify-between">

        <div className="flex items-center gap-3">

          <FileText className="h-8 w-8 text-blue-600" />

          <div>

            <h3 className="text-lg font-semibold">
              {resume.original_filename}
            </h3>

            <p className="text-sm text-muted-foreground">
              Uploaded on{" "}
              {new Date(resume.created_at).toLocaleDateString(
                "en-US",
                {
                  year: "numeric",
                  month: "long",
                  day: "numeric",
                }
              )}
            </p>

          </div>

        </div>

        {resume.is_default && (
          <span className="rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-700">
            Default
          </span>
        )}

      </CardHeader>

      <CardContent>

        <div className="flex flex-wrap gap-2">

          <Button
            onClick={() => onParse(resume.id)}
          >
            Parse Resume
          </Button>

          <Button
            variant="secondary"
            onClick={() => onATS(resume.id)}
          >
            ATS Score
          </Button>

          {!resume.is_default && (
            <Button
              variant="outline"
              onClick={() => onSetDefault(resume.id)}
            >
              Set Default
            </Button>
          )}

          <Button
            variant="destructive"
            onClick={() => onDelete(resume.id)}
          >
            Delete
          </Button>

        </div>

      </CardContent>
    </Card>
  );
}