// ── Job types ─────────────────────────────────────────────────────────

export interface Job {
  id: number;
  user_id: number;
  title: string;
  company: string | null;
  location: string | null;
  source: string | null;
  job_url: string | null;
  raw_text: string;
  created_at: string;
}

export interface ParsedJob {
  id: number;
  job_id: number;
  title: string | null;
  company: string | null;
  location: string | null;
  job_summary: string | null;
  skills: string[] | Record<string, string[]>;
  technologies: string[];
  responsibilities: string[];
  qualifications: string[];
  keywords: string[];
}

export interface JobCreateRequest {
  title: string;
  company?: string;
  location?: string;
  source?: string;
  job_url?: string;
  raw_text: string;
}

// ── Saved Job types ───────────────────────────────────────────────────

export interface SavedJob {
  id: number;
  user_id: number;
  job_id: number;
  resume_id: number;
  match_score: number;
  tailored_resume_text: string | null;
  cover_letter_text: string | null;
  apply_url: string | null;
  auto_apply_eligible: boolean;
  recruiter_links: Record<string, string> | null;
  status: "saved" | "applied" | "dismissed";
  created_at: string;
  applied_at: string | null;
  // Relations (populated when joined)
  job?: Job;
}

// ── Match types ───────────────────────────────────────────────────────

export interface MatchResponse {
  resume_id: number;
  job_id: number;
  match_score: number;
  matched_skills: string[];
  missing_skills: string[];
  recommendations: string[];
}

// ── Tailor types ──────────────────────────────────────────────────────

export interface TailorResponse {
  resume_id: number;
  job_id: number;
  original_match_score: number;
  improved_match_score: number;
  tailored_summary: string;
  tailored_experience: string[];
  tailored_projects: string[];
  ats_keywords: string[];
  tailored_bullets: string[];
  keywords_added: string[];
  keywords_missing: string[];
}

// ── Cover Letter types ────────────────────────────────────────────────

export interface CoverLetterResponse {
  id: number;
  resume_id: number;
  job_id: number;
  company: string;
  position: string;
  content: string;
  docx_filename: string | null;
  pdf_filename: string | null;
  status: string;
  created_at: string;
  download_url: string | null;
}

// ── Keyword Gap types ─────────────────────────────────────────────────

export interface KeywordGapResponse {
  matched_keywords: string[];
  missing_keywords: string[];
  suggestions: string[];
}

// ── ATS Score types ───────────────────────────────────────────────────

export interface ATSScoreResponse {
  score: number;
  strengths: string[];
  weaknesses: string[];
  suggestions: string[];
}

// ── Pipeline types ────────────────────────────────────────────────────

export interface PipelineRunRequest {
  keywords: string[];
  location?: string;
  remote_only?: boolean;
  job_type?: string;
  experience_level?: string;
  work_arrangement?: string;
}
