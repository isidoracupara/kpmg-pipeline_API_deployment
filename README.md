## Customer facing API for the KPMG use case: instracting info from CLA documents
# Url: https://kpmg-cla.onrender.com/docs

Features:
Advanced full text search (Algolia)
Intelligent document comparison (ChatGPT)
Structure Extraction (ChatGPT)

Endpoints:
GET /cla 
  - gets all CLA and their data from the database
GET /cla/{id} (example: https://kpmg-cla.onrender.com/cla/002-1000)
  - gets specific CLA data by id
GET /search/?keyword=example (example: https://kpmg-cla.onrender.com/search/?keyword=salaire)
  - gets all CLA with specified keyword
GET /comparison/{id} (example: https://kpmg-cla.onrender.com/comparison/002-1000)
  - returns comparison of CLA and its parent
