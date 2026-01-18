import { timelineEvents } from "../data/timelineMock";
import "../styles/timeline.css";

export default function Timeline() {
  return (
    <div>
      <h2>Case Timeline</h2>
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Event</th>
            <th>Description</th>
            <th>Actor</th>
          </tr>
        </thead>
        <tbody>
          {timelineEvents.map((evt) => (
            <tr key={evt._id}>
              <td>{evt.timestamp}</td>
              <td>{evt.type.replace("_", " ")}</td>
              <td>{evt.description}</td>
              <td>{evt.actor}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}