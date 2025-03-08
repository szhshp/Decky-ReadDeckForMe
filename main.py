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


PLUGIN_PATH = decky.DECKY_PLUGIN_DIR
BIN_PATH = os.path.join(decky.DECKY_PLUGIN_DIR, "bin")
MODEL_PATH = '/tmp/rifm'
WAV_PATH = '/tmp/rifm/cache.wav'

model_map = {
    "chi_sim": {
        "tesseract": {"url": "https://github.com/tesseract-ocr/tessdata/raw/refs/heads/main/chi_sim.traineddata", "filename": "chi_sim.traineddata"},
        "onnx": {"url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx?download=true", "filename": "zh_CN-huayan-medium.onnx"},
        "onnx_json": {"url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx.json?download=true.json", "filename": "zh_CN-huayan-medium.onnx.json"}
    },
    "eng": {
        "tesseract": {"url": "https://github.com/tesseract-ocr/tessdata/raw/refs/heads/main/eng.traineddata", "filename": "eng.traineddata"},
        "onnx": {"url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/amy/medium/en_US-amy-medium.onnx?download=true", "filename": "en_US-amy-medium.onnx"},
        "onnx_json": {"url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/amy/medium/en_US-amy-medium.onnx.json?download=true.json", "filename": "en_US-amy-medium.onnx.json"}
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
    
    async def download_lang_model(self, lang: str) -> dict:
        try:
            model_files = model_map[lang]
            files_to_download = [
                model_files["tesseract"],
                model_files["onnx"], 
                model_files["onnx_json"]
            ]

            lang_dir = os.path.join('/tmp/rifm', lang)
            os.makedirs(lang_dir, exist_ok=True)

            for model in files_to_download:
                model_url = model["url"]
                model_file = model["filename"]
                output_path = os.path.join(lang_dir, model_file)
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
