import { useState, useEffect } from 'react';

export default function Listings() {
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [brand, setBrand] = useState('');
  const [model, setModel] = useState('');
  const [minYear, setMinYear] = useState('');
  const [maxYear, setMaxYear] = useState('');
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [orderBy, setOrderBy] = useState('price');
  const [orderDirection, setOrderDirection] = useState('asc');
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(10);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchListings();
  }, [page]);

  const fetchListings = async () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (brand) params.append('brand', brand);
    if (model) params.append('model', model);
    if (minYear) params.append('min_year', minYear);
    if (maxYear) params.append('max_year', maxYear);
    if (minPrice) params.append('min_price', minPrice);
    if (maxPrice) params.append('max_price', maxPrice);
    params.append('order_by', orderBy);
    params.append('order_direction', orderDirection);
    params.append('page', page);
    params.append('limit', limit);
    const url = `http://127.0.0.1:8000/listings?${params.toString()}`;
    
    console.log('Fetching URL:', url);  // Log the URL
    
    try {
      const response = await fetch(url);
      const data = await response.json();
      setListings(data);
      // Calculate total pages based on the total number of listings (Assuming this is returned in the response)
      const totalListings = response.headers.get('X-Total-Count');
      setTotalPages(Math.ceil(totalListings / limit));
    } catch (error) {
      console.error('Error fetching listings:', error);
    }
    setLoading(false);
  };

  const applyFilters = async () => {
    setPage(1);  // Reset to the first page when filters are applied
    fetchListings();
  };

  const resetFilters = () => {
    setBrand('');
    setModel('');
    setMinYear('');
    setMaxYear('');
    setMinPrice('');
    setMaxPrice('');
    setOrderBy('price');
    setOrderDirection('asc');
    setPage(1);
    fetchListings();
  };

  const handlePreviousPage = () => {
    if (page > 1) {
      setPage(page - 1);
    }
  };

  const handleNextPage = () => {
    if (page < totalPages) {
      setPage(page + 1);
    }
  };

  return (
    <div className="container mt-5">
      <h2>Car Listings</h2>
      <div className="row">
        {/* Filters */}
        <div className="col-md-3">
          <div className="filters mb-4">
            <input
              type="text"
              placeholder="Brand"
              value={brand}
              onChange={(e) => setBrand(e.target.value)}
              className="form-control mb-2"
            />
            <input
              type="text"
              placeholder="Model"
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="form-control mb-2"
            />
            <input
              type="number"
              placeholder="Min Year"
              value={minYear}
              onChange={(e) => setMinYear(e.target.value)}
              className="form-control mb-2"
            />
            <input
              type="number"
              placeholder="Max Year"
              value={maxYear}
              onChange={(e) => setMaxYear(e.target.value)}
              className="form-control mb-2"
            />
            <input
              type="number"
              placeholder="Min Price"
              value={minPrice}
              onChange={(e) => setMinPrice(e.target.value)}
              className="form-control mb-2"
            />
            <input
              type="number"
              placeholder="Max Price"
              value={maxPrice}
              onChange={(e) => setMaxPrice(e.target.value)}
              className="form-control mb-2"
            />
            <div className="mb-2">
              <label>Order by</label>
              <select
                value={orderBy}
                onChange={(e) => setOrderBy(e.target.value)}
                className="form-select"
              >
                <option value="price">Price</option>
                <option value="year">Year</option>
              </select>
            </div>
            <div className="mb-2">
              <label>Order</label>
              <select
                value={orderDirection}
                onChange={(e) => setOrderDirection(e.target.value)}
                className="form-select"
              >
                <option value="asc">Ascending</option>
                <option value="desc">Descending</option>
              </select>
            </div>
            <button onClick={applyFilters} className="btn btn-primary mt-2">Apply Filters</button>
            <button onClick={resetFilters} className="btn btn-secondary mt-2">Reset Filters</button>
          </div>
        </div>
        
        {/* Listings */}
        <div className="col-md-9">
          {loading ? (
            <p>Loading...</p>
          ) : (
            <>
              <table className="table table-striped">
                <thead>
                  <tr>
                    <th>Brand</th>
                    <th>Model</th>
                    <th>Price</th>
                    <th>Year</th>
                    <th>Mileage</th>
                    <th>Fuel Type</th>
                    <th>URL</th>
                  </tr>
                </thead>
                <tbody>
                  {listings.length > 0 ? (
                    listings.map((listing) => (
                      <tr key={listing.id}>
                        <td>{listing.brand}</td>
                        <td>{listing.model}</td>
                        <td>${listing.price}</td>
                        <td>{listing.year}</td>
                        <td>{listing.mileage}</td>
                        <td>{listing.fuel_type}</td>
                        <td>
                          <a href={listing.url} target="_blank" rel="noopener noreferrer">{listing.url}</a>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="7">No listings found.</td>
                    </tr>
                  )}
                </tbody>
              </table>
              {/* Pagination Controls */}
              <div className="pagination-controls">
                <button onClick={handlePreviousPage} className="btn btn-outline-primary" disabled={page === 1}>Previous</button>
                <span className="mx-3">Page {page} of {totalPages}</span>
                <button onClick={handleNextPage} className="btn btn-outline-primary" disabled={page === totalPages}>Next</button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
