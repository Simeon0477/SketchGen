import "./Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
        <span className="logo">Sketch<em>Gen</em></span>
        <div className="nav-links">
            <a href="#images">Image</a>
            <a href="#videos">Vidéo</a>
        </div>
    </nav>
  );
}

export default Navbar;