import json
import random
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
JSON_FILE = DATA_DIR / "transactions.json"


def load_transactions():
    if not JSON_FILE.exists():
        raise FileNotFoundError(
            f"{JSON_FILE} not found. Run your parser first to generate it."
        )
    with JSON_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def linear_search(transactions, target_id):
    """Scan through the list until a matching id is found."""
    for tx in transactions:
        if str(tx.get("id")) == str(target_id):
            return tx
    return None


def dict_lookup(tx_dict, target_id):
    """Return a transaction by dictionary key lookup."""
    return tx_dict.get(str(target_id))


def compare(transactions, trials=1000):
    if len(transactions) < 20:
        base = list(transactions)
        while len(transactions) < 20:
            transactions.append(dict(base[len(transactions) % len(base)]))

    ids = [tx["id"] for tx in transactions]
    mapping = {str(tx["id"]): tx for tx in transactions}

    targets = [random.choice(ids) for _ in range(trials)]

    t0 = time.perf_counter()
    for tid in targets:
        linear_search(transactions, tid)
    linear_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    for tid in targets:
        dict_lookup(mapping, tid)
    dict_time = time.perf_counter() - t0

    return {
        "records_tested": len(transactions),
        "trials": trials,
        "linear_total_time_s": round(linear_time, 6),
        "dict_total_time_s": round(dict_time, 6),
        "linear_avg_ms": round((linear_time / trials) * 1000, 6),
        "dict_avg_ms": round((dict_time / trials) * 1000, 6),
    }


if __name__ == "__main__":
    print("Loading transactions...")
    transactions = load_transactions()
    print(f"Loaded {len(transactions)} transactions from JSON.")

    print("\nRunning comparison (linear search vs dictionary lookup)...")
    results = compare(transactions, trials=1000)

    print("\n--- DSA Comparison Results ---")
    for k, v in results.items():
        print(f"{k}: {v}")
    print("------------------------------")
    print("\nReflection:")
    print(
        "- Linear search takes O(n) time since it checks one-by-one.\n"
        "- Dictionary lookup is O(1) on average, because Python dicts use hashing.\n"
        "- This shows why dictionaries are much more efficient for lookup-heavy tasks.\n"
        "- For very large datasets, advanced structures like Binary Search Trees could also help."
    )
