import classes from './File.module.css';
import type {ReactNode} from "react";

interface FileProps {
    htmlFor: string;
    children? : ReactNode | undefined;
    className?: string | undefined;
}

const File = (Props: FileProps) => {
    const { htmlFor, children, className } = Props;
    return (
        <>
            <button name={htmlFor} className={`${classes.label} ${className || ''}`}>
                <label htmlFor={htmlFor}></label>
                <input type="file" name={htmlFor} className={classes.input}/>
                {children}
            </button>
        </>
    );
};

export default File;