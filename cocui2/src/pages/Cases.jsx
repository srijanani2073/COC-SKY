import { useState } from "react";
import CaseModal from "../components/CaseModal";
import "../styles/table.css";

export default function Cases() {
  const [showModal, setShowModal] = useState(false);

  return (
    <div>
      <h2>Cases</h2>
      <button onClick={() => setShowModal(true)}>Add Case</button>
      <table>
        <thead>
          <tr>
            <th>ID</th><th>Title</th><th>Status</th><th>Date</th><th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>CASE-01</td>
            <td>Forgery</td>
            <td>Open</td>
            <td>2026-01-10</td>
            <td>
              <button onClick={() => setShowModal(true)}>Edit</button>
            </td>
          </tr>
        </tbody>
      </table>

      {showModal && <CaseModal onClose={() => setShowModal(false)} />}
    </div>
  );
}