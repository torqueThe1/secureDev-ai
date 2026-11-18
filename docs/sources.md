
# Knowledge Sources and Attribution

SecureDev AI uses third-party documentation as its
retrieval-augmented generation (RAG) knowledge base.

## FastAPI

- Project: FastAPI
- Author: Sebastián Ramírez and contributors
- Topic: OAuth2 and JWT Authentication
- Documentation:
  https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
- Source repository:
  https://github.com/fastapi/fastapi
- Python example:
  https://github.com/fastapi/fastapi/blob/master/docs_src/security/tutorial004.py
- License: MIT
- License text:
  https://github.com/fastapi/fastapi/blob/master/LICENSE

The documentation is used for text retrieval.
The Python example is indexed to preserve original
function definitions.

## OWASP

- Project: OWASP Cheat Sheet Series
- Author: OWASP Cheat Sheet Series contributors
- Topic: Authentication Security
- Documentation:
  https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- Source repository:
  https://github.com/OWASP/CheatSheetSeries
- License: Creative Commons Attribution-ShareAlike 4.0
- License text:
  https://creativecommons.org/licenses/by-sa/4.0/

## Modifications

Documentation files were downloaded and processed
for use in the SecureDev AI knowledge base.

The processing pipeline cleans Markdown text,
splits content into chunks, and generates embeddings
for semantic retrieval.

Processed documentation is stored separately from
the downloaded source files.

## Third-Party Rights

The original documentation and example code remain
subject to their respective licenses.

These licenses do not automatically apply to all
original SecureDev AI application code.
