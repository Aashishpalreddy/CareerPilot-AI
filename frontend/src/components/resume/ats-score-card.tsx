"use client";

import { ATSScore } from "@/types/resume";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";


interface ATSScoreCardProps {
  atsScore: ATSScore;
}


export default function ATSScoreCard({
  atsScore,
}: ATSScoreCardProps) {

  return (
    <Card className="w-full">

      <CardHeader>
        <CardTitle>
          ATS Score
        </CardTitle>
      </CardHeader>


      <CardContent className="space-y-4">


        {/* Score */}
        <div>
          <p className="text-4xl font-bold">
            {atsScore.score}%
          </p>

          <p className="text-sm text-muted-foreground">
            Resume compatibility score
          </p>
        </div>



        {/* Matched Keywords */}
        {atsScore.matched_keywords &&
          atsScore.matched_keywords.length > 0 && (

          <div>

            <h3 className="font-semibold">
              Matching Keywords
            </h3>


            <div className="flex flex-wrap gap-2 mt-2">

              {atsScore.matched_keywords.map(
                (keyword, index) => (

                  <span
                    key={index}
                    className="rounded-md bg-secondary px-3 py-1 text-sm"
                  >
                    {keyword}
                  </span>

                )
              )}

            </div>

          </div>

        )}




        {/* Missing Keywords */}
        {atsScore.missing_keywords &&
          atsScore.missing_keywords.length > 0 && (

          <div>

            <h3 className="font-semibold">
              Missing Keywords
            </h3>


            <div className="flex flex-wrap gap-2 mt-2">

              {atsScore.missing_keywords.map(
                (keyword, index) => (

                  <span
                    key={index}
                    className="rounded-md bg-destructive/10 px-3 py-1 text-sm"
                  >
                    {keyword}
                  </span>

                )
              )}

            </div>

          </div>

        )}




        {/* Suggestions */}
        {atsScore.suggestions &&
          atsScore.suggestions.length > 0 && (

          <div>

            <h3 className="font-semibold">
              Suggestions
            </h3>


            <ul className="list-disc ml-5">

              {atsScore.suggestions.map(
                (suggestion, index) => (

                  <li key={index}>
                    {suggestion}
                  </li>

                )
              )}

            </ul>

          </div>

        )}


      </CardContent>

    </Card>
  );
}