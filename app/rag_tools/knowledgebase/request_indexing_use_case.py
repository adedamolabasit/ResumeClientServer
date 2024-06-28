import json
import os
import time
from typing import Optional
from web3 import Web3
from knowledgebase.entities import KnowledgeBaseIndexingResponse
import settings

# Initialize Web3 client
web3_client = Web3(Web3.HTTPProvider(settings.RPC_URL))
account = web3_client.eth.account.from_key(settings.PRIVATE_KEY)

# Construct absolute path to ChatOracle.json assuming it's in the same directory as this script
json_file_path = os.path.join(os.path.dirname(__file__), 'ChatOracle.json')

try:
    # Load ABI from ChatOracle.json
    with open(json_file_path, "r", encoding="utf-8") as f:
        oracle_abi = json.load(f)["abi"]

    # Initialize contract instance
    contract = web3_client.eth.contract(address=settings.ORACLE_ADDRESS, abi=oracle_abi)

except FileNotFoundError:
    # Handle FileNotFoundError
    print(f"Error: ChatOracle.json not found at {json_file_path}")
    exit(1)

def _get_index_cid(cid: str) -> str:
    """ Get index CID """
    return contract.functions.kbIndexes(cid).call()

def _get_indexing_error(request_id: int) -> str:
    """ Get indexing error """
    return contract.functions.kbIndexingRequestErrors(request_id).call()

def _is_indexing_request_processed(request_id: int) -> bool:
    """ Check if indexing request is processed """
    return contract.functions.isKbIndexingRequestProcessed(request_id).call()

def _request_indexing(cid: str) -> Optional[int]:
    nonce = web3_client.eth.get_transaction_count(account.address)
    tx_data = {
        "from": account.address,
        "nonce": nonce,
        "maxFeePerGas": web3_client.to_wei("2", "gwei"),
        "maxPriorityFeePerGas": web3_client.to_wei("1", "gwei"),
    }
    if chain_id := settings.CHAIN_ID:
        tx_data["chainId"] = int(chain_id)
    
    # Use build_transaction instead of buildTransaction
    tx = contract.functions.addKnowledgeBase(cid).build_transaction(tx_data)
    
    signed_tx = web3_client.eth.account.sign_transaction(tx, private_key=account.key)
    tx_hash = web3_client.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3_client.eth.wait_for_transaction_receipt(tx_hash)

    event = contract.events.KnowledgeBaseIndexRequestAdded()
    decoded_logs = event.process_receipt(tx_receipt)
    success = bool(tx_receipt.get("status"))
    if success:
        return decoded_logs[0]["args"]["id"]

def _wait_for_indexing(request_id: int, cid: str, max_loops: int = 120) -> KnowledgeBaseIndexingResponse:
    """ Wait for indexing to complete """
    print("Waiting for indexing to complete...", end="", flush=True)
    for _ in range(max_loops):
        index_cid = _get_index_cid(cid)
        error = _get_indexing_error(request_id)
        is_processed = _is_indexing_request_processed(request_id)
        if is_processed:
            return KnowledgeBaseIndexingResponse(
                id=request_id,
                is_processed=is_processed,
                index_cid=index_cid,
                error=error,
            )
        else:
            time.sleep(5)
    return KnowledgeBaseIndexingResponse(
        id=request_id,
        is_processed=False,
        index_cid=None,
        error="Timed out waiting for indexing to finish",
    )

def execute(cid: str) -> KnowledgeBaseIndexingResponse:
    """ Execute indexing process """
    index_cid = _get_index_cid(cid)
    if len(index_cid) and index_cid[0]:
        return KnowledgeBaseIndexingResponse(
            id=None, is_processed=True, index_cid=index_cid, error=None
        )
    request_id = _request_indexing(cid)
    if request_id is None:
        return KnowledgeBaseIndexingResponse(
            id=None,
            is_processed=False,
            index_cid=None,
            error="Failed to request indexing",
        )
    print("Indexing request successful. Waiting for completion...")
    return _wait_for_indexing(request_id, cid)

# Example usage
if __name__ == "__main__":
    cid = "your_cid_here"  # Replace with actual CID
    result = execute(cid)
    print("Indexing process result:", result)
