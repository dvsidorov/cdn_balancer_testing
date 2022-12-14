import os

from app import app

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000,
            auto_reload=True,
            workers=int(os.getenv('BALANCER_WORKERS', os.cpu_count())))
