import React from "react";
import { render, screen } from "@testing-library/react";
import CompoundDetails from "./CompoundDetails";

jest.mock("react-ocl", () => ({
  SmilesSvgRenderer: ({ smiles }) => (
    <div data-testid="smiles-renderer">Rendered: {smiles}</div>
  ),
}));

describe("CompoundDetails Component", () => {
  test("renders message when no compoundData is provided", () => {
    render(<CompoundDetails compoundData={null} />);

    expect(screen.getByText("Select a compound")).toBeInTheDocument();
  });

  test("renders compound details when compoundData is provided", () => {
    const mockData = {
      name: "Test Compound",
      smiles: "C1=CC=CC=C1",
      moa: "Test MOA",
      moa_concentration: "50",
    };

    render(<CompoundDetails compoundData={mockData} />);

    expect(screen.getByText("Compound Details")).toBeInTheDocument();
    expect(screen.getByText("TEST COMPOUND")).toBeInTheDocument();
    expect(screen.getByText("Smiles:")).toBeInTheDocument();
    expect(screen.getByText("C1=CC=CC=C1")).toBeInTheDocument();
    expect(screen.getByText("MOA:")).toBeInTheDocument();
    expect(screen.getByText("Test MOA")).toBeInTheDocument();
    expect(screen.getByText("MOA Concentration:")).toBeInTheDocument();
    expect(screen.getByText("50")).toBeInTheDocument();
  });

  test("renders N/A for missing fields in compoundData", () => {
    const mockData = {
      name: "Test Compound",
    };

    render(<CompoundDetails compoundData={mockData} />);

    expect(screen.getByText("Smiles:")).toBeInTheDocument();
    expect(screen.getByText("MOA:")).toBeInTheDocument();
    expect(screen.getByText("MOA Concentration:")).toBeInTheDocument();

    const naElements = screen.queryAllByText("N/A");
    expect(naElements).toHaveLength(3);
  });

  test("renders SmilesSvgRenderer when smiles is provided", () => {
    const mockData = {
      name: "Test Compound",
      smiles: "C1=CC=CC=C1",
    };

    render(<CompoundDetails compoundData={mockData} />);

    expect(screen.getByTestId("smiles-renderer")).toHaveTextContent("Rendered: C1=CC=CC=C1");
  });
});
