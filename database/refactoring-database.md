# Refactoring the Codebase for Firestore Integration

This document outlines the changes, updates, and removals required in the codebase, particularly in the `models` package, to transition from the current JSON-based storage to Firestore as the database.

---

## **1. Overview of Changes**

- **Database Integration**: Replace JSON file-based storage with Firestore for storing and retrieving data.
- **Firestore Client**: Introduce Firestore client initialization and queries.
- **Data Models**: Update models to interact with Firestore instead of reading/writing JSON files.
- **Collections**: Map existing collections (`courses`, `labs`, `paths`) to Firestore collections.
- **Error Handling**: Update error handling to account for Firestore-specific exceptions.
- **Data Serialization**: Ensure compatibility between Firestore document structure and existing data models.

---

## **2. Changes to the `models` Package**

### **2.1. `BaseEntity` Class**

- **Current Role**: Acts as a base class for entities like `Course`, `Lab`, and `Path`. Handles JSON serialization and file-based storage.
- **Changes**:
  - Remove methods for saving/loading JSON files (`save_json`, `load_json`).
  - Add methods for Firestore integration:
    - `save_to_firestore`: Save the entity to Firestore.
    - `load_from_firestore`: Load the entity from Firestore.
    - `delete_from_firestore`: Delete the entity from Firestore.

#### Example:

```python
class BaseEntity:
    def save_to_firestore(self, collection_name: str):
        db.collection(collection_name).document(self.id).set(self.to_dict())

    def load_from_firestore(self, collection_name: str):
        doc = db.collection(collection_name).document(self.id).get()
        if doc.exists:
            self.from_dict(doc.to_dict())
        else:
            raise ValueError(f"Document with ID {self.id} not found in {collection_name}.")

    def delete_from_firestore(self, collection_name: str):
        db.collection(collection_name).document(self.id).delete()
```

---

### **2.2. `Course` Class**

- **Current Role**: Represents a course entity, handles extracting course data and saving it to JSON.
- **Changes**:
  - Replace JSON file operations with Firestore operations.
  - Update `extract_transcript` to save course data directly to Firestore.
  - Add Firestore-specific methods for querying related data (e.g., modules, activities).

#### Example Updates:

- **Replace JSON Save/Load**:
  ```python
  def save_to_firestore(self):
      super().save_to_firestore("courses")

  def load_from_firestore(self):
      super().load_from_firestore("courses")
  ```

- **Update `extract_transcript`**:
  - Save extracted data (e.g., modules, activities) directly to Firestore.
  - Remove file-based operations like `save_json`.

---

### **2.3. `Lab` Class**

- **Current Role**: Represents a lab entity, handles extracting lab data and saving it to JSON.
- **Changes**:
  - Replace JSON file operations with Firestore operations.
  - Add Firestore-specific methods for saving/loading lab steps.

#### Example Updates:

- **Replace JSON Save/Load**:
  ```python
  def save_to_firestore(self):
      super().save_to_firestore("labs")

  def load_from_firestore(self):
      super().load_from_firestore("labs")
  ```

- **Update Lab Steps**:
  - Save lab steps as subcollections in Firestore.

---

### **2.4. `Path` Class**

- **Current Role**: Represents a learning path entity, handles extracting path data and saving it to JSON.
- **Changes**:
  - Replace JSON file operations with Firestore operations.
  - Add Firestore-specific methods for managing `hasPart` relationships.

#### Example Updates:

- **Replace JSON Save/Load**:
  ```python
  def save_to_firestore(self):
      super().save_to_firestore("paths")

  def load_from_firestore(self):
      super().load_from_firestore("paths")
  ```

- **Update `hasPart` Relationships**:
  - Save `hasPart` as references to related documents in Firestore.

---

### **2.5. `Collection` Class**

- **Current Role**: Manages collections of entities (e.g., `courses`, `labs`, `paths`) and handles JSON file operations.
- **Changes**:
  - Replace JSON file operations with Firestore queries.
  - Add methods for querying Firestore collections.

#### Example Updates:

- **Replace JSON Save/Load**:
  ```python
  def load_from_firestore(self, collection_name: str):
      docs = db.collection(collection_name).stream()
      self.items = {doc.id: doc.to_dict() for doc in docs}

  def save_to_firestore(self, collection_name: str):
      for item_id, item_data in self.items.items():
          db.collection(collection_name).document(item_id).set(item_data)
  ```

---

## **3. Updates to Utility Functions**

- **Current Role**: Provide helper functions for JSON serialization, HTML parsing, etc.
- **Changes**:
  - Remove JSON-specific utilities (e.g., `save_json`, `load_json`).
  - Add Firestore-specific utilities for data serialization/deserialization.

---

## **4. Updates to Error Handling**

- **Current Role**: Handle exceptions related to file operations and HTML parsing.
- **Changes**:
  - Add handling for Firestore-specific exceptions (e.g., `google.api_core.exceptions.NotFound`).

---

## **5. Removal of JSON File Operations**

- **Files Affected**:
  - Remove JSON file operations from `BaseEntity`, `Course`, `Lab`, `Path`, and `Collection`.
  - Remove JSON-specific utility functions.

---

## **6. Firestore Client Initialization**

- Add Firestore client initialization in a central location (e.g., `database.py`).

#### Example:

```python
from google.cloud import firestore

db = firestore.Client()
```

---

## **7. Testing and Validation**

- **Unit Tests**:
  - Update unit tests to mock Firestore operations.
  - Remove tests for JSON file operations.
- **Integration Tests**:
  - Test Firestore integration for all models and collections.

---

## **8. Summary of Changes**

| Component       | Change                                                                 |
|------------------|------------------------------------------------------------------------|
| `BaseEntity`     | Add Firestore methods (`save_to_firestore`, `load_from_firestore`).    |
| `Course`         | Replace JSON operations with Firestore operations.                    |
| `Lab`            | Replace JSON operations with Firestore operations.                    |
| `Path`           | Replace JSON operations with Firestore operations.                    |
| `Collection`     | Replace JSON operations with Firestore queries.                       |
| Utility Functions| Remove JSON-specific utilities, add Firestore utilities.              |
| Error Handling   | Add Firestore-specific exception handling.                             |

---

## **9. Benefits of Refactoring**

- **Scalability**: Firestore provides a scalable solution for managing large datasets.
- **Real-Time Updates**: Firestore enables real-time updates for data changes.
- **Simplified Codebase**: Removing JSON file operations reduces complexity.
- **Cloud Integration**: Firestore aligns with the planned deployment to Cloud Run.

---

## **10. Next Steps**

1. Implement Firestore integration in the `models` package.
2. Update unit and integration tests.
3. Validate the refactored codebase with real data.
4. Deploy the updated application to Cloud Run.
