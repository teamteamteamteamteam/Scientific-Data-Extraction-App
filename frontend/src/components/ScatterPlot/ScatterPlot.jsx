import React, { useState, useEffect } from "react";
import Plot from "react-plotly.js";
import ColorBySelect, { COLOR_BY_CRITERIUM } from "../ColorBySelect/ColorBySelect";
import "./ScatterPlot.css";

const preparePlotData = (rawData) => {
    return [
        {
            x: rawData.map((point) => point.x),
            y: rawData.map((point) => point.y),
            mode: "markers",
            type: "scatter",
            marker: {
                size: 12,
                color: rawData.map(
                    (point) =>
                        `rgb(${point.color.R},${point.color.G},${point.color.B})`
                ),
            },
            text: rawData.map((point) => point.name),
            customdata: rawData.map((point) => ({
                concentration: point.concentration,
                name: point.name,
            })),
            hoverinfo: "text",
        },
    ];
};

function ScatterPlot({ onClick }) {
    const [colorBy, setColorBy] = useState(COLOR_BY_CRITERIUM.CONCENTRATION);
    const [plotData, setPlotData] = useState();

    const fetchData = async (colorBy) => {
        const apiURL = `http://127.0.0.1:8000/compounds/colored_by_${colorBy}`;
        try {
            const response = await fetch(apiURL);
            const result = await response.json();
            setPlotData(preparePlotData(result));
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    useEffect(() => {
        fetchData(colorBy);
    }, [colorBy]);

    return (
        <>
            <ColorBySelect 
                colorBy={colorBy}
                onChange={(selectedOption) => setColorBy(selectedOption.value)}
            />
            <div className="plotly-container">
                <Plot
                    data={plotData}
                    layout={{
                        title: `Compounds colored by ${colorBy}`,
                        dragmode: "pan",
                        xaxis: { title: "" },
                        yaxis: { title: "" },
                        autosize: true,
                    }}
                    useResizeHandler={true}
                    style={{ width: "100%", height: "100%" }}
                    config={{
                        scrollZoom: true,
                    }}
                    onClick={(e) => onClick(e.points[0].customdata)}
                />
            </div>
        </>
    );
}

export default ScatterPlot;
