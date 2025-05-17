import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import FindClosestCompounds from "./FindClosestCompounds";

describe("FindClosestCompounds component", () => {
  test("renders title, input and button", () => {
    render(<FindClosestCompounds onClick={() => {}} />);
    
    expect(screen.getByText(/Find Closest Compounds/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Enter a number/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /find/i })).toBeInTheDocument();
  });

  test("calls onClick with correct number when button is clicked", () => {
    const mockOnClick = jest.fn();
    render(<FindClosestCompounds onClick={mockOnClick} />);
    
    const input = screen.getByPlaceholderText(/Enter a number/i);
    fireEvent.change(input, { target: { value: "5" } });

    fireEvent.click(screen.getByRole("button", { name: /find/i }));

    expect(mockOnClick).toHaveBeenCalledWith(5);
  });

  test("does not allow negative values", () => {
    render(<FindClosestCompounds onClick={() => {}} />);
    
    const input = screen.getByPlaceholderText(/Enter a number/i);
    expect(input).toHaveAttribute("min", "0");
  });
});
