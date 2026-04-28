from app import YumRushApp  
from services.db import initialize_database

if __name__ == "__main__":
    initialize_database()
    app = YumRushApp()
    app.mainloop()
