import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ImageModal from './ImageModal';

HTMLCanvasElement.prototype.getContext = jest.fn(() => ({
  drawImage: jest.fn(),
  getImageData: jest.fn(() => ({
    data: new Array(400).fill(0),
    width: 10,
    height: 10,
  })),
  putImageData: jest.fn(),
}));

describe('ImageModal', () => {
  const mockCompoundData = {
    name: 'test-compound',
    concentration: '10',
  };

  const mockOnClose = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders correctly with loading state', () => {
    render(
      <ImageModal
        imageType="actin"
        compoundData={mockCompoundData}
        onClose={mockOnClose}
      />
    );

    expect(screen.getByText('Loading image...')).toBeInTheDocument();
    expect(screen.getByText('ACTIN Image')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'X' })).toBeInTheDocument();
  });

  it('calls onClose when close button is clicked', () => {
    render(
      <ImageModal
        imageType="actin"
        compoundData={mockCompoundData}
        onClose={mockOnClose}
      />
    );

    fireEvent.click(screen.getByRole('button', { name: 'X' }));
    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });

  it('renders RGB controls', () => {
    render(
      <ImageModal
        imageType="actin"
        compoundData={mockCompoundData}
        onClose={mockOnClose}
      />
    );

    expect(screen.getByText('R: 0 - 255')).toBeInTheDocument();
    expect(screen.getByText('G: 0 - 255')).toBeInTheDocument();
    expect(screen.getByText('B: 0 - 255')).toBeInTheDocument();
  });

  it('updates range values when sliders are moved', async () => {
    render(
      <ImageModal
        imageType="actin"
        compoundData={mockCompoundData}
        onClose={mockOnClose}
      />
    );

    const sliders = screen.getAllByRole('slider');

    fireEvent.mouseDown(sliders[0], { clientX: 0 });
    fireEvent.mouseMove(sliders[0], { clientX: 50 });
    fireEvent.mouseUp(sliders[0]);

    await waitFor(() => {
      expect(screen.getByText(/R: \d+ - 255/)).toBeInTheDocument();
    });
  });
});