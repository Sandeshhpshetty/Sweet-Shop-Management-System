import React, { useEffect, useState } from "react";
import API from "../api/axiosConfig";

export default function SweetsPage() {
  const [sweets, setSweets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Load sweets from backend
  const loadSweets = async () => {
    try {
      setLoading(true);
      const res = await API.get("/sweets/");
      setSweets(res.data);
      setError("");
    } catch (err) {
      console.error(err);
      setError("Error loading sweets.");
    } finally {
      setLoading(false);
    }
  };

  // Purchase sweet
  const purchaseSweet = async (id) => {
    try {
      await API.post(`/sweets/${id}/purchase/`);
      loadSweets();
    } catch (err) {
      alert("Purchase failed: Out of stock or backend error");
    }
  };

  // Restock sweet (restore)
  const restockSweet = async (id) => {
    try {
      await API.post(`/sweets/${id}/restock/`);
      loadSweets();
    } catch (err) {
      alert("Restock failed");
    }
  };

  useEffect(() => {
    loadSweets();
  }, []);

  if (loading) return <h3>Loading sweets...</h3>;
  if (error) return <h3 style={{ color: "red" }}>{error}</h3>;

  return (
    <div style={{ padding: "20px" }}>
      <h2>Sweets List</h2>

      {sweets.length === 0 ? (
        <p>No sweets found.</p>
      ) : (
        sweets.map((sweet) => (
          <div
            key={sweet.id}
            style={{
              padding: "10px",
              border: "1px solid #ccc",
              marginBottom: "10px",
              borderRadius: "5px",
              width: "300px"
            }}
          >
            <p><b>Name:</b> {sweet.name}</p>
            <p><b>Category:</b> {sweet.category}</p>
            <p><b>Price:</b> ₹{sweet.price}</p>
            <p><b>Quantity:</b> {sweet.quantity}</p>

            {/* Purchase */}
            <button
              onClick={() => purchaseSweet(sweet.id)}
              disabled={sweet.quantity === 0}
            >
              Purchase
            </button>

            {/* Restore / Restock */}
            <button
              style={{ marginLeft: "10px" }}
              onClick={() => restockSweet(sweet.id)}
            >
              Restore
            </button>
          </div>
        ))
      )}
    </div>
  );
}
