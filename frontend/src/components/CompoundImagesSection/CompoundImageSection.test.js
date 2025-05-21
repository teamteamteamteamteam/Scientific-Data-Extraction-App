import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import CompoundImagesSection from './CompoundImagesSection';

jest.mock('../ImageModal/ImageModal', () => ({ imageType, compoundData, onClose }) => (
    <div data-testid="image-modal">
        <span>{imageType}</span>
        <button onClick={onClose}>Close</button>
    </div>
));

const mockCompoundData = {
    name: 'compoundX',
    concentration: '10',
};

describe('CompoundImagesSection', () => {
    it('renders image labels and loaders for all image types', () => {
        render(<CompoundImagesSection compoundData={mockCompoundData} />);

        ['DAPI', 'ACTIN', 'TUBULIN'].forEach((label) => {
            expect(screen.getByText(label)).toBeInTheDocument();
        });

        const loaders = screen.getAllByText('Loading...');
        expect(loaders.length).toBe(3);
    });

    it('displays images after load and hides loader', async () => {
        render(<CompoundImagesSection compoundData={mockCompoundData} />);

        const images = ['dapi', 'actin', 'tubulin'].map((type) =>
            screen.getByAltText(type)
        );
        images.forEach((img) => {
            fireEvent.load(img);
        });

        await waitFor(() => {
            images.forEach((img) => {
                expect(img.style.display).toBe('block');
            });

            const loaders = screen.queryAllByText('Loading...');
            expect(loaders.length).toBe(0);
        });
    });

    it('opens modal when image is clicked', () => {
        render(<CompoundImagesSection compoundData={mockCompoundData} />);

        const image = screen.getByAltText('dapi');
        fireEvent.load(image);
        fireEvent.click(image);

        expect(screen.getByTestId('image-modal')).toBeInTheDocument();
    });

    it('closes modal when onClose is called', async () => {
        render(<CompoundImagesSection compoundData={mockCompoundData} />);

        const image = screen.getByAltText('dapi');
        fireEvent.load(image);
        fireEvent.click(image);

        const closeBtn = screen.getByText('Close');
        fireEvent.click(closeBtn);

        await waitFor(() => {
            expect(screen.queryByTestId('image-modal')).not.toBeInTheDocument();
        });
    });
});
