import { SmilesSvgRenderer } from 'react-ocl';
import "./CompoundDetails.css";
import CompoundImagesSection from '../CompoundImagesSection/CompoundImagesSection';

function CompoundDetails({ compoundData }) {
    return compoundData ? (
        <div className="compound-info">
            <h2>Compound Details</h2>
            <h3>{compoundData.name && compoundData.name.toUpperCase()} {compoundData.concentration}</h3>
            <p><b>Smiles:</b> {compoundData.smiles ? compoundData.smiles : "N/A"}</p>
            <p><b>MOA:</b> {compoundData.moa ? compoundData.moa : "N/A"}</p>
            <p><b>MOA Concentration:</b> {compoundData.moa_concentration ? compoundData.moa_concentration : "N/A"}</p>
            {compoundData.smiles &&
                <div className="smiles-renderer">
                    <SmilesSvgRenderer smiles={compoundData.smiles} />
                </div>
            }
            <CompoundImagesSection compoundData={compoundData} />
        </div>
    )
        : (
            <div className="select-compound">
                Select a compound
            </div>
        )
}

export default CompoundDetails
