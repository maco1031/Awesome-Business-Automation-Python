import React from 'react';
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';

export const MyComposition: React.FC<{
    text: string;
    titleColor: string;
    bgColor: string;
}> = ({ text, titleColor, bgColor }) => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    // Animate opacity and scale using spring physics
    const scale = spring({
        fps,
        frame,
        config: {
            damping: 10,
        }
    });

    const lines = text.split('\n');

    return (
        <div
            style={{
                flex: 1,
                textAlign: 'center',
                fontSize: '7em',
                fontFamily: 'Helvetica, Arial, sans-serif',
                fontWeight: 'bold',
                background: bgColor,
                color: titleColor,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
            }}
        >
            <div style={{ transform: `scale(${scale})` }}>
                {lines.map((line, i) => (
                    <div key={i}>{line}</div>
                ))}
            </div>
        </div>
    );
};
