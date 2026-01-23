import React from 'react';
import { useCurrentFrame } from 'remotion';

export const TerminalComposition: React.FC<{
    text: string;
    bgColor: string;
    titleColor: string; // Used for text color
}> = ({ text, bgColor, titleColor }) => {
    const frame = useCurrentFrame();

    // Typing speed: 2 characters per frame (adjust as needed)
    const charsShown = Math.floor(frame * 1.5);
    const textToShow = text.slice(0, charsShown);

    // Cursor blinking every 15 frames
    const cursorVisible = Math.floor(frame / 15) % 2 === 0;

    return (
        <div
            style={{
                flex: 1,
                fontSize: '2.5em', // Smaller font for terminal
                fontFamily: "'Consolas', 'Monaco', 'Courier New', monospace",
                fontWeight: 'bold',
                background: '#1e1e1e', // Force dark terminal bg
                color: '#33ff00', // Classic hacker green or configurable
                padding: '40px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'flex-start', // Top align
                alignItems: 'flex-start', // Left align
                whiteSpace: 'pre-wrap', // Preserve newlines
                overflow: 'hidden',
                lineHeight: '1.4',
            }}
        >
            <div>
                {textToShow}
                <span style={{
                    opacity: cursorVisible ? 1 : 0,
                    display: 'inline-block',
                    width: '0.6em',
                    height: '1em',
                    backgroundColor: '#33ff00',
                    marginLeft: '5px',
                    verticalAlign: 'middle'
                }} />
            </div>
        </div>
    );
};
