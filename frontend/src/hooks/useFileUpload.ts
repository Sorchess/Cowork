import {type ChangeEvent, useState} from "react";

interface UseFileUploadReturn {
    file: File | null;
    handleFileChange: (event: ChangeEvent<HTMLInputElement>) => void;
    resetFile: () => void;
}

const useFileUpload = (): UseFileUploadReturn => {
    const [file, setFile] = useState<File | null>(null);

    const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
        const fileList: FileList | null = event.target.files;
        if (!fileList || fileList.length === 0) {
            console.log('Файлы не выбраны');
            return;
        }

        const filesArray = new Array(fileList);
        filesArray.forEach((file, index) => {
            console.log(`Файл ${index + 1}:`, file);
        });
    }

    const resetFile = () => {
        setFile(null);
    }

    return { file, handleFileChange, resetFile };
};

export default useFileUpload;