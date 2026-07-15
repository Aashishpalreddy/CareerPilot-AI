export interface Resume {
  id: number;
  filename: string;
  file_path?: string;
  uploaded_at: string;
  is_default: boolean;
}


export interface ParsedResume {
  id?: number;

  summary?: string;

  skills?: string[];

  experience?: {
    company?: string;
    role?: string;
    duration?: string;
    description?: string;
  }[];

  education?: {
    institution?: string;
    degree?: string;
    year?: string;
  }[];

  projects?: {
    name?: string;
    description?: string;
    technologies?: string[];
  }[];

  certifications?: string[];

  technologies?: string[];

  languages?: string[];
}


export interface ATSScore {
  score: number;

  matched_keywords?: string[];

  missing_keywords?: string[];

  suggestions?: string[];
}