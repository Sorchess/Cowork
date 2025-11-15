import {type ReactNode} from 'react';
import classes from './Header.module.css';

interface HeaderProps {
    children?: ReactNode | undefined;
}

const Header = ({ children }: HeaderProps) => {

    return (
        <header className={classes.header}>
            <div className={classes.header__container}>
                {children}
            </div>
        </header>
    );
};

export default Header;