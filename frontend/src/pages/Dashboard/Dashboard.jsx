import { useState } from "react";
import ScatterPlot from "../../components/ScatterPlot/ScatterPlot";
import CompoundDetails from "../../components/CompoundDetails/CompoundDetails";
import './Dashboard.css';
import FindClosestCompounds from "../../components/FindClosestCompounds/FindClosestCompounds";

function Dashboard() {
    const [selectedCompound, setSelectedCompound] = useState(null);
    const [compoundsSortedByDistance, setCompoundsSortedByDistance] = useState([]);
    const [numberOfClosestCompounds, setNumberOfClosestCompounds] = useState(0);

    const handleFindClosestClick = async (numberOfCompounds) => {
        if (numberOfCompounds <= 0) {
            return;
        }

        setNumberOfClosestCompounds(numberOfCompounds);
        if (selectedCompound && (!compoundsSortedByDistance.length ||
                !isSameCompound(selectedCompound, compoundsSortedByDistance[0]))) {

            const apiURL = `http://127.0.0.1:8000/compound/distances/${selectedCompound.name}/${selectedCompound.concentration}`
            try {
                const response = await fetch(apiURL);
                const result = await response.json();
                setCompoundsSortedByDistance(result);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }
    }

    const handlePointClick = async (point) => {
        if (isSameCompound(selectedCompound, point.customdata)) {
            return;
        }

        setCompoundsSortedByDistance([]);
        setNumberOfClosestCompounds(0);
        const { name, concentration } = point.customdata;
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
                    <ScatterPlot 
                        onClick={handlePointClick} 
                        selectedCompound={selectedCompound}
                        closestCompounds={compoundsSortedByDistance?.slice(0, numberOfClosestCompounds + 1)}
                    />
                </div>
            </div>
            <div className="details-panel">
                <CompoundDetails compoundData={selectedCompound} />
                <FindClosestCompounds onClick={handleFindClosestClick}/>
            </div>
        </div>
    );
}

export const isSameCompound = (compound1, compound2) => 
    compound1?.name === compound2?.name && compound1?.concentration === compound2?.concentration;

export default Dashboard
