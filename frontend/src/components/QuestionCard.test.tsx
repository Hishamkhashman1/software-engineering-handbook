import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import { QuestionCard } from './QuestionCard';

describe('QuestionCard', () => {
  it('submits an answer and displays feedback', async () => {
    const onSubmit = vi.fn(async () => ({ correct: true, score: 1, explanation: 'PATCH updates selected fields.', expected: 'PATCH', xp_awarded: 10 }));
    render(<QuestionCard question={{ id: 'q1', type: 'multiple_choice', prompt: 'Choose', options: ['PUT', 'PATCH'], explanation: '', difficulty: 1, tags: ['http'] }} onSubmit={onSubmit} />);
    await userEvent.click(screen.getByLabelText('PATCH'));
    await userEvent.click(screen.getByText('Submit'));
    expect(onSubmit).toHaveBeenCalledWith('PATCH');
    expect(await screen.findByText('Correct')).toBeInTheDocument();
  });
});
