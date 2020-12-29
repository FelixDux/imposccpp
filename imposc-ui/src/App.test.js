import { render, screen } from '@testing-library/react';
import App from './App';

test('renders app name', () => {
  render(<App />);
  const nameElement = screen.getByText(/Impact Oscillator/i);
  expect(nameElement).toBeInTheDocument();
});
