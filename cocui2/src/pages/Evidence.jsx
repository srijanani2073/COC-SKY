import { useState } from "react";
import EvidenceModal from "../components/EvidenceModal";
import "../styles/table.css";

export default function Evidence() {
  const [showModal, setShowModal] = useState(false);
  return (
    <div>
      <h2>Evidence</h2>
      <button onClick={() => setShowModal(true)}>Upload Evidence</button>

      <table>
        <thead>
          <tr>
            <th>ID</th><th>Type</th><th>File</th><th>Uploaded By</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>EVD-01</td>
            <td>Digital</td>
            <td>photo.jpg</td>
            <td>Admin</td>
          </tr>
        </tbody>
      </table>

      {showModal && <EvidenceModal onClose={() => setShowModal(false)} />}
    </div>
  );
}