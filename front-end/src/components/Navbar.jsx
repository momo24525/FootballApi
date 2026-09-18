import { useState } from "react";
import { Link } from "react-router-dom";
import "./Navbar.css";

const LINKS = [
    { label: "Partite", to: "/matches" },
    { label: "Head to head", to: "/h2h" },
    { label: "Stagioni", to: "/seasons" },
    { label: "Classifica", to: "/standings" },
];

function NavBar() {
    const [open, setOpen] = useState(false);

    return (
        <nav className="navbar">
            <div className="navbar-inner">
                

                <button
                    className="navbar-toggle"
                    onClick={() => setOpen((prev) => !prev)}
                    aria-label="Apri il menu"
                    aria-expanded={open}
                >
                    <span />
                    <span />
                    <span />
                </button>

                <Link className="navbar-brand" to="/matches">
                    <span className="navbar-brand-mark">⚽</span>
                    Serie A Tracker
                </Link>

                <ul className={`navbar-links ${open ? "navbar-links-open" : ""}`}>
                    {LINKS.map((link) => (
                        <li key={link.label}>
                            <Link to={link.to} onClick={() => setOpen(false)}>
                                {link.label}
                            </Link>
                        </li>
                    ))}
                </ul>
            </div>
        </nav>
    );
}

export default NavBar;