import { Resume } from "@/types/resume";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";


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
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">

          <span>
            {resume.filename}
          </span>


          {resume.is_default && (
            <span className="text-sm text-green-600">
              Default
            </span>
          )}

        </CardTitle>
      </CardHeader>


      <CardContent>

        <p className="text-sm text-muted-foreground mb-4">
          Uploaded:
          {" "}
          {new Date(resume.uploaded_at).toLocaleDateString()}
        </p>


        <div className="flex flex-wrap gap-2">

          <Button
            onClick={() => onParse(resume.id)}
          >
            Parse
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