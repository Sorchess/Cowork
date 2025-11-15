import classes from './Button.module.css';
import type { ReactNode, CSSProperties } from 'react';

interface ButtonProps {
    htmlFor: string;
    children?: ReactNode | undefined;
    disabled?: boolean | undefined;
    onClick?: (() => void) | undefined;
    className?: string | undefined;
    styles?: CSSProperties | undefined;
}

const Button = (Props: ButtonProps) => {
    const { htmlFor, children, disabled = false, onClick, className, styles } = Props;
    const handleClick = () => {
        if (disabled) return;
        onClick?.();
    }

    return (
        <button type="button" name={htmlFor} id={htmlFor} className={`${classes.btn} ${className || ''}`} onClick={handleClick} style={styles}>
            {children}
        </button>
    );
};

export default Button;