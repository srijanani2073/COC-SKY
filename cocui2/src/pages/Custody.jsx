import { useState } from "react";
import TransferCustodyModal from "../components/TransferCustodyModal";
import "../styles/custody.css";

export default function Custody() {
  const [showTransfer, setShowTransfer] = useState(false);

  return (
    <div className="custody-layout">
      <div className="evidence-info">
        <h3>Evidence Information</h3>
        <p><b>ID:</b> EVD-01</p>
        <p><b>Type:</b> Digital</p>
        <p><b>Current Custodian:</b> Officer A</p>

        <button onClick={() => setShowTransfer(true)}>
          Transfer Custody
        </button>
        <button>View History</button>
      </div>
      <div className="graph-area">
        <h3>Chain of Custody Graph</h3>
        <div className="graph-placeholder">
          Neo4j Graph Visualization Area
        </div>
      </div>

      {showTransfer && (
        <TransferCustodyModal onClose={() => setShowTransfer(false)} />
      )}
    </div>
  );
}