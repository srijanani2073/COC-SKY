export default function Reports() {
  return (
    <div>
      <h2>Report Generator</h2>
      <div style={{ width: "300px" }}>
        <label>Select Case</label>
        <select style={{ width: "100%", marginBottom: "10px" }}>
          <option>CASE-01</option>
          <option>CASE-02</option>
        </select>
        <button>Generate Report</button>
        <p style={{ marginTop: "15px", color: "green" }}>
          Report generated successfully.
        </p>
        <a href="#">Download Report (PDF)</a>
      </div>
    </div>
  );
}