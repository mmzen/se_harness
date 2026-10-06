"""Explicit initialization or sandbox service start. Neither migrates on request."""
import argparse
import json
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["init", "serve", "ready"])
    parser.add_argument("--config", default=os.environ.get("HAG_CONFIG", "/run/config/config.json"))
    parser.add_argument("--credentials", default="/run/secrets/sandbox_credentials")
    args = parser.parse_args()
    if args.action == "serve":
        import uvicorn
        from .app import create_app
        # One process; synchronous database/evaluator handlers use bounded worker threads.
        uvicorn.run(create_app(args.config, args.credentials), host="0.0.0.0", port=8080, workers=1,
                    access_log=False, log_level="info", limit_concurrency=16)
    else:
        from .service import Service
        service = Service(json.loads(Path(args.config).read_text()), json.loads(Path(args.credentials).read_text()))
        try:
            result = service.store.initialize() if args.action == "init" else service.readiness()
            print(json.dumps(result, indent=2))
        finally:
            service.store.driver.close()


if __name__ == "__main__":
    main()
