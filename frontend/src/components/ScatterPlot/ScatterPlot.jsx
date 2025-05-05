import React, { useState, useEffect, memo, useRef } from "react";
import Plot from "react-plotly.js";
import ColorBySelect, { COLOR_BY_CRITERIUM } from "../ColorBySelect/ColorBySelect";
import "./ScatterPlot.css";
import { isSameCompound } from "../../pages/Dashboard/Dashboard";

const ScatterPlot = memo(function ScatterPlot({ onClick, selectedCompound, closestCompounds }) {
    const [colorBy, setColorBy] = useState(COLOR_BY_CRITERIUM.CONCENTRATION);
    const [rawData, setRawData] = useState([]);
    const [plotData, setPlotData] = useState([]);
    const [layout, setLayout] = useState({
        title: `Compounds colored by ${colorBy}`,
        dragmode: "pan",
        xaxis: { title: "" },
        yaxis: { title: "" },
        autosize: true,
    });
    const plotRef = useRef(null);

    const fetchData = async (colorBy) => {
        const apiURL = `http://127.0.0.1:8000/compounds/colored_by_${colorBy}`;
        try {
            const response = await fetch(apiURL);
            const result = await response.json();
            setRawData(result);
            setPlotData(preparePlotData(result, selectedCompound, closestCompounds));
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    useEffect(() => {
        fetchData(colorBy);
        setLayout(current => ({
            ...current,
            title: `Compounds colored by ${colorBy}`,
        }));
    }, [colorBy]);

    useEffect(() => {
        setPlotData(preparePlotData(rawData, selectedCompound, closestCompounds));
    }, [selectedCompound, closestCompounds]);

    const handlePlotClick = (e) => {
        if (e.points && e.points.length > 0) {
            onClick(e.points[0]);
        }
    };

    const onRelayout = (newLayout) => {
        setLayout(current => ({
            ...current,
            xaxis: newLayout['xaxis'] || current.xaxis,
            yaxis: newLayout['yaxis'] || current.yaxis
        }));
    };

    return (
        <>
            <ColorBySelect 
                colorBy={colorBy}
                onChange={(selectedOption) => setColorBy(selectedOption.value)}
            />
            <div className="plotly-container">
                <Plot
                    ref={plotRef}
                    data={plotData}
                    layout={layout}
                    useResizeHandler={true}
                    style={{ width: "100%", height: "100%" }}
                    config={{
                        scrollZoom: true,
                    }}
                    onClick={handlePlotClick}
                    onRelayout={onRelayout}
                />
            </div>
        </>
    );
});


const preparePlotData = (rawData, selectedCompound, closestCompounds) => {
    const closestCompoundsSet = new Set(
        closestCompounds.map(c => `${c.name}|${c.concentration}`)
    );

    const getPointSize = (point) => {
        return isSameCompound(point, selectedCompound) 
            ? 24
            : closestCompoundsSet.has(`${point.name}|${point.concentration}`)
                ? 16
                : 12;
    }

    const getPointBorderWidth = (point) => {
        return isSameCompound(point, selectedCompound)
            ? 4
            : closestCompoundsSet.has(`${point.name}|${point.concentration}`)
                ? 2
                : 0;
    }

    return [
        {
            x: rawData.map((point) => point.x),
            y: rawData.map((point) => point.y),
            mode: "markers",
            type: "scatter",
            marker: {
                size: rawData.map(getPointSize),
                color: rawData.map(
                    (point) =>
                        `rgb(${point.color.R},${point.color.G},${point.color.B})`
                ),
                opacity: 1,
                line: {
                    color: "black",
                    width: rawData.map(getPointBorderWidth),
                }
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

export default ScatterPlot;