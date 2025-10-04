import logging
import os
import subprocess
import sys
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
        filemode="w",
        force=True,
    )

    logging.info("Starting WhisperWriter…")
    load_dotenv()

    try:
        process = subprocess.Popen(
            [sys.executable, os.path.join("src", "main.py")],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=script_dir,
            bufsize=1,
        )
    except Exception:
        logging.exception("Failed to launch WhisperWriter")
        raise

    assert process.stdout is not None
    try:
        for line in process.stdout:
            logging.info(line.rstrip())
    except Exception:
        logging.exception("Error while streaming WhisperWriter output")
    finally:
        process.stdout.close()

    return_code = process.wait()
    logging.info("WhisperWriter exited with code %s", return_code)
    if return_code:
        sys.exit(return_code)


if __name__ == "__main__":
    main()
