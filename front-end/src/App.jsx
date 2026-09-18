import { BrowserRouter, Routes, Route } from "react-router-dom";
import NavBar from "./components/Navbar";
import MainTable from "./pages/MainTable";
import H2hTable from "./pages/h2hTable";

function App() {
    return (
        <BrowserRouter>
            <NavBar />

            <Routes>
                <Route path="/matches" element={<MainTable />} />
                <Route path="/h2h" element={<H2hTable />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;