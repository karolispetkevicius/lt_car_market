// pages/index.js

import { useEffect, useState } from 'react';

export default function Home() {
  const [listings, setListings] = useState([]);

  useEffect(() => {
    // Fetch listings from your backend (you'll need to adjust the endpoint URL)
    fetch('/api/listings') // Example, modify this to your actual API URL
      .then((response) => response.json())
      .then((data) => setListings(data));
  }, []);

  return (
    <div className="container">
      <h1 className="text-center my-4">Car Listings</h1>
      <div className="row">
        {listings.map((listing) => (
          <div key={listing.id} className="col-md-4">
            <div className="card mb-4">
              <div className="card-body">
                <h5 className="card-title">{listing.brand} {listing.model}</h5>
                <p className="card-text">
                  Year: {listing.year}<br />
                  Price: ${listing.price}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
