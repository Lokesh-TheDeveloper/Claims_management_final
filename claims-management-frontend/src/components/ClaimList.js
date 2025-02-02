import React, { useState, useEffect } from "react";
import axios from "axios";

const ClaimsList = () => {
  const [claims, setClaims] = useState([]);
  const [error, setError] = useState(null);

  // Fetch claims from backend
  useEffect(() => {
    axios
      .get("https://claims-management-final-1.onrender.com/claim-list")
      .then((response) => setClaims(response.data.claims))
      .catch((err) => {
        console.error("Error fetching claims:", err);
        setError("Failed to load claims. Please try again.");
      });
  }, []);

  const handleDelete = (claim_id) => {
    axios
      .delete(`https://claims-management-final-1.onrender.com/claim/${claim_id}`)
      .then((response) => {
        alert(response.data.message); // Optional: Display a success message
        setClaims(claims.filter((claim) => claim.claim_id !== claim_id)); // Remove claim from the list
      })
      .catch((error) => {
        console.error("Error deleting claim:", error);
        alert("Failed to delete claim");
      });
  };

  return (
    <div>
      <h2>Claims List</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {claims.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>Claim ID</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {claims.map((claim) => (
              <tr key={claim.claim_id}>
                <td>{claim.claim_id}</td>
                <td>{claim.status}</td>
                <td>
                  {/* Delete Button */}
                  <button
                    className="delete-btn"
                    onClick={() => handleDelete(claim.claim_id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No claims found.</p>
      )}
    </div>
  );
};

export default ClaimsList;
