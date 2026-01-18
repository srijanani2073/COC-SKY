import "../styles/modal.css";

export default function Modal({ title, onClose, children }) {
  return (
    <div className="modal-backdrop">
      <div className="modal-window">
        <div className="modal-header">
          <h3>{title}</h3>
          <button onClick={onClose}>✖</button>
        </div>
        <div className="modal-body">
          {children}
        </div>
      </div>
    </div>
  );
}