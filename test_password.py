from backend.app.core.security import verify_password

hashed = "$2b$12$ln87xiSoBulBPC45cnelJ.BPzA.Wenz6AMLIldSq1Y4vZWraXcMl2"

print(verify_password("Reddy@1425", hashed))
