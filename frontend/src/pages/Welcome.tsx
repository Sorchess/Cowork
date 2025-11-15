import Navbar from "../components/UI/navbar/Navbar.tsx";
import Footer from "../components/UI/footer/Footer.tsx";
import Main from '../components/layout/main/Main.tsx'
import Search from "../components/forms/search/Search.tsx";

const Welcome = () => {
    return (
        <>
            <Navbar/>
            <Main>

                <h2>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ad aliquid amet cupiditate dicta
                    eaque eius error, fugiat illo ipsum iure maxime minima molestiae nostrum odio reprehenderit
                    rerum vel velit vero.
                </h2>
                <Search/>

            </Main>
            <Footer/>
        </>
    );
};

export default Welcome;