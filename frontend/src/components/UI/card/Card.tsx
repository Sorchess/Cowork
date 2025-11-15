import classes from './Card.module.css';
import type { CSSProperties, ReactNode } from 'react';

interface CardProps {
    children?: ReactNode | undefined;
    className?: string | undefined;
    styles?: CSSProperties | undefined;
}

const Card = (Props: CardProps) => {
    const { children, className, styles } = Props;
    return (
        <div className={`${classes.card} ${className || ''}`} style={styles}>
            {children}
        </div>
    );
};

export default Card;