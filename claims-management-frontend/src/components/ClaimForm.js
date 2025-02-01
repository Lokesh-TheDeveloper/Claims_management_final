import React, { useState } from "react";
import axios from "axios";

const ClaimForm = () => {
  const [tab, setTab] = useState("create"); // Toggle between Create & Update/Delete
  const [claimId, setClaimId] = useState("");
  const [policyId, setPolicyId] = useState("");
  const [amount, setAmount] = useState("");
  const [newStatus, setNewStatus] = useState("");
  const [message, setMessage] = useState("");

  const handleCreate = async () => {
    if (!claimId || !policyId || !amount) {
      setMessage("Please fill all fields.");
      return;
    }
    try {
      const response = await axios.post("http://localhost:5000/claim", {
        claim_id: claimId,
        policy_id: policyId,
        amount: parseFloat(amount),
      });
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response?.data?.error || "Error creating claim.");
    }
  };

  const handleUpdate = async () => {
    if (!claimId || !newStatus) {
      setMessage("Please enter Claim ID and new status.");
      return;
    }
    try {
      const response = await axios.put(`http://localhost:5000/claim/${claimId}`, {
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
      const response = await axios.delete(`http://localhost:5000/claim/${claimId}`);
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response?.data?.error || "Error deleting claim.");
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "auto", textAlign: "center", padding: "20px" }}>
      <h2>Claims Management</h2>
      <div>
        <button onClick={() => setTab("create")} style={{ marginRight: "10px" }}>Create Claim</button>
        <button onClick={() => setTab("update-delete")}>Update Claim</button>
      </div>

      {tab === "create" ? (
        <div>
          <input type="text" placeholder="Enter Claim ID" value={claimId} onChange={(e) => setClaimId(e.target.value)} style={{ display: "block", margin: "10px auto", padding: "8px", width: "100%" }} />
          <input type="text" placeholder="Enter Policy ID" value={policyId} onChange={(e) => setPolicyId(e.target.value)} style={{ display: "block", margin: "10px auto", padding: "8px", width: "100%" }} />
          <input type="number" placeholder="Enter Amount" value={amount} onChange={(e) => setAmount(e.target.value)} style={{ display: "block", margin: "10px auto", padding: "8px", width: "100%" }} />
          <button onClick={handleCreate} style={{ padding: "10px", margin: "5px", background: "white", color: "black" }}>Create Claim</button>
        </div>
      ) : (
        <div>
          <input type="text" placeholder="Enter Claim ID" value={claimId} onChange={(e) => setClaimId(e.target.value)} style={{ display: "block", margin: "10px auto", padding: "8px", width: "100%" }} />
          <input type="text" placeholder="Enter New Status" value={newStatus} onChange={(e) => setNewStatus(e.target.value)} style={{ display: "block", margin: "10px auto", padding: "8px", width: "100%" }} />
          <button onClick={handleUpdate} style={{ padding: "10px", margin: "5px", background: "white", color: "black" }}>Update Claim</button>
          {/* <button onClick={handleDelete} style={{ padding: "10px", margin: "5px", background: "white", color: "black" }}>Delete Claim</button> */}
        </div>
      )}

      {message && <p>{message}</p>}
    </div>
  );
};

export default ClaimForm;