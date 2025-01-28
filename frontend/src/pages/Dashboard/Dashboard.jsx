import { useState } from "react";
import ScatterPlot from "../../components/ScatterPlot/ScatterPlot";
import CompoundDetails from "../../components/CompoundDetails/CompoundDetails";
import './Dashboard.css';

function Dashboard() {
    const [selectedCompound, setSelectedCompound] = useState(null);

    const handlePointClick = async ({ name, concentration }) => {
        const apiURL = `http://127.0.0.1:8000/compound/details/${name}/${concentration}`
        try {
            const response = await fetch(apiURL);
            const result = await response.json();
            setSelectedCompound({
                ...result[0],
                name: name,
                concentration: concentration
            });
        } catch (error) {
            console.error('Error fetching data:', error);
            setSelectedCompound(null);
        }
    }

    return (
        <div className="dashboard-container">
            <div className="scatter-plot-container">
                <div className="control-panel">
                    <ScatterPlot onClick={handlePointClick} />
                </div>
            </div>
            <div className="details-panel">
                <CompoundDetails compoundData={selectedCompound} />
            </div>
        </div>
    );
}

export default Dashboard
