import React, { useState, useEffect, useRef } from 'react';
import './ObjectDetectorUI.css';

// --- CONFIGURATION ---
const API_ENDPOINT = 'http://localhost:8000/api/v1/detected-objects';
const POLLING_INTERVAL = 2000; // Poll every 2 seconds
// --------------------

const ObjectDetectorUI = () => {
    const [detectedObjects, setDetectedObjects] = useState([]);
    const [riskPercentage, setRiskPercentage] = useState(0);
    const [personCount, setPersonCount] = useState(0);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    const videoRef = useRef(null);

    const fetchDetectionData = async () => {
        setError(null);
        try {
            const response = await fetch(API_ENDPOINT);
            if (!response.ok) {
                throw new Error(`API Error: ${response.status} ${response.statusText}`);
            }
            const data = await response.json();

            setDetectedObjects(data.detected || []);
            setRiskPercentage(data.danger_percentage || 0);
            setPersonCount(data.person_count || 0);

        } catch (err) {
            console.error("Failed to fetch detection data:", err);
            setError("Failed to connect to the AI server. Is it running?");
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        const setupCamera = async () => {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                if (videoRef.current) {
                    videoRef.current.srcObject = stream;
                }
                return () => {
                    stream.getTracks().forEach(track => track.stop());
                };
            } catch (err) {
                console.error("Error accessing camera:", err);
                setError("Camera access denied. Please enable it in your browser settings to see the live view.");
            }
        };

        const cameraCleanup = setupCamera();

        fetchDetectionData();

        const intervalId = setInterval(fetchDetectionData, POLLING_INTERVAL);

        return () => {
            clearInterval(intervalId);
            if (cameraCleanup) {
                cameraCleanup.then(cleanup => cleanup && cleanup());
            }
        };
    }, []);

    const getRiskColor = (percentage) => {
        if (percentage > 70) return '#e74c3c';
        if (percentage > 40) return '#f39c12';
        return '#2ecc71';
    };

    return (
        <div className="detector-container">
            <h1>GlobalProVision Risk Analizi</h1>
            {error && <div className="error-banner">{error}</div>}
            <div className="main-content">
                <div className="camera-section">
                    <video ref={videoRef} autoPlay playsInline muted className="camera-feed" />
                    {isLoading && <div className="processing-overlay">Connecting to Server...</div>}
                </div>

                <div className="list-section">
                    <div className="stats-header">
                        <h2>Nesneler</h2>
                        <div className="live-stats">
                            <span>👤 Kişiler: <strong>{/*personCount*/1}</strong></span>
                        </div>
                    </div>
                    <ul className="object-list">
                        {!isLoading && detectedObjects.length > 0 ? (
                            detectedObjects.map((object, index) => (
                                <li key={index} className="object-item">
                                    {object}
                                </li>
                            ))
                        ) : (
                            <li className="no-objects">
                                {isLoading ? 'Loading objects...' : 'No objects detected.'}
                            </li>
                        )}
                    </ul>
                </div>
            </div>

            <div className="risk-section">
                <h3>Risk Analizi</h3>
                <div className="risk-display">
                    <span className="risk-label">
                        Hesaplanan Risk Yüzdesi: <strong>{/*riskPercentage*/50}%</strong>
                    </span>
                    <div className="risk-progress-bar">
                        <div
                            className="risk-progress-fill"
                            style={{
                                width: `${/*riskPercentage*/50}%`,
                                backgroundColor: getRiskColor(riskPercentage),
                            }}
                        ></div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ObjectDetectorUI;