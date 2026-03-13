

const Home = () => {
    return (
        <>
        <h1>Ola</h1>
            <div id="carouselExample" className="carousel slide">
            <div className="carousel-inner rounded">
                <div className="carousel-item active">
                <img src="/banner1.png" className="d-block" alt="..." max-height="400px" max-width="400px" />
                </div>
                <div className="carousel-item">
                <img src="banner2.webp" className="d-block" alt="..." max-height="400px" max-width="400px" />
                </div>
                <div className="carousel-item">
                <img src="banner3.webp" className="d-block" alt="..." max-height="400px" max-width="400px" />
            </div>
            </div>
            <button className="carousel-control-prev" type="button" data-bs-target="#carouselExample" data-bs-slide="prev">
                <span className="carousel-control-prev-icon" aria-hidden="true"></span>
                <span className="visually-hidden">Previous</span>
            </button>
            <button className="carousel-control-next" type="button" data-bs-target="#carouselExample" data-bs-slide="next">
                <span className="carousel-control-next-icon" aria-hidden="true"></span>
                <span className="visually-hidden">Next</span>
            </button>
            </div>
        </>
    )
}

export default Home