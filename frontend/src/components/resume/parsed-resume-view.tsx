"use client";

import { ParsedResume } from "@/types/resume";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";


interface ParsedResumeViewProps {
  parsedResume: ParsedResume;
}


export default function ParsedResumeView({
  parsedResume,
}: ParsedResumeViewProps) {

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>
          Parsed Resume
        </CardTitle>
      </CardHeader>


      <CardContent className="space-y-6">


        {/* Summary */}
        {parsedResume.summary && (
          <div>
            <h3 className="font-semibold">
              Summary
            </h3>

            <p className="text-sm text-muted-foreground">
              {parsedResume.summary}
            </p>
          </div>
        )}



        {/* Skills */}
        {parsedResume.skills &&
          parsedResume.skills.length > 0 && (

          <div>
            <h3 className="font-semibold">
              Skills
            </h3>

            <div className="flex flex-wrap gap-2 mt-2">

              {parsedResume.skills.map(
                (skill, index) => (
                  <span
                    key={index}
                    className="rounded-md bg-secondary px-3 py-1 text-sm"
                  >
                    {skill}
                  </span>
                )
              )}

            </div>
          </div>

        )}



        {/* Experience */}
        {parsedResume.experience &&
          parsedResume.experience.length > 0 && (

          <div>

            <h3 className="font-semibold">
              Experience
            </h3>


            {parsedResume.experience.map(
              (exp, index) => (

                <div
                  key={index}
                  className="mt-3"
                >

                  <p className="font-medium">
                    {exp.title}
                  </p>


                  <p className="text-sm">
                    {exp.company}
                  </p>


                  <p className="text-sm text-muted-foreground">
                    {exp.description}
                  </p>

                </div>

              )
            )}

          </div>

        )}



        {/* Education */}
        {parsedResume.education &&
          parsedResume.education.length > 0 && (

          <div>

            <h3 className="font-semibold">
              Education
            </h3>


            {parsedResume.education.map(
              (edu, index) => (

                <p
                  key={index}
                  className="text-sm"
                >
                  {edu.degree} - {edu.institution}
                </p>

              )
            )}

          </div>

        )}



        {/* Projects */}
        {parsedResume.projects &&
          parsedResume.projects.length > 0 && (

          <div>

            <h3 className="font-semibold">
              Projects
            </h3>


            {parsedResume.projects.map(
              (project, index) => (

                <div
                  key={index}
                  className="mt-2"
                >

                  <p className="font-medium">
                    {project.name}
                  </p>

                  <p className="text-sm text-muted-foreground">
                    {project.description}
                  </p>

                </div>

              )
            )}

          </div>

        )}



        {/* Certifications */}
        {parsedResume.certifications &&
          parsedResume.certifications.length > 0 && (

          <div>

            <h3 className="font-semibold">
              Certifications
            </h3>

            <ul className="list-disc ml-5">

              {parsedResume.certifications.map(
                (cert, index) => (

                  <li key={index}>
                    {cert}
                  </li>

                )
              )}

            </ul>

          </div>

        )}



        {/* Technologies */}
        {parsedResume.technologies &&
          parsedResume.technologies.length > 0 && (

          <div>

            <h3 className="font-semibold">
              Technologies
            </h3>


            <p className="text-sm">
              {parsedResume.technologies.join(", ")}
            </p>

          </div>

        )}



        {/* Languages */}
        {parsedResume.languages &&
          parsedResume.languages.length > 0 && (

          <div>

            <h3 className="font-semibold">
              Languages
            </h3>


            <p className="text-sm">
              {parsedResume.languages.join(", ")}
            </p>

          </div>

        )}

      </CardContent>

    </Card>
  );
}