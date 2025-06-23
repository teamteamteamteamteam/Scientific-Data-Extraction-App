import React, { useState, useEffect, useRef } from 'react';
import './ImageModal.css';
import { Range, getTrackBackground } from 'react-range';

function ImageModal({ imageType, compoundData, onClose }) {
    const [ranges, setRanges] = useState({
        r: [0, 255],
        g: [0, 255],
        b: [0, 255],
    });
    const canvasRef = useRef(null);
    const imageRef = useRef(null);
    const [loading, setLoading] = useState(true);

  const imageURL = `http://127.0.0.1:8888/images/png/${imageType}/${compoundData.name}/${compoundData.concentration}`;

    const updateRange = (channel, newRange) => {
        setRanges(prev => ({ ...prev, [channel]: newRange }));
    };

    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas?.getContext('2d');
        const img = imageRef.current;

        if (!canvas || !ctx || !img) return;

        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;

        const clampAndScale = (val, min, max) => {
            if (val < min) return 0;
            if (val > max) return 255;
            if (max === min) return 0;
            return ((val - min) / (max - min)) * 255;
        };

        for (let i = 0; i < data.length; i += 4) {
            const [minR, maxR] = ranges.r;
            const [minG, maxG] = ranges.g;
            const [minB, maxB] = ranges.b;

            data[i]     = clampAndScale(data[i],     minR, maxR); // R
            data[i + 1] = clampAndScale(data[i + 1], minG, maxG); // G
            data[i + 2] = clampAndScale(data[i + 2], minB, maxB); // B
        }

        ctx.putImageData(imageData, 0, 0);
    }, [ranges]);

    const handleImageLoad = () => {
        const canvas = canvasRef.current;
        const img = imageRef.current;
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;

        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0);

        setLoading(false);
    };

    return (
        <div className="modal-backdrop">
            <div className="modal-content">
                <button className="close-button" onClick={onClose}>X</button>
                <h3>{imageType.toUpperCase()} Image</h3>
                <div className="image-container">
                    <img
                        ref={imageRef}
                        src={imageURL}
                        alt={imageType}
                        crossOrigin="anonymous"
                        onLoad={handleImageLoad}
                        style={{ display: 'none' }}
                        onError={() => setLoading(false)}
                    />
                    {loading && (
                        <div style={{ padding: '20px', fontSize: '18px' }}>Loading image...</div>
                    )}
                    <canvas ref={canvasRef} className="full-image" />
                </div>
                <div className="rgb-controls">
                    {['r', 'g', 'b'].map(channel => (
                        <ChannelRange
                            key={channel}
                            channel={channel}
                            value={ranges[channel]}
                            onChange={updateRange}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
}

const ChannelRange = ({ channel, value, onChange }) => {
    const STEP = 1;
    const MIN = 0;
    const MAX = 255;

    return (
        <div style={{ marginBottom: '20px' }}>
            <label>{channel.toUpperCase()}: {value[0]} - {value[1]}</label>
            <Range
                values={value}
                step={STEP}
                min={MIN}
                max={MAX}
                onChange={(vals) => onChange(channel, vals)}
                renderTrack={({ props, children }) => (
                    <div
                        {...props}
                        style={{
                            ...props.style,
                            height: '6px',
                            width: '100%',
                            background: getTrackBackground({
                                values: value,
                                colors: ['#ccc', '#548BF4', '#ccc'],
                                min: MIN,
                                max: MAX,
                            }),
                            borderRadius: '4px',
                        }}
                    >
                        {children.map((child, index) => (
                            React.cloneElement(child, { key: index })
                        ))}
                    </div>
                )}
                renderThumb={({ props }) => {
                    const { key, ...rest } = props;
                    return (
                        <div
                            {...rest}
                            style={{
                                ...rest.style,
                                height: '16px',
                                width: '16px',
                                borderRadius: '50%',
                                backgroundColor: '#548BF4',
                            }}
                        />
                    );
                }}
            />
        </div>
    );
};

export default ImageModal;
