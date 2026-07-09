export interface CVSummary {
    characters: number;
    skills_found: string[];
    top_matches: number;
}

export interface CareerAnalysis {
    overall_match?: number;
    strengths?: string[];
    missing_skills?: string[];
    recommendation?: string;
    learning_path?: string[];
    error?: string;
    raw_response?: string;
}

export interface MatchCVResponse {
    cv_summary: CVSummary;
    recommendations: any[];
    career_analysis: CareerAnalysis;
}