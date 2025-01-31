import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import ClaimForm from "./components/ClaimForm";
import ClaimList from "./components/ClaimList";
import ClaimsList from "./components/ClaimsList";


function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<ClaimList />} />
          <Route path="/create" element={<ClaimForm />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
