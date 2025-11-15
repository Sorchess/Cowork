import {Link} from "react-router";
import classes from './Logo.module.css';
import {type CSSProperties, useContext} from "react";
import {ThemeContext} from "../../../contexts/ThemeContext.tsx";

interface LogoProps {
    className?: string | undefined;
    styles?: CSSProperties | undefined;
}

const Logo = (Props: LogoProps) => {
    const { className, styles } = Props;
    const { isDark } = useContext(ThemeContext);
    return (
        <Link key="logo" className={`${classes.logo} ${className || ''}`} style={styles} to='/'>
            {/*<img style={{ paddingTop: "2px"}} src={isDark ? '' : ''} alt="Логотип"/>*/}
            <label className={classes.label} htmlFor="logo">Project-AI</label>
        </Link>
    );
};

export default Logo;