import { alerts } from "../data/alertsMock";
import "../styles/alerts.css";

export default function Alerts() {
  return (
    <div>
      <h2>Security Alerts</h2>
      <table>
        <thead>
          <tr>
            <th>Type</th>
            <th>Related</th>
            <th>Severity</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {alerts.map(alert => (
            <tr key={alert._id} className={alert.severity.toLowerCase()}>
              <td>{alert.type}</td>
              <td>{alert.related}</td>
              <td>{alert.severity}</td>
              <td>{alert.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}