from pymongo import MongoClient, UpdateOne, errors
from datetime import datetime, timedelta
import time

# Connection setup
target_host = "localhost"
target_port = 27018

try:
    print(f"Connecting to target MongoDB at {target_host}:{target_port}...")
    client = MongoClient(target_host, target_port, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("Connected to target MongoDB.")
except errors.ServerSelectionTimeoutError as e:
    print(f"Failed to connect to target MongoDB: {e}")
    exit(1)

# Connect to the actual database
target_db_name = "econdDB"
db = client[target_db_name]

start_time_total = time.time()

# Process each collection
for collection_name in db.list_collection_names():
    collection = db[collection_name]
    print(f"\n Processing collection: {collection_name}")

    total_docs = collection.estimated_document_count()
    if total_docs == 0:
        print("Collection is empty. Skipping.")
        continue

    # Get only necessary fields
    docs_cursor = collection.find({}, {"_id": 1, "chip_number": 1})

    bulk_updates = []
    batch_size = 500
    processed = 0

    start_time = time.time()

    for doc in docs_cursor:
        chip = doc.get('chip_number')

        try:
            chip_int = int(chip)
            if 0 <= chip_int <= 9999:
                chip_int += 1000000

            bulk_updates.append(UpdateOne(
                {"_id": doc["_id"]},
                {"$set": {"chip_number": chip_int}}
            ))
        except (ValueError, TypeError):
            print(f"Skipping document {doc['_id']} with invalid chip_number: {chip}")

        processed += 1

        # Execute in batches
        if len(bulk_updates) >= batch_size:
            collection.bulk_write(bulk_updates, ordered=False)
            bulk_updates = []

            # Timing
            elapsed = time.time() - start_time
            docs_left = total_docs - processed
            rate = processed / elapsed if elapsed > 0 else 0
            eta = timedelta(seconds=int(docs_left / rate)) if rate else "unknown"

            print(f"Updated {processed}/{total_docs} docs "
                  f"({(processed / total_docs) * 100:.1f}%) - ETA: {eta}")

    # Final batch
    if bulk_updates:
        collection.bulk_write(bulk_updates, ordered=False)
        print(f"Applied final {len(bulk_updates)} updates")

    duration = time.time() - start_time
    print(f"Finished collection {collection_name} in {timedelta(seconds=int(duration))}")

total_duration = time.time() - start_time_total
print(f"\nAll collections updated in {timedelta(seconds=int(total_duration))}")
