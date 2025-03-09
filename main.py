import base64
import os
import ssl
# The decky plugin module is located at decky-loader/plugin
# For easy intellisense checkout the decky-loader code repo
# and add the `decky-loader/plugin/imports` path to `python.analysis.extraPaths` in `.vscode/settings.json`
import decky
import asyncio
import subprocess
import aiohttp
import certifi
import hashlib

PLUGIN_PATH = decky.DECKY_PLUGIN_DIR
BIN_PATH = os.path.join(decky.DECKY_PLUGIN_DIR, "bin")
MODEL_PATH = '/tmp/rdfm'
WAV_PATH = '/tmp/rdfm/cache.wav'

model_map = {
    "chi_sim": {
        "tesseract": {
            "url": "https://github.com/tesseract-ocr/tessdata_fast/raw/refs/heads/main/chi_sim.traineddata",
            "filename": "chi_sim.traineddata",
            "sha256hash":"a5fcb6f0db1e1d6d8522f39db4e848f05984669172e584e8d76b6b3141e1f730"
        },
        "onnx": {
            "url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx?download=true",
            "filename": "zh_CN-huayan-medium.onnx",
            "sha256hash": "9929917bf8cabb26fd528ea44d3a6699c11e87317a14765312420be230be0f3d"
        },
        "onnx_json": {
            "url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx.json?download=true.json",
            "filename": "zh_CN-huayan-medium.onnx.json",
            "sha256hash": "d521dc45504a8ccc99e325822b35946dd701840bfb07e3dbb31a40929ed6a82b"
        }
    },
    "eng": {
        "tesseract": {
            "url": "https://github.com/tesseract-ocr/tessdata_fast/raw/refs/heads/main/eng.traineddata",
            "filename": "eng.traineddata",
            "sha256hash": "7d4322bd2a7749724879683fc3912cb542f19906c83bcc1a52132556427170b2"
        },
        "onnx": {
            "url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/amy/medium/en_US-amy-medium.onnx?download=true",
            "filename": "en_US-amy-medium.onnx",
            "sha256hash": "b3a6e47b57b8c7fbe6a0ce2518161a50f59a9cdd8a50835c02cb02bdd6206c18"
        },
        "onnx_json": {
            "url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/amy/medium/en_US-amy-medium.onnx.json?download=true.json",
            "filename": "en_US-amy-medium.onnx.json",
            "sha256hash": "95a23eb4d42909d38df73bb9ac7f45f597dbfcde2d1bf9526fdeaf5466977d77"
        }
    }
}

