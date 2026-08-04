export type QuestionType = 'multiple_choice' | 'true_false' | 'short_answer' | 'ordering' | 'scenario' | 'code_output' | 'debugging' | 'multi_select' | 'matching' | 'code_fill' | 'bug_hunt' | 'scenario_choice';

export interface Lesson {
  id: string;
  title: string;
  summary: string;
  explanation: string;
  key_points: string[];
  examples: string[];
  interview_questions: string[];
  difficulty: number;
  tags: string[];
}

export interface DiagramSpec {
  type: 'flow' | 'compare' | 'network' | 'triangle' | 'tree';
  title?: string;
  nodes?: { id?: string; label: string; status?: string }[];
  edges?: { from: string; to: string; label?: string; status?: string }[];
  columns?: { title: string; items: string[] }[];
  points?: { label: string; detail?: string }[];
}

export interface ConceptPanel {
  title: string;
  explanation: string;
  key_takeaways: string[];
  interview_insight: string;
  practical_example: string;
  diagram?: DiagramSpec;
}

export interface Question {
  id: string;
  type: QuestionType;
  prompt: string;
  options?: string[];
  pairs?: { left: string; right: string }[];
  code?: string;
  explanation: string;
  difficulty: number;
  tags: string[];
  concept_panel?: ConceptPanel;
}

export interface CodingChallenge {
  id: string;
  title: string;
  instructions: string;
  starter_code: string;
  function_signature: string;
  visible_tests: { name: string; call: string; expected: unknown }[];
  timeout_seconds: number;
  explanation: string;
  difficulty: number;
  tags: string[];
}

export interface ModuleSummary {
  id: string;
  title: string;
  description: string;
  order: number;
  tags: string[];
  lesson_count: number;
  question_count: number;
  challenge_count: number;
}

export interface ModuleDetail extends Omit<ModuleSummary, 'lesson_count' | 'question_count' | 'challenge_count'> {
  lessons: Lesson[];
  questions: Question[];
  coding_challenges: CodingChallenge[];
  boss_battle: { id: string; title: string; question_ids: string[]; passing_threshold: number; reward_xp: number };
}

export interface Progress {
  total_xp: number;
  level: number;
  current_streak: number;
  best_streak: number;
  accuracy: number;
  average_response_time_ms: number;
  completed_lessons: string[];
  completed_modules: string[];
  module_progress: { module_id: string; title: string; completed_lessons: number; total_lessons: number; completed: boolean }[];
  weakest_topics: { topic: string; mastery: number; module_id: string }[];
  due_reviews: number;
  recent_activity: { question_id: string; module_id: string; correct: boolean; score: number }[];
}

export interface GradeResult {
  correct: boolean;
  score: number;
  explanation: string;
  expected: unknown;
  xp_awarded: number;
}
