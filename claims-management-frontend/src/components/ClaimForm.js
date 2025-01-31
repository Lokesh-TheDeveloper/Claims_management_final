import React, { useState } from "react";
import axios from "axios";

const ClaimForm = () => {
  const [formData, setFormData] = useState({
    claim_id: "",
    policy_id: "",
    amount: "",
  });

  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:5000/claim", formData);
      setMessage(response.data?.message || "Claim created successfully!");
    } catch (error) {
      console.error("Error creating claim:", error);
      setMessage(error.response?.data?.error || "Failed to create claim.");
    }
  };

  return (
    <div>
      <h2>Create a Claim</h2>
      {message && <p>{message}</p>}
      <form onSubmit={handleSubmit}>
        <input type="number" name="claim_id" placeholder="Claim ID" onChange={handleChange} required />
        <input type="text" name="policy_id" placeholder="Policy ID" onChange={handleChange} required />
        <input type="number" name="amount" placeholder="Amount" onChange={handleChange} required />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default ClaimForm;
