import { Link, useLocation } from "react-router-dom";

function Navbar() {
  const location = useLocation();

  return (
    <nav className="bg-gray-900 border-b border-gray-800 px-8 py-4 flex justify-between items-center">

      <h1 className="text-2xl font-bold text-cyan-400">
        🛡️ AegisAI
      </h1>

      <div className="flex gap-6">

        <Link
          to="/"
          className={`${
            location.pathname === "/"
              ? "text-cyan-400"
              : "text-gray-300"
          } hover:text-cyan-400`}
        >
          Dashboard
        </Link>

        <Link
          to="/history"
          className={`${
            location.pathname === "/history"
              ? "text-cyan-400"
              : "text-gray-300"
          } hover:text-cyan-400`}
        >
          History
        </Link>

      </div>

    </nav>
  );
}

export default Navbar;