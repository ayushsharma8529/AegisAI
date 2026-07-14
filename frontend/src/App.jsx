import { BrowserRouter, Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import History from "./pages/History";
import Navbar from "./components/Navbar";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/history" element={<History />} />
      </Routes>
    </BrowserRouter>
  );
}