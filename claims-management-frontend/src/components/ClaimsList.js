// import React, { useState, useEffect } from "react";

// const ClaimsList = () => {
//   const [claims, setClaims] = useState([]);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     fetch("https://claims-management-final-1.onrender.com/claim-list") // Make sure your backend has this endpoint
//       .then((response) => response.json())
//       .then((data) => setClaims(data.claims))
//       .catch((err) => setError(err.message));
//   }, []);

//   return (
//     <div>
//       <h2>Claims List</h2>
//       {error && <p style={{ color: "red" }}>{error}</p>}
//       {claims.length > 0 ? (
//         <ul>
//           {claims.map((claim) => (
//             <li key={claim.claim_id}>
//               <strong>Claim ID:</strong> {claim.claim_id}, <strong>Status:</strong> {claim.status}
//             </li>
//           ))}
//         </ul>
//       ) : (
//         <p>No claims found.</p>
//       )}
//     </div>
//   );
// };

// export default ClaimsList;
