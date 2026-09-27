import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const controller = new AbortController();

    axios
      .get("/api/v1/customers", { signal: controller.signal })
      .then((response) => {
        setCustomers(response.data.items);
      })
      .catch((err) => {
        if (!controller.signal.aborted) {
          setError(
            err.response?.data?.detail ?? "Could not load customers."
          );
        }
      })
      .finally(() => {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      });

    return () => controller.abort();
  }, []);

  if (loading) return <main><p>Loading customers…</p></main>;
  if (error) return <main><p role="alert">{error}</p></main>;

  return (
    <main>
      <h1>Sample customers</h1>
      <p>{customers.length} records loaded from the API</p>

      <table>
        <thead>
          <tr>
            <th>Customer ID</th>
            <th>First name</th>
            <th>Last name</th>
            <th>City</th>
            <th>State</th>
          </tr>
        </thead>
        <tbody>
          {customers.map((customer) => (
            <tr key={customer.customerID}>
              <td>{customer.customerID}</td>
              <td>{customer.first_name}</td>
              <td>{customer.last_name}</td>
              <td>{customer.city}</td>
              <td>{customer.state}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}

export default App;