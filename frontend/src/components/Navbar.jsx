import { Link } from "react-router-dom";

const Navbar = () => {
    const navLinkClass = "px-3 py-2 rounded hover:bg-gray-200";
    return (
        <>
            <h1 className="pl-6 pt-6 pb-6 text-5xl font-bold">
                CP Analytics
            </h1>

            <nav className="flex gap-4 pl-6 pb-6">
                <Link to="/contests" className={navLinkClass}>Contests</Link>
                <Link to="/dashboard" className={navLinkClass}>Dashboard</Link>
                <Link to="/daily-activity" className={navLinkClass}>Daily Activity</Link>
                <Link to="/tags" className={navLinkClass}>Tags</Link>
                <Link to="/recommendations" className={navLinkClass}>Recommendations</Link>
                <Link to="/tags/weakest" className={navLinkClass}>Weakest Tags</Link>
                <Link to="/upsolve" className={navLinkClass}>Upsolves</Link>
            </nav>
        </>
    );
};

export default Navbar;