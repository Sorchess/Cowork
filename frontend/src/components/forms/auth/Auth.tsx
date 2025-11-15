import Button from "../../UI/button/Button.tsx";
import Card from "../../UI/card/Card.tsx";
import Input from "../../UI/input/Input.tsx";
import {Link, useNavigate} from "react-router";
import Footer from "../../UI/footer/Footer.tsx";
import './Auth.css';
import {useState} from "react";
import Logo from "../../UI/logo/Logo.tsx";

const AuthForm = () => {
    const [userCreated, setUserCreated] = useState(true);
    const navigate = useNavigate();
    return (
        <>
            <Button htmlFor="back" className="auth-back-btn" onClick={() => navigate('/')}>
                <svg className="auth-back-btn-icon" xmlns="http://www.w3.org/2000/svg" id="Outline" viewBox="0 0 24 24" width="512" height="512">
                    <path
                        d="M23.12,9.91,19.25,6a1,1,0,0,0-1.42,0h0a1,1,0,0,0,0,1.41L21.39,11H1a1,1,0,0,0-1,1H0a1,1,0,0,0,1,1H21.45l-3.62,3.61a1,1,0,0,0,0,1.42h0a1,1,0,0,0,1.42,0l3.87-3.88A3,3,0,0,0,23.12,9.91Z"/>
                </svg>
                <label className="auth-back-btn-text" htmlFor="back">На главную</label>
            </Button>
            {userCreated
                ?
                <Card className="auth-card">
                    <form className="auth-form">
                        <Logo styles={{ position: "absolute", top: "50px" }} />

                        <div className="auth-form-buttons">
                            <Button className={`${userCreated ? ' active' : ''}`} htmlFor="sign-in"
                                    onClick={() => setUserCreated(true)}>Вход</Button>
                            <Button className={`${userCreated ? '' : 'active'}`} htmlFor="sign-up"
                                    onClick={() => setUserCreated(false)}>Регистрация</Button>
                        </div>
                        Электронная почта
                        <Input type="text" placeholder="Электронная почта"/>
                        Пароль
                        <Input type="text" placeholder="Пароль"/>
                        <div className="auth-form-forgot-password">
                            Забыли пароль?
                            <Link style={{ textDecoration: "none", color: "var(--link-text-color)" }} to="/recover">Восстановить</Link>
                        </div>
                        <Button className="auth-form-login" htmlFor="auth">Войти</Button>

                    </form>
                </Card>
                :
                <Card className="auth-card">
                    <form className="auth-form">
                        <Logo styles={{ position: "absolute", top: "50px" }} />
                        <div className="auth-form-buttons">
                            <Button className={`${userCreated ? ' active' : ''}`} htmlFor="sign-in"
                                    onClick={() => setUserCreated(true)}>Вход</Button>
                            <Button className={`${userCreated ? '' : 'active'}`} htmlFor="sign-up"
                                    onClick={() => setUserCreated(false)}>Регистрация</Button>
                        </div>
                        Электронная почта
                        <Input type="text" placeholder="Электронная почта"/>
                        Пароль
                        <Input type="text" placeholder="Пароль"/>
                        <Button className="auth-form-register" htmlFor="register">Зарегистрироваться</Button>

                    </form>
                </Card>}
            <Footer className="auth-card-footer"></Footer>

        </>
    );
};

export default AuthForm;