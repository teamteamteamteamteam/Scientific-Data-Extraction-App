import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import Dashboard from "./Dashboard";

jest.mock("../../components/ScatterPlot/ScatterPlot", () => (props) => (
  <div data-testid="scatter-plot" onClick={() => props.onClick({ name: "Compound1", concentration: 10 })}>
    ScatterPlot Component
  </div>
));

jest.mock("../../components/CompoundDetails/CompoundDetails", () => (props) => (
  <div data-testid="compound-details">
    {props.compoundData ? 
        `Details: ${props.compoundData.name}, ${props.compoundData.moa}, ${props.compoundData.smiles}, ${props.compoundData.moa_concentration}` 
    :
        "No Data"
    }
  </div>
));

describe("Dashboard Component", () => {
  beforeEach(() => {
    global.fetch = jest.fn();
    jest.spyOn(console, "error").mockImplementation(() => {});
  });

  afterEach(() => {
    jest.clearAllMocks();
    console.error.mockRestore();
  });

  test("renders ScatterPlot and CompoundDetails components", () => {
    render(<Dashboard />);

    expect(screen.getByTestId("scatter-plot")).toBeInTheDocument();
    expect(screen.getByTestId("compound-details")).toBeInTheDocument();
  });

  test("handles point click and fetches compound data successfully", async () => {
    const mockData = [{ smiles: "test smiles", moa: "test moa", moa_concentration: "test concentration" }];
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockData,
    });

    render(<Dashboard />);

    fireEvent.click(screen.getByTestId("scatter-plot"));

    expect(global.fetch).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/compound/details/Compound1/10"
    );

    const details = await screen.findByText("Details: Compound1, test moa, test smiles, test concentration");
    expect(details).toBeInTheDocument();
  });

  test("handles API error", async () => {
    fetch.mockRejectedValueOnce(new Error("API Error"));

    render(<Dashboard />);

    fireEvent.click(screen.getByTestId("scatter-plot"));

    const noData = await screen.findByText("No Data");
    expect(noData).toBeInTheDocument();
  });
});
