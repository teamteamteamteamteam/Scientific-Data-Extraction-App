import React, { useState, useEffect } from "react";
import Plot from "react-plotly.js";

const COLOR_BY_CRITERIUM = {
    MOA: 'moa',
    CONCENTRATION: 'concentration'
};

function ScatterPlot() {
    const [colorBy, setColorBy] = useState(COLOR_BY_CRITERIUM.CONCENTRATION)
    const [plotData, setPlotData] = useState();

    const preparePlotData = (rawData) => {
        return [
            {
                x: rawData.map((point) => point.x),
                y: rawData.map((point) => point.y),
                mode: "markers",
                type: "scatter",
                marker: {
                    size: 12,
                    color: rawData.map((point) => `rgb(${point.color.R},${point.color.G},${point.color.B})`)
                },
            },
        ];
    } 

    const handleClick = (event) => {
        const point = event.points[0];
        alert(`Clicked on X=${point.x}, Y=${point.y}`);
    };

    const fetchData = async (colorBy) => {
        const apiURL = `http://127.0.0.1:8000/compounds/colored_by_${colorBy}`
        try {
            const response = await fetch(apiURL);
            const result = await response.json();
            setPlotData(preparePlotData(result));
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    useEffect(() => {
        fetchData(colorBy);
    }, [colorBy]);

    return (
        <>
            <div>
                <label htmlFor="color-criteria">Color by: </label>
                <select
                    id="color-criteria"
                    value={colorBy}
                    onChange={(e) => setColorBy(e.target.value)}
                >
                <option value={COLOR_BY_CRITERIUM.MOA}>MOA</option>
                <option value={COLOR_BY_CRITERIUM.CONCENTRATION}>Concentration</option>
                </select>
            </div>
            <Plot
                data={plotData}
                layout={{
                    title: `Compounds colored by ${colorBy}`,
                    dragmode: "pan",
                    xaxis: { title: "" },
                    yaxis: { title: "" },
                }}
                config={{
                    scrollZoom: true,
                    responsive: true,
                }}
                onClick={handleClick}
            />
        </>
    );
}

export default ScatterPlot;
