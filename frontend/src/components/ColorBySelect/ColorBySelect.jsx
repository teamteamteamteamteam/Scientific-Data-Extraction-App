import Select from "react-select";
import "./ColorBySelect.css";

const customStyles = {
    control: (base) => ({
        ...base,
        backgroundColor: "#f9f9f9",
        border: "1px solid #ccc",
        boxShadow: "none",
        borderRadius: "4px",
        padding: "2px",
        fontSize: "14px",
        width: "200px",
    }),
    option: (base) => ({
        ...base,
        color: "#333",
        backgroundColor: "#fff",
        "&:hover": {
            backgroundColor: "#f0f0f0",
        },
    }),
};

export const COLOR_BY_CRITERIUM = {
    MOA: "moa",
    CONCENTRATION: "concentration",
};

const options = [
    { value: COLOR_BY_CRITERIUM.MOA, label: "MOA" },
    { value: COLOR_BY_CRITERIUM.CONCENTRATION, label: "Concentration" },
];

function ColorBySelect({ colorBy, onChange }) {
    return <div className="color-by-select">
                <label
                    htmlFor="color-criteria"
                    style={{
                        marginRight: "10px",
                        marginTop: "10px",
                        fontWeight: "bold",
                    }}
                >
                    Color by:
                </label>
                <Select
                    id="color-criteria"
                    options={options}
                    value={options.find((option) => option.value === colorBy)}
                    onChange={onChange}
                    styles={customStyles}
                />
            </div>
}

export default ColorBySelect
