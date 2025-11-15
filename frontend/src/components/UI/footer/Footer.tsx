import classes from './Footer.module.css';
import type { CSSProperties, ReactNode } from 'react';

interface FooterProps {
    children?: ReactNode | undefined;
    className?: string | undefined;
    styles?: CSSProperties | undefined;

}

const Footer = ({children, className, styles}: FooterProps) => {
    return (
        <footer className={`${classes.footer} ${className || ''}`} style={styles}>
            {children}
            <p>Учебный проект, 2025</p>
        </footer>
    );
};

export default Footer;