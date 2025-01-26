import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import ScatterPlot from "./ScatterPlot";

jest.mock("../ColorBySelect/ColorBySelect", () => {
    const COLOR_BY_CRITERIUM = {
      CONCENTRATION: "concentration",
      MOA: "moa",
    };
  
    const ColorBySelect = ({ colorBy, onChange }) => (
      <select
        data-testid="color-by-select"
        value={colorBy}
        onChange={(e) => onChange({ value: e.target.value })}
      >
        <option value="concentration">Concentration</option>
        <option value="moa">Moa</option>
      </select>
    );
  
    return { __esModule: true, COLOR_BY_CRITERIUM, default: ColorBySelect };
  });
  
  
jest.mock("react-plotly.js", () => {
    return jest.fn((props) => (
      <div
        data-testid="plotly-mock"
        onClick={() =>
          props.onClick({
            points: [{ customdata: { name: "Compound1", concentration: 10 } }],
          })
        }
      >
        Mocked Plotly
      </div>
    ));
  });  

global.fetch = jest.fn();

describe("ScatterPlot Component", () => {
  beforeEach(() => {
    fetch.mockClear();
    jest.spyOn(console, "error").mockImplementation(() => {});
  });

  afterEach(() => {
    console.error.mockRestore();
  });

  test("renders ColorBySelect and Plotly components", () => {
    render(<ScatterPlot onClick={jest.fn()} />);

    expect(screen.getByTestId("color-by-select")).toBeInTheDocument();
    expect(screen.getByTestId("plotly-mock")).toBeInTheDocument();
  });

  test("fetches data on mount and updates plotData", async () => {
    const mockData = [
      {
        x: 1,
        y: 2,
        color: { R: 255, G: 0, B: 0 },
        name: "Compound1",
        concentration: 10,
      },
    ];
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockData,
    });

    render(<ScatterPlot onClick={jest.fn()} />);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith("http://127.0.0.1:8000/compounds/colored_by_concentration");
    });
  });

  test("updates data when ColorBySelect changes", async () => {
    const mockData = [
      {
        x: 1,
        y: 2,
        color: { R: 0, G: 255, B: 0 },
        name: "Compound2",
        concentration: 20,
      },
    ];
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockData,
    });

    render(<ScatterPlot onClick={jest.fn()} />);

    fireEvent.change(screen.getByTestId("color-by-select"), {
      target: { value: "moa" },
    });

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith("http://127.0.0.1:8000/compounds/colored_by_moa");
    });
  });

  test("calls onClick with correct data when Plotly is clicked", () => {
    const handleClick = jest.fn();
    render(<ScatterPlot onClick={handleClick} />);

    fireEvent.click(screen.getByTestId("plotly-mock"));

    expect(handleClick).toHaveBeenCalledWith({ name: "Compound1", concentration: 10 });
  });
});
