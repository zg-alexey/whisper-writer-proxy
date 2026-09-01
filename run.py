import logging
import os
import subprocess
import sys
import uuid
from pathlib import Path

from dotenv import load_dotenv


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    log_dir = script_dir / "logs"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "whisper-writer.log"
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filemode="a",
        encoding="utf-8",
        force=True,
    )

    session_id = uuid.uuid4().hex[:8]
    logging.info(
        "=== WhisperWriter session %s starting (launcher_pid=%s, python=%s) ===",
        session_id,
        os.getpid(),
        sys.executable,
    )
    load_dotenv(script_dir / ".env")
    logging.info(
        "Environment: OPENAI_API_KEY=%s, OPENAI_PROXY_URL=%s",
        "set" if os.getenv("OPENAI_API_KEY") else "missing",
        "set" if os.getenv("OPENAI_PROXY_URL") else "missing",
    )

    child_env = os.environ.copy()
    child_env["PYTHONUNBUFFERED"] = "1"
    child_env["PYTHONIOENCODING"] = "utf-8"
    child_command = [sys.executable, str(script_dir / "src" / "main.py")]

    try:
        process = subprocess.Popen(
            child_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=script_dir,
            bufsize=1,
            env=child_env,
        )
        logging.info("Application process started (pid=%s)", process.pid)
    except Exception:
        logging.exception("Failed to launch WhisperWriter")
        raise

    assert process.stdout is not None
    try:
        for line in process.stdout:
            logging.info("[app] %s", line.rstrip())
    except Exception:
        logging.exception("Error while streaming WhisperWriter output")
    finally:
        process.stdout.close()

    return_code = process.wait()
    logging.info(
        "=== WhisperWriter session %s exited with code %s ===",
        session_id,
        return_code,
    )
    if return_code:
        sys.exit(return_code)


if __name__ == "__main__":
    main()
