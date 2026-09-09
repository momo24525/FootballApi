import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import MainTable from "./pages/MainTable";

function App() {
    return (
        <BrowserRouter>
            <nav>
                <Link to="/matches">Match</Link> 
            </nav>

            <Routes>
                <Route path="/matches" element={<MainTable />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;