import "./Banner.css";

function Banner() {
    return (
        <header>
            <div className="img-container">
                <img src="/stallone.jpg" alt="banner-img" className="banner-img"/>
            </div>
            <div className="content">
                <h1>Générez des sketchs et des dessins<br/>avec l'IA</h1>
            </div>
        </header>
    );
}

export default Banner;