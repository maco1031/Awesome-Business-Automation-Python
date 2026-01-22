import { Composition, getInputProps } from 'remotion';
import { MyComposition } from './Composition';
import './style.css';

// Default props that can be overridden by input.json
const defaultProps = {
    text: 'Welcome to\nBusiness Automation',
    titleColor: '#333333',
    bgColor: '#ffffff',
    durationInFrames: 150, // 5 seconds at 30fps
};

export const RemotionRoot: React.FC = () => {
    // Merge input props with defaults
    const inputProps = { ...defaultProps, ...getInputProps() };

    return (
        <>
            <Composition
                id="HelloWorld"
                component={MyComposition}
                durationInFrames={inputProps.durationInFrames}
                fps={30}
                width={1920}
                height={1080}
                defaultProps={defaultProps}
            />
            <Composition
                id="HelloWorldVertical"
                component={MyComposition}
                durationInFrames={inputProps.durationInFrames}
                fps={30}
                width={1080}
                height={1920}
                defaultProps={defaultProps}
            />
        </>
    );
};
