import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/">Claim List</Link>
        </li>
        <li>
          <Link to="/create">Create Claim</Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
