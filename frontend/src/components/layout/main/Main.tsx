import classes from './Main.module.css';
import {type ReactNode} from "react";

interface MainProps {
    children?: ReactNode | undefined;
}

const Main = (Props: MainProps) => {
    const { children } = Props;
    return (
        <main className={classes.main}>
            <div className={classes.main__container}>
                {children}
            </div>
        </main>
    );
};

export default Main;