import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { Dashboard } from './Dashboard';

describe('Dashboard', () => {
  it('renders progress values from the API', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => ({
      ok: true,
      json: async () => ({
        total_xp: 125,
        level: 2,
        current_streak: 3,
        best_streak: 5,
        accuracy: 0.8,
        average_response_time_ms: 900,
        completed_lessons: [],
        completed_modules: [],
        module_progress: [{ module_id: 'apis', title: 'APIs', completed_lessons: 1, total_lessons: 4, completed: false }],
        weakest_topics: [{ topic: 'pagination', mastery: 30, module_id: 'apis' }],
        due_reviews: 1,
        recent_activity: []
      })
    })));
    render(<Dashboard openModule={() => undefined} />);
    expect(await screen.findByText('125')).toBeInTheDocument();
    expect(screen.getByText('APIs')).toBeInTheDocument();
    expect(screen.getByText('pagination')).toBeInTheDocument();
  });
});
