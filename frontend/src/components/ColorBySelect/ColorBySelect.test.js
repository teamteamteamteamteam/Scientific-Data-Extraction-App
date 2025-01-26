import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import ColorBySelect, { COLOR_BY_CRITERIUM } from "./ColorBySelect";

describe("ColorBySelect Component", () => {
  test("renders the label and select dropdown", () => {
    render(<ColorBySelect colorBy={COLOR_BY_CRITERIUM.MOA} onChange={jest.fn()} />);

    expect(screen.getByText("Color by:")).toBeInTheDocument();

    expect(screen.getByRole("combobox")).toBeInTheDocument();
  });

  test("sets the correct default value based on the 'colorBy' prop", () => {
    render(<ColorBySelect colorBy={COLOR_BY_CRITERIUM.CONCENTRATION} onChange={jest.fn()} />);

    expect(screen.getByText("Concentration")).toBeInTheDocument();
  });

  test("calls onChange when a new option is selected", () => {
    let onChangeCalled = false;
    const handleChange = (value) => { 
        expect(value == COLOR_BY_CRITERIUM.CONCENTRATION);
        onChangeCalled = true
    }

    render(<ColorBySelect colorBy={COLOR_BY_CRITERIUM.MOA} onChange={handleChange} />);

    const dropdown = screen.getByRole("combobox");

    fireEvent.change(dropdown, { target: { value: COLOR_BY_CRITERIUM.CONCENTRATION } });

    expect(onChangeCalled);
  });
});
