import type { GradeResult, ModuleDetail, ModuleSummary, Progress, Question } from '../types/content';

const API_BASE = '';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(init?.headers ?? {}) },
    ...init
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  modules: () => request<ModuleSummary[]>('/api/modules'),
  module: (id: string) => request<ModuleDetail>(`/api/modules/${id}`),
  lesson: (id: string) => request<{ module_id: string; lesson: ModuleDetail['lessons'][number]; questions: Question[] }>(`/api/lessons/${id}`),
  completeLesson: (moduleId: string, lessonId: string) => request<{ ok: boolean }>('/api/lessons/complete', { method: 'POST', body: JSON.stringify({ module_id: moduleId, lesson_id: lessonId }) }),
  quiz: (moduleIds: string[], count: number) => request<{ questions: Question[] }>(`/api/quiz?count=${count}&module_ids=${moduleIds.join(',')}`),
  attempt: (moduleId: string, questionId: string, answer: unknown, responseTimeMs = 0) => request<GradeResult>('/api/attempts', { method: 'POST', body: JSON.stringify({ module_id: moduleId, question_id: questionId, answer, response_time_ms: responseTimeMs }) }),
  progress: () => request<Progress>('/api/progress'),
  weak: () => request<{ questions: Question[] }>('/api/review/weak'),
  runCode: (moduleId: string, challengeId: string, code: string) => request<{ passed: boolean; tests: unknown[]; stderr?: string; error?: string; timeout?: boolean }>('/api/coding/run', { method: 'POST', body: JSON.stringify({ module_id: moduleId, challenge_id: challengeId, code }) }),
  interview: (count: number) => request<{ session_id: string; duration_seconds: number; questions: Question[] }>(`/api/interview/session?count=${count}`),
  submitInterview: (sessionId: string, answers: { module_id: string; question_id: string; answer: unknown; response_time_ms: number }[]) => request<{ score: number; results: unknown[]; breakdown: Record<string, { correct: number; total: number }> }>(`/api/interview/session/${sessionId}/submit`, { method: 'POST', body: JSON.stringify({ answers }) }),
  submitBoss: (moduleId: string, answers: { module_id: string; question_id: string; answer: unknown; response_time_ms: number }[]) => request<{ score: number; passed: boolean; results: unknown[] }>(`/api/modules/${moduleId}/boss-battle/submit`, { method: 'POST', body: JSON.stringify({ answers }) }),
  reset: () => request<{ ok: boolean }>('/api/progress/reset', { method: 'POST' })
};
