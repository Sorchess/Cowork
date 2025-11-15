import classes from './Input.module.css';
import type {ChangeEvent, CSSProperties, Ref} from "react";

interface InputProps {
    type: string;
    styles?: CSSProperties | undefined;
    className?: string | undefined;
    placeholder?: string | undefined;
    ref?: Ref<HTMLInputElement> | undefined;
    onChange?: ((event:ChangeEvent<HTMLInputElement>) => void) | undefined;
}

const Input = (Props: InputProps) => {
    const { type, styles, className, placeholder, ref, onChange } = Props;
    return (
        <input ref={ref} type={type} style={styles} onChange={onChange}
               placeholder={`${placeholder || ''}`} className={`${classes.input} ${className || ''}`}/>
    );
};

export default Input;