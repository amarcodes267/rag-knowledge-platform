# Render Deployment Optimization - Progress Tracker


- [ ] 2. Optimize `backend/services/vector_store.py` - Move faiss, numpy, pickle imports inside methods
- [ ] 3. Optimize `backend/services/rag_service.py` - Move heavy service imports inside query() method
- [ ] 4. Optimize `backend/services/llm_service.py` - Move requests import inside methods
- [ ] 5. Optimize `backend/requirements.txt` - Remove unused packages
- [ ] 6. Optimize `render.yaml` - Remove --preload, update start command
