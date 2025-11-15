import './Search.css';
import Card from "../../UI/card/Card.tsx";
import Textarea from "../../UI/textarea/Textarea.tsx";
import Button from "../../UI/button/Button.tsx";
import Input from "../../UI/input/Input.tsx";
import {useRef} from "react";
import useFileUpload from "../../../hooks/useFileUpload.ts";

const Search = () => {
    const fileInputRef = useRef<HTMLInputElement>(null);
    const { file, handleFileChange, resetFile } = useFileUpload();

    const handleClick = (): void => {
        fileInputRef.current?.click();
    }

    return (
        <Card className="search-container">
            <Textarea className="search-container__textarea" placeholder="Enter your prompt here"/>
            <div className="search-container__buttons">
                <Button className="file-btn" htmlFor="prompt-file" onClick={handleClick}>
                    <Input ref={fileInputRef} type="file" styles={{ display: "none" }} onChange={handleFileChange}></Input>
                    <svg className="file-btn__icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
                        <g>
                            <path d="M480,224H288V32c0-17.673-14.327-32-32-32s-32,14.327-32,32v192H32c-17.673,0-32,14.327-32,32s14.327,32,32,32h192v192   c0,17.673,14.327,32,32,32s32-14.327,32-32V288h192c17.673,0,32-14.327,32-32S497.673,224,480,224z"/>
                        </g>
                    </svg>
                </Button>
                <Button className="search-btn" htmlFor="search">
                    <svg className="search-btn__icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="512" height="512">
                        <path
                            d="M23.12,9.91,19.25,6a1,1,0,0,0-1.42,0h0a1,1,0,0,0,0,1.41L21.39,11H1a1,1,0,0,0-1,1H0a1,1,0,0,0,1,1H21.45l-3.62,3.61a1,1,0,0,0,0,1.42h0a1,1,0,0,0,1.42,0l3.87-3.88A3,3,0,0,0,23.12,9.91Z"/>
                    </svg>
                </Button>
            </div>
        </Card>
    );
};

export default Search;