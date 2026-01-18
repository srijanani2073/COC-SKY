import Modal from "./Modal";

export default function CaseModal({ onClose }) {
  return (
    <Modal title="Add / Edit Case" onClose={onClose}>
      <input placeholder="Case Title" />
      <textarea placeholder="Description" />
      <input placeholder="Assigned Officer" />
      <select>
        <option>Open</option>
        <option>Closed</option>
      </select>

      <button>Save</button>
      <button onClick={onClose}>Cancel</button>
    </Modal>
  );
}