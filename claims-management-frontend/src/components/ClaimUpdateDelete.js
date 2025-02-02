import React, { useState } from "react";
import axios from "axios";

const ClaimUpdateDelete = () => {
  const [claimId, setClaimId] = useState("");
  const [newStatus, setNewStatus] = useState("");
  const [message, setMessage] = useState("");

  const handleUpdate = async () => {
    if (!claimId || !newStatus) {
      setMessage("Please enter Claim ID and new status.");
      return;
    }
    try {
      const response = await axios.put(`https://claims-management-final-1.onrender.com/claim/${claimId}`, {
        status: newStatus,
      });
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response?.data?.error || "Error updating claim.");
    }
  };

  const handleDelete = async () => {
    if (!claimId) {
      setMessage("Please enter Claim ID.");
      return;
    }
    try {
      const response = await axios.delete(`https://claims-management-final-1.onrender.com/claim/${claimId}`);
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response?.data?.error || "Error deleting claim.");
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "auto", textAlign: "center", padding: "20px" }}>
      <h2>Update or Delete Claim</h2>
      <input
        type="text"
        placeholder="Enter Claim ID"
        value={claimId}
        onChange={(e) => setClaimId(e.target.value)}
        style={{ display: "block", margin: "10px auto", padding: "8px", width: "100%" }}
      />
      <input
        type="text"
        placeholder="Enter New Status"
        value={newStatus}
        onChange={(e) => setNewStatus(e.target.value)}
        style={{ display: "block", margin: "10px auto", padding: "8px", width: "100%" }}
      />
      <button onClick={handleUpdate} style={{ padding: "10px", margin: "5px", background: "blue", color: "white" }}>
        Update Claim
      </button>
      <button onClick={handleDelete} style={{ padding: "10px", margin: "5px", background: "red", color: "white" }}>
        Delete Claim
      </button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default ClaimUpdateDelete;
