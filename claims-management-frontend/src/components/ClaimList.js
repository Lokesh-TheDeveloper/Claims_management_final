import React, { useState, useEffect } from "react";
import axios from "axios";

const ClaimsList = () => {
  const [claims, setClaims] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get("http://localhost:5000/claim-list")  // ✅ Check the correct backend URL
      .then((response) => setClaims(response.data.claims))
      .catch((err) => {
        console.error("Error fetching claims:", err);
        setError("Failed to load claims. Please try again.");
      });
  }, []);

  return (
    <div>
      <h2>Claims List</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {claims.length > 0 ? (
        <ul>
          {claims.map((claim) => (
            <li key={claim.claim_id}>
              <strong>Claim ID:</strong> {claim.claim_id}, <strong>Status:</strong> {claim.status}
            </li>
          ))}
        </ul>
      ) : (
        <p>No claims found.</p>
      )}
    </div>
  );
};

export default ClaimsList;
