# Customer facing API for the KPMG use case: extracting info from CLA documents
## Url: https://kpmg-cla.onrender.com/docs

Features:

  - Advanced full text search (Algolia)
  - Intelligent document comparison (ChatGPT)
  - Structure Extraction (ChatGPT)

Note: Works best with Firefox or Chrome



Endpoints:

GET /cla (example: https://kpmg-cla.onrender.com/cla)
  -gets all CLA and their data from the database


GET /cla/{id} (example: https://kpmg-cla.onrender.com/cla/200-2020-000391)
  -gets specific CLA data by id


GET /search/?keyword=example (example: https://kpmg-cla.onrender.com/search/?keyword=salaire)
  -gets all CLA with specified keyword


GET /comparison/{id} (example: https://kpmg-cla.onrender.com/comparison/200-2020-000391)
  -returns comparison of CLA and its parent if a parent document exists



Full project repo: https://github.com/KNobles/kpmg-pipeline
