import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";

import Dashboard from "./pages/Dashboard";
import History from "./pages/History";
import ScanDetails from "./pages/ScanDetails";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/history" element={<History />} />
        <Route path="/history/:id" element={<ScanDetails />} />
      </Routes>
    </BrowserRouter>
  );
}