import Modal from "./Modal";

export default function TransferCustodyModal({ onClose }) {
  return (
    <Modal title="Transfer Custody" onClose={onClose}>
      <input value="Officer A" disabled />
      <select>
        <option>Officer B</option>
        <option>Forensics Lab</option>
        <option>Evidence Locker</option>
      </select>
      <textarea placeholder="Reason for transfer" />

      <button>Transfer</button>
      <button onClick={onClose}>Cancel</button>
    </Modal>
  );
}