function CompoundDetails({compoundData}) {

    return (
        <>
            {compoundData ?
                <>
                    <h3>Compound details:</h3>
                    Smiles: {compoundData.smiles} <br/>
                    MOA: {compoundData.moa} <br/>
                    MOA concentration: {compoundData.moa_concentration} <br/>
                </>
                :
                <>Select compound</>
            }
        </>
    )
}

export default CompoundDetails