class Plugin:
    steamdir = "/home/deck/.local/share/Steam/"
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async def tts(self, text: str, lang: str = "eng") -> None:
        try:
            decky.logger.info("Running TTS")
            onnx_model = model_map[lang]["onnx"]["filename"]
            decky.logger.info(f"Using ONNX model: {onnx_model}")
            process = subprocess.Popen(
                [f'{BIN_PATH}/piper/piper', '--model', f'{MODEL_PATH}/{lang}/{onnx_model}', '--debug', '--output_file', f'{WAV_PATH}'],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            stdout, stderr = process.communicate(input=text)
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, process.args, output=stdout, stderr=stderr)
            decky.logger.info("TTS completed")
        except subprocess.CalledProcessError as e:
            decky.logger.error(f"TTS: Command failed with error: {e}")
            decky.logger.error(f"TTS: Return code: {e.returncode}")
            decky.logger.error(f"TTS: Output: {e.output}")
            decky.logger.error(f"TTS: Stderr: {e.stderr}")

        # Run the command
        try:
            decky.logger.info("Playing TTS")
            command = f'paplay {WAV_PATH}'
            subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            decky.logger.info("TTS playback completed")
        except subprocess.CalledProcessError as e:
            decky.logger.error(f"Command failed with error: {e}")
            decky.logger.error(f"Return code: {e.returncode}")
            decky.logger.error(f"Output: {e.output}")
            decky.logger.error(f"Stderr: {e.stderr}")

    # async def stop_tts(self) -> None:
    #     try:
    #         decky.logger.info("Stopping TTS")
    #         command = f'pkill -f paplay'
    #         subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
    #         decky.logger.info("TTS stopped")

    #     except subprocess.CalledProcessError as e:
    #         decky.logger.error(f"Command failed with error: {e}")
    #         decky.logger.error(f"Return code: {e.returncode}")
    #         decky.logger.error(f"Output: {e.output}")
    #         decky.logger.error(f"Stderr: {e.stderr}")
    #     except Exception as e:
    #         decky.logger.error(f"Error: {e}")

    async def delete_latest(self, path:str) -> dict:
        decky.logger.info("Delete Latest - Start")
        try:
            files = await self.get_file_list( path)
            decky.logger.info(f"DeleteLatest: Files: {files}")
            # Get the latest file
            latest_file = files["output"].split("\n")[0]
            decky.logger.info(f"DeleteLatest: Latest_file: {latest_file}")

            # Delete the file
            os.remove(latest_file)
            decky.logger.info(f"DeleteLatest: Deleted file: {latest_file}")

            return {"status": "success", "output": latest_file}
        except subprocess.CalledProcessError as e:
            decky.logger.error(f"DeleteLatest: Command failed with error: {e}")
            decky.logger.error(f"DeleteLatest: Return code: {e.returncode}")
            decky.logger.error(f"DeleteLatest: Output: {e.output}")
            decky.logger.error(f"DeleteLatest: Stderr: {e.stderr}")
            return {"status": "error", "output": str(e)}

    async def get_latest(self, path: str) -> dict:
        decky.logger.info("Get Latest - Start")
        try:
            files = await self.get_file_list( path)
            decky.logger.info(f"GetLatest: Files: {files}")
            # Get the latest file
            latest_file = files["output"].split("\n")[0]
            decky.logger.info(f"GetLatest: Latest_file: {latest_file}")

            with open(latest_file, "rb") as file:
                encoded_string = base64.b64encode(file.read()).decode('utf-8')
            # decky.logger.info(f"GetLatest: Base64: {encoded_string}")

            return {"status": "success", "output": latest_file, "base64": encoded_string}
        except subprocess.CalledProcessError as e:
            decky.logger.error(f"GetLatest: Command failed with error: {e}")
            decky.logger.error(f"GetLatest: Return code: {e.returncode}")
            decky.logger.error(f"GetLatest: Output: {e.output}")
            decky.logger.error(f"GetLatest: Stderr: {e.stderr}")
            return {"status": "error", "output": str(e)}

    async def ocr_latest(self, path: str, lang: str = "eng") -> dict:
        decky.logger.info("OCR Latest - Start")
        os.environ['TESSDATA_PREFIX'] = f"{MODEL_PATH}/{lang}"
        try:
            latest_file_info = await self.get_latest(path)
            if latest_file_info["status"] != "success":
                return latest_file_info

            latest_file = latest_file_info["output"]
            decky.logger.info(f"OCRLatest: Latest_file: {latest_file}")

            decky.logger.info("OCRLatest: Running OCR")
            command = f"{BIN_PATH}/tesseract {latest_file} stdout -l {lang} "
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            decky.logger.info(f"OCRLatest: Result: {result.stdout}")
            await self.tts(result.stdout, lang)

            return {"status": "success", "output": result.stdout}
        except subprocess.CalledProcessError as e:
            decky.logger.error(f"OCRLatest: Command failed with error: {e}")
            decky.logger.error(f"OCRLatest: Return code: {e.returncode}")
            decky.logger.error(f"OCRLatest: Output: {e.output}")
            decky.logger.error(f"OCRLatest: Stderr: {e.stderr}")
            return {"status": "error", "output": str(e)}


    async def get_file_list(self, path: str) -> dict:
        try:
            decky.logger.info("Running 'find' command")
            command = f"find {path} -type f -regex '.*\\.\(jpg\\|jpeg\\|png\\)$' ! -path '*/thumbnails/*' -printf '%T@ %p\n' | sort -nr | head -n 1 | cut -d' ' -f2- "
            decky.logger.info(f"Command: {command}")
            # Execute the command using subprocess.run
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            # Get the output and split by lines
            file_paths = result.stdout.strip().split("\n")
            # Log full file paths
            decky.logger.info(f"file_paths: {file_paths}")

            return {"status": "success", "output": result.stdout}
        except subprocess.CalledProcessError as e:
            decky.logger.error(f"Command failed with error: {e}")
            return {"status": "error", "output": str(e)}

    def file_matches_hash(self, file_path, expected_hash):
        decky.logger.info(f"Checking file hash for {file_path}")
        if not os.path.exists(file_path):
            return False
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        file_hash = sha256.hexdigest()
        decky.logger.info(f"File hash: {file_hash}")
        decky.logger.info(f"Expected hash: {expected_hash}")
        return file_hash == expected_hash

    async def check_lang_model(self, lang: str) -> dict:
        try:
            decky.logger.info(f"Checking language models for {lang}")
            lang_dir = os.path.join(MODEL_PATH, lang)
            os.makedirs(lang_dir, exist_ok=True)
            model_files = model_map[lang]
            files_to_download = [
                model_files["tesseract"],
                model_files["onnx"], 
                model_files["onnx_json"]
            ]
            lang_status = {}
            for model in files_to_download:
                model_file = model["filename"]
                output_path = os.path.join(lang_dir, model_file)
                decky.logger.info(f"Checking {model_file} at {output_path}")
                if os.path.exists(output_path) and self.file_matches_hash(output_path, model["sha256hash"]):
                    decky.logger.info(f"File {model_file} exists and matches the hash")
                    lang_status[model_file] = True
                else:
                    decky.logger.info(f"File {model_file} is missing or does not match the hash")
                    lang_status[model_file] = False
                decky.logger.info(f"Model: {model_file} - Status: {lang_status[model_file]}")
            
            decky.logger.info(f"Language: {lang} - Status: {lang_status}")
            return {"status": "success", "output": lang_status}
        except Exception as e:
            decky.logger.error(f"Error: {e}")
            return {"status": "error", "output": str(e)}

    async def download_lang_model(self, lang: str) -> dict:
        try:
            model_files = model_map[lang]
            files_to_download = [
                model_files["tesseract"],
                model_files["onnx"], 
                model_files["onnx_json"]
            ]

            lang_dir = os.path.join(MODEL_PATH, lang)
            os.makedirs(lang_dir, exist_ok=True)


            for model in files_to_download:
                model_url = model["url"]
                model_file = model["filename"]
                expected_hash = model["sha256hash"]
                output_path = os.path.join(lang_dir, model_file)

                if self.file_matches_hash(output_path, expected_hash):
                    decky.logger.info(f"File {model_file} already exists and matches the hash. Skipping download.")
                    continue

                decky.logger.info(f"Downloading {model_file} from {model_url} to {output_path}")

                last_progress = 0
                async with aiohttp.ClientSession() as session:
                    async with session.get(model_url, ssl=self.ssl_context) as res:
                        res.raise_for_status()
                        total_size = int(res.headers.get('Content-Length', 0))
                        downloaded_size = 0
                        with open(output_path, "wb") as file:
                            async for chunk in res.content.iter_chunked(1024):
                                file.write(chunk)
                                downloaded_size += len(chunk)
                                progress = (downloaded_size / total_size) * 100
                                if progress - last_progress > 1:
                                    last_progress = progress
                                    decky.logger.info(f"Downloading {model_file}: {int(progress)}%")

                decky.logger.info(f"Downloaded {model_file}")

            return {"status": "success", "output": f"Downloaded language model for '{lang}'"}
        except subprocess.CalledProcessError as e:
            decky.logger.error(f"Command failed with error: {e}")
            decky.logger.error(f"Return code: {e.returncode}")
            decky.logger.error(f"Output: {e.output}")
            decky.logger.error(f"Stderr: {e.stderr}")
            return {"status": "error", "output": str(e)}
        except ValueError as e:
            decky.logger.error(f"Error: {e}")
            return {"status": "error", "output": str(e)}


    async def backend_addition(self, parameter_a: int, parameter_b: int) -> str:
        return str(parameter_a + parameter_b)

    async def long_running(self):
        await asyncio.sleep(15)
        # Passing through a bunch of random data, just as an example
        await decky.emit("toast_event", "Hello from the backend!", True, 2)

    async def _main(self):
        self.loop = asyncio.get_event_loop()

        # Check if /bin/piper exists
        if not os.path.exists(f"{BIN_PATH}/piper"):
            # Extract /bin/file to /bin
            command = f"tar -xvf {BIN_PATH}/piper_linux_x86_64.tar.gz -C {BIN_PATH}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            decky.logger.info(f"Extraction result: {result.stdout}")
        else:
            decky.logger.info("/bin/piper already exists, skipping extraction")

        # Player: Set the XDG_RUNTIME_DIR environment variable
        os.environ['XDG_RUNTIME_DIR'] = "/run/user/1000"

        decky.logger.info("Hello World!")

    async def _unload(self):
        decky.logger.info("Goodnight World!")
        pass

    async def _uninstall(self):
        decky.logger.info("Goodbye World!")
        pass

    async def start_timer(self):
        self.loop.create_task(self.long_running())

    async def _migration(self):
        decky.logger.info("Migrating")
        decky.migrate_logs(os.path.join(decky.DECKY_USER_HOME, ".config", "decky-template", "template.log"))
        decky.migrate_settings(
            os.path.join(decky.DECKY_HOME, "settings", "template.json"),
            os.path.join(decky.DECKY_USER_HOME, ".config", "decky-template"))
        decky.migrate_runtime(
            os.path.join(decky.DECKY_HOME, "template"),
            os.path.join(decky.DECKY_USER_HOME, ".local", "share", "decky-template"))
