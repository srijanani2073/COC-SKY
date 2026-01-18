import Modal from "./Modal";

export default function EvidenceModal({ onClose }) {
  return (
    <Modal title="Upload Evidence" onClose={onClose}>
      <div>
        <label>
          <input type="radio" name="type" /> Physical
        </label>
        <label>
          <input type="radio" name="type" /> Digital
        </label>
      </div>

      <input type="file" />
      <textarea placeholder="Description" />
      <input placeholder="Source Location" />

      <button>Upload</button>
      <button onClick={onClose}>Cancel</button>
    </Modal>
  );
}