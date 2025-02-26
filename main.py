import base64
import os

# The decky plugin module is located at decky-loader/plugin
# For easy intellisense checkout the decky-loader code repo
# and add the `decky-loader/plugin/imports` path to `python.analysis.extraPaths` in `.vscode/settings.json`
import decky
import asyncio
import subprocess

PLUGIN_PATH = decky.DECKY_PLUGIN_DIR
BIN_PATH = os.path.join(decky.DECKY_PLUGIN_DIR, "bin")
WAV_PATH = os.path.join(decky.DECKY_PLUGIN_DIR, "dist/cache.wav")

class Plugin:
    async def tts(self, text: str):
        try:
            decky.logger.info("Running TTS")
            process = subprocess.Popen(
                [f'{BIN_PATH}/piper/piper', '--model', f'{BIN_PATH}/en_GB-alba-medium.onnx', '--debug', '--output_file', f'{WAV_PATH}'],
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

    async def delete_latest(self) -> dict:
        decky.logger.info("Delete Latest - Start")
        try:
            files = await self.get_file_list()
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

    async def get_latest(self) -> dict:
        decky.logger.info("Get Latest - Start")
        try:
            files = await self.get_file_list()
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

    async def ocr_latest(self) -> dict:
        decky.logger.info("OCR Latest - Start")
        try:
            latest_file_info = await self.get_latest()
            if latest_file_info["status"] != "success":
                return latest_file_info

            latest_file = latest_file_info["output"]
            decky.logger.info(f"OCRLatest: Latest_file: {latest_file}")

            decky.logger.info("OCRLatest: Running OCR")
            command = f"{BIN_PATH}/tesseract {latest_file} stdout -l eng"
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            decky.logger.info(f"OCRLatest: Result: {result.stdout}")
            await self.tts(result.stdout)

            return {"status": "success", "output": result.stdout}
        except subprocess.CalledProcessError as e:
            decky.logger.error(f"OCRLatest: Command failed with error: {e}")
            decky.logger.error(f"OCRLatest: Return code: {e.returncode}")
            decky.logger.error(f"OCRLatest: Output: {e.output}")
            decky.logger.error(f"OCRLatest: Stderr: {e.stderr}")
            return {"status": "error", "output": str(e)}


    async def get_file_list(self) -> dict:
        try:
            decky.logger.info("Running 'find' command")
            command = "find /home/deck/Desktop/_Screenshot -type f -name '*.png' | sort | tail -n 1"
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

    async def backend_addition(self, parameter_a: int, parameter_b: int) -> str:
        return str(parameter_a + parameter_b)

    async def long_running(self):
        await asyncio.sleep(15)
        # Passing through a bunch of random data, just as an example
        await decky.emit("timer_event", "Hello from the backend!", True, 2)

    async def _main(self):
        self.loop = asyncio.get_event_loop()

        # OCR: Set the TESSDATA_PREFIX environment variable
        os.environ['TESSDATA_PREFIX'] = BIN_PATH
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
