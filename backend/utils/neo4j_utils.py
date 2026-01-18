from neo4j import GraphDatabase
from backend.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE
NEO4J_DB = NEO4J_DATABASE

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

def create_case_node(case_id: int):
    query = """
    MERGE (c:Case {case_id: $case_id})
    RETURN c
    """
    with driver.session(database=NEO4J_DB) as session:
        session.run(query, case_id=case_id)

def create_evidence_node(case_id: int, evidence_id: int, version: int):
    query = """
    MERGE (c:Case {case_id: $case_id})
    MERGE (e:Evidence {evidence_id: $evidence_id})
    SET e.version = $version
    MERGE (c)-[:HAS_EVIDENCE]->(e)
    """
    with driver.session(database=NEO4J_DB) as session:
        session.run(
            query,
            case_id=case_id,
            evidence_id=evidence_id,
            version=version
        )

def create_custody_event(
    case_id: int,
    evidence_id: int,
    custody_id: int,
    from_user: int,
    to_user: int,
    action: str,
    location: str,
    timestamp
):
    query = """
    MERGE (c:Case {case_id: $case_id})
    MERGE (e:Evidence {evidence_id: $evidence_id})

    MERGE (u_from:User {user_id: $from_user})
    MERGE (u_to:User {user_id: $to_user})

    CREATE (ce:CustodyEvent {
        custody_id: $custody_id,
        action: $action,
        location: $location,
        timestamp: $timestamp
    })

    MERGE (c)-[:HAS_EVIDENCE]->(e)
    MERGE (e)-[:HAS_CUSTODY_EVENT]->(ce)
    MERGE (ce)-[:FROM]->(u_from)
    MERGE (ce)-[:TO]->(u_to)
    """
    with driver.session(database=NEO4J_DB) as session:
        session.run(
            query,
            case_id=case_id,
            evidence_id=evidence_id,
            custody_id=custody_id,
            from_user=from_user,
            to_user=to_user,
            action=action,
            location=location,
            timestamp=timestamp
        )

def get_custody_graph(evidence_id: int):
    query = """
    MATCH (e:Evidence {evidence_id: $evidence_id})-[:HAS_CUSTODY_EVENT]->(ce)
    MATCH (ce)-[:FROM]->(u_from)
    MATCH (ce)-[:TO]->(u_to)
    RETURN ce, u_from, u_to
    ORDER BY ce.timestamp ASC
    """
    results = []
    with driver.session(database=NEO4J_DB) as session:
        records = session.run(query, evidence_id=evidence_id)

        for record in records:
            ce = record["ce"]
            u_from = record["u_from"]
            u_to = record["u_to"]

            ts = ce["timestamp"]
            if ts is not None:
                ts = ts.iso_format()

            results.append({
                "custody_id": ce.get("custody_id"),
                "action": ce.get("action"),
                "location": ce.get("location"),
                "timestamp": ts,
                "from_user": u_from.get("user_id"),
                "to_user": u_to.get("user_id")
            })

    return results