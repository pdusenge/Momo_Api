import re
import json
import xml.etree.ElementTree as ET
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
XML_FILE = DATA_DIR / "modified_sms_v2.xml"
JSON_FILE = DATA_DIR / "transactions.json"

def classify_and_parse(body: str):
    """Parse SMS body into a structured transaction dict."""
    tx = {
        "transaction_id": None,
        "type": None,
        "amount": None,
        "sender": None,
        "receiver": None,
        "timestamp": None,
        "balance": None,
        "fee": None,
        "raw_body": body.strip(),
    }

    # Receive money
    m = re.search(r"received (\d+[,.]?\d*) RWF from (.+?) \(", body)
    if m:
        tx["type"] = "receive"
        tx["amount"] = m.group(1)
        tx["sender"] = m.group(2)
        tx["transaction_id"] = re.search(r"Financial Transaction Id: (\d+)", body).group(1) if "Financial Transaction Id" in body else None
        tx["balance"] = re.search(r"balance[: ](\d+[,.]?\d*) RWF", body).group(1) if "balance" in body else None
        tx["timestamp"] = re.search(r"at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body).group(1)
        return tx

    # Payment
    m = re.search(r"TxId[: ](\d+).+ Your payment of (\d+[,.]?\d*) RWF to (.+?) (\d+)?", body)
    if m:
        tx["type"] = "payment"
        tx["transaction_id"] = m.group(1)
        tx["amount"] = m.group(2)
        tx["receiver"] = m.group(3).strip()
        m4 = re.search(r"balance [: ](\d+[,.]?\d*) RWF", body, re.I)
        tx["balance"] = m4.group(1) if m4 else None
        tx["timestamp"] = re.search(r"at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body).group(1)
        m5 = re.search(r"Fee (?:was|paid): (\d+[,.]?\d*) RWF", body, re.I)
        tx["fee"] = m5.group(1) if m5 else None        
        return tx
    # CodePay
    m = re.search(
        r"TxId[: ] (\d+). Your payment of (\d+[,.]?\d*) RWF to (.+?) (\d+)? has been completed at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})",
        body,
        re.I,
    )
    if m:
        tx["type"] = "codePay"
        tx["transaction_id"] = m.group(1)
        tx["amount"] = m.group(2)
        tx["receiver"] = (m.group(3) + ((" " + m.group(4)) if m.group(4) else "")).strip()
        tx["timestamp"] = m.group(5)
        m_bal = re.search(r"balance[: ] (\d+[,.]?\d*) RWF", body, re.I)
        tx["balance"] = m_bal.group(1) if m_bal else None
        m_fee = re.search(r" Fee (?:was|paid): (\d+[,.]?\d*) RWF", body, re.I)
        tx["fee"] = m_fee.group(1) if m_fee else 0
        return tx
    # Deposit
    m = re.search(r"deposit of (\d+[,.]?\d*) RWF.*at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)
    if m:
        tx["type"] = "deposit"
        tx["amount"] = m.group(1)
        tx["timestamp"] = m.group(2)
        m2 = re.search(r"BALANCE [: ](\d+[,.]?\d*) RWF", body, re.I)
        tx["balance"] = m2.group(1) if m2 else None
        return tx
    
    # Airtime purchase
    m = re.search(
        r"TxId[: ](\d+).*payment of (\d+[,.]?\d*) RWF to Airtime.*at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})",
        body,
        re.I,
    )
    if m:
        tx["type"] = "airtime"
        tx["transaction_id"] = m.group(1)
        tx["amount"] = m.group(2)
        tx["receiver"] = "Airtime"
        tx["timestamp"] = m.group(3)
        # optional fee
        m_fee = re.search(r"Fee (?:was|paid): (\d+[,.]?\d*) RWF", body, re.I)
        tx["fee"] = m_fee.group(1) if m_fee else 0
        # optional balance
        m_bal = re.search(r"balance[: ] (\d+[,.]?\d*) RWF", body, re.I)
        tx["balance"] = m_bal.group(1) if m_bal else None
        return tx


    # Transfer
    m = re.search(r"(\d+[,.]?\d*) RWF transferred to (.+?) \(", body)
    if m:
        tx["type"] = "transfer"
        tx["amount"] = m.group(1)
        tx["receiver"] = m.group(2).strip()
        tx["timestamp"] = re.search(r"at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body).group(1)
        tx["fee"] = re.search(r"Fee (?:was|paid): (\d+[,.]?\d*) RWF", body).group(1) if "Fee" in body else None
        m3 = re.search(r"balance[: ] (\d+[,.]?\d*) RWF", body, re.I)
        tx["balance"] = m3.group(1) if m3 else None
        return tx

    # Withdrawal
    if "withdrawn" in body.lower():
        m = re.search(r"withdrawn (\d+[,.]?\d*) RWF.*at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)
        if m:
            tx["type"] = "withdraw"
            tx["amount"] = m.group(1)
            tx["timestamp"] = m.group(2)
            m6 = re.search(r"balance [: ](\d+[,.]?\d*) RWF", body, re.I)
            tx["balance"] = m6.group(1) if m6 else None
            tx["fee"] = re.search(r"Fee (?:was|paid): (\d+[,.]?\d*) RWF", body).group(1) if "Fee" in body else None
        return tx

    # OTP or others
    if "one-time password" in body.lower() or "otp" in body.lower():
        tx["type"] = "otp"
        return tx

    tx["type"] = "other"
    return tx


def parse_xml():
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    transactions = []

    for idx, sms in enumerate(root.findall("sms"), start=1):
        body = sms.get("body", "")
        parsed = classify_and_parse(body)
        parsed["id"] = idx
        parsed["raw_date"] = sms.get("readable_date")
        transactions.append(parsed)

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(transactions, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(transactions)} transactions to {JSON_FILE}")


if __name__ == "__main__":
    parse_xml()
