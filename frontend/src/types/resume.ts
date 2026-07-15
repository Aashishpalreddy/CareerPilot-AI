export interface Resume {
  id: number;
  user_id: number;
  title: string;
  original_filename: string;
  file_path?: string;
  created_at: string;
  is_default: boolean;
}

export interface ParsedResume {
  id?: number;
  resume_id?: number;

  summary?: string;

  skills?: string[];

  experience?: {
    title?: string;
    company?: string;
    location?: string;
    start_date?: string;
    end_date?: string;
    description?: string;
  }[];

  education?: {
    institution?: string;
    degree?: string;
    field_of_study?: string;
    start_date?: string;
    end_date?: string;
  }[];

  projects?: {
    name?: string;
    description?: string;
    technologies?: string[];
  }[];

  certifications?: string[];

  technologies?: string[];

  achievements?: string[];

  languages?: string[];

  years_experience?: number;

  raw_text?: string;

  created_at?: string;

  updated_at?: string;
}

export interface ATSScore {
  score: number;

  matched_keywords?: string[];

  missing_keywords?: string[];

  suggestions?: string[];
}