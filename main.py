import os

# The decky plugin module is located at decky-loader/plugin
# For easy intellisense checkout the decky-loader code repo
# and add the `decky-loader/plugin/imports` path to `python.analysis.extraPaths` in `.vscode/settings.json`
import decky
import asyncio
import subprocess

PLUGIN_PATH = decky.DECKY_PLUGIN_DIR
BIN_PATH = os.path.join(decky.DECKY_PLUGIN_DIR, "bin")
WAV_PATH = os.path.join(decky.DECKY_PLUGIN_DIR, "dist/assets/cache.wav")

class Plugin:
    async def tts(self, text: str):
        try:
            decky.logger.info("Running TTS")
            command = f'echo "{text}" | {BIN_PATH}/piper/piper --model {BIN_PATH}/en_US-lessac-medium.onnx --debug --output_file {PLUGIN_PATH}/dist/assets/cache.wav'
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, command, output=stdout, stderr=stderr)
            decky.logger.info("TTS completed")
        except subprocess.CalledProcessError as e:
            decky.logger.error(f"Command failed with error: {e}")
            decky.logger.error(f"Return code: {e.returncode}")
            decky.logger.error(f"Output: {e.output}")
            decky.logger.error(f"Stderr: {e.stderr}")

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

    async def ocr_latest(self) -> dict:
        try:
            files = await self.get_file_list()
            decky.logger.info(f"files: {files}")
            # Get the latest file
            latest_file = files["output"].split("\n")[0]
            decky.logger.info(f"latest_file: {latest_file}")

            decky.logger.info("Running OCR")
            command = f"{BIN_PATH}/tesseract {latest_file} stdout -l eng"
            # Execute the command using subprocess.run
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            decky.logger.info(f"result: {result}")
            await self.tts(result.stdout)

            return {"status": "success", "output": result.stdout}
        except subprocess.CalledProcessError as e:
            decky.logger.error(f"Command failed with error: {e}")
            decky.logger.error(f"Return code: {e.returncode}")
            decky.logger.error(f"Output: {e.output}")
            decky.logger.error(f"Stderr: {e.stderr}")
            return {"status": "error", "output": str(e)}

    async def get_file_list(self) -> dict:
        try:
            decky.logger.info("Running 'find' command")
            command = "find /home/deck/Desktop/_Screenshot -type f -name '*.png'"
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

        # Check if /bin/piper exists
        if not os.path.exists(f"{BIN_PATH}/piper"):
            # Extract /bin/file to /bin
            command = f"tar -xvf {BIN_PATH}/piper_linux_x86_64.tar.gz -C {BIN_PATH}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            decky.logger.info(f"Extraction result: {result.stdout}")
        else:
            decky.logger.info("/bin/piper already exists, skipping extraction")

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
