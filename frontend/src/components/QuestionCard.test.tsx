import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import { QuestionCard } from './QuestionCard';

describe('QuestionCard', () => {
  it('submits an answer and displays feedback', async () => {
    const onSubmit = vi.fn(async () => ({ correct: true, score: 1, explanation: 'PATCH updates selected fields.', expected: 'PATCH', xp_awarded: 10 }));
    render(<QuestionCard question={{
      id: 'q1',
      type: 'multiple_choice',
      prompt: 'Choose',
      options: ['PUT', 'PATCH'],
      explanation: '',
      difficulty: 1,
      tags: ['http'],
      concept_panel: {
        title: 'PATCH vs PUT',
        explanation: 'PATCH updates selected fields. PUT replaces the whole resource.',
        key_takeaways: ['PATCH is partial.', 'PUT is replacement.', 'Method choice is part of the API contract.'],
        practical_example: 'PATCH /users/5 with only an email field changes only that field.',
        interview_insight: 'Interviewers usually ask this concept to evaluate whether you understand API semantics.',
        diagram: {
          type: 'compare',
          title: 'Update semantics',
          columns: [
            { title: 'PUT', items: ['Replace resource'] },
            { title: 'PATCH', items: ['Update selected fields'] }
          ]
        }
      }
    }} onSubmit={onSubmit} />);
    expect(screen.getByText('PATCH vs PUT')).toBeInTheDocument();
    expect(screen.getByText('Update selected fields')).toBeInTheDocument();
    await userEvent.click(screen.getByLabelText('PATCH'));
    await userEvent.click(screen.getByText('Submit'));
    expect(onSubmit).toHaveBeenCalledWith('PATCH');
    expect(await screen.findByText('Correct')).toBeInTheDocument();
  });
});
