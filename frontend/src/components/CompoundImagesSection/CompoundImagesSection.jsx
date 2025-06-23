import React, { useState, useEffect } from 'react';
import './CompoundImagesSection.css';
import ImageModal from '../ImageModal/ImageModal';

function CompoundImagesSection({ compoundData }) {
    const [selectedImage, setSelectedImage] = useState(null);
    const [loadedImages, setLoadedImages] = useState({});

    if (!compoundData) return null;

    const imageTypes = ['dapi', 'actin', 'tubulin'];

    const handleImageLoad = (type) => {
        setLoadedImages(prev => ({ ...prev, [type]: true }));
    };

    useEffect(() => {
        setLoadedImages({});
    }, [compoundData]);

    return (
        <div className="compound-images">
            <h3>Images</h3>
            <div className="image-thumbnails">
                {imageTypes.map((type) => {
          const imageUrl = `http://127.0.0.1:8888/images/png/${type}/${compoundData.name}/${compoundData.concentration}`;
                    return (
                        <div className="image-wrapper" key={type}>
                            {!loadedImages[type] && <div className="loader">Loading...</div>}
                            <img
                                src={imageUrl}
                                alt={type}
                                onClick={() => setSelectedImage(type)}
                                onLoad={() => handleImageLoad(type)}
                                style={{ display: loadedImages[type] ? 'block' : 'none' }}
                                className="thumbnail"
                            />
                            <div className="image-label">{type.toUpperCase()}</div>
                        </div>
                    );
                })}
            </div>
            {selectedImage && (
                <ImageModal
                    imageType={selectedImage}
                    compoundData={compoundData}
                    onClose={() => setSelectedImage(null)}
                />
            )}
        </div>
    );
}

export default CompoundImagesSection;
