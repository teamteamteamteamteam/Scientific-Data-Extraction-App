import { useState } from "react";
import ScatterPlot from "../../components/ScatterPlot/ScatterPlot";
import CompoundDetails from "../../components/CompoundDetails/CompoundDetails";

function Dashboard() {
    const [selectedCompound, setSelectedCompound] = useState(null);

    const handlePointClick = async ({name, concentration}) => {
        const apiURL = `http://127.0.0.1:8000/compound/details/${name}/${concentration}`
        try {
            const response = await fetch(apiURL);
            const result = await response.json();
            setSelectedCompound(result[0]);
        } catch (error) {
            console.error('Error fetching data:', error);
            setSelectedCompound(null);
        }
    }

    return (
        <>
            <ScatterPlot onClick={handlePointClick}/>
            <CompoundDetails compoundData={selectedCompound} />
        </>
    )
}

export default Dashboard
