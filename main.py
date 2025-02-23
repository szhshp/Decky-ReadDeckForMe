import os

# The decky plugin module is located at decky-loader/plugin
# For easy intellisense checkout the decky-loader code repo
# and add the `decky-loader/plugin/imports` path to `python.analysis.extraPaths` in `.vscode/settings.json`
import decky
import asyncio
import subprocess
import base64

PLUGIN_PATH = decky.DECKY_PLUGIN_DIR
BIN_PATH = os.path.join(decky.DECKY_PLUGIN_DIR, "bin")

class Plugin:
    async def tts(self, text: str):
        # Run the command
        try:

            decky.logger.info("Running TTS125")
            command = f'echo "12345682" | {BIN_PATH}/piper/piper --model {BIN_PATH}/zh_CN-huayan-medium.onnx --output_file {PLUGIN_PATH}/dist/assets/cache.wav'
            try:
                await subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            except subprocess.CalledProcessError as e:
                decky.logger.error(f"Command failed with error: {e}")
                decky.logger.error(f"Return code: {e.returncode}")
                decky.logger.error(f"Output: {e.output}")
                decky.logger.error(f"Stderr: {e.stderr}")
            decky.logger.info("TTS completed")


            # decky.logger.info("Playing audio")
            # # Play the audio
            # command = f'aplay -r 22050 -f S16_LE -t raw {BIN_PATH}/cache.wav'
            # await subprocess.run(command, shell=True, capture_output=True, text=True, check=True)

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
            command = f"{BIN_PATH}/tesseract {latest_file} stdout -l chi_sim"
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

    async def get_latest_file(self) -> dict:
        decky.logger.info(f"123123")
        try:
            files = await self.get_file_list()
            decky.logger.info(f"files: {files}")
            # Get the latest file
            latest_file = files["output"].split("\n")[0]
            decky.logger.info(f"latest_file: {latest_file}")

            # Read the file content and encode it in base64
            with open(latest_file, "rb") as file:
                file_content = file.read()
                file_base64 = base64.b64encode(file_content).decode('utf-8')
            
            decky.logger.info(f"file_base64: {file_base64}")

            return {"status": "success", "output": latest_file, "base64": file_base64}
        except subprocess.CalledProcessError as e:
            decky.logger.error(f"Command failed with error: {e}")
            return {"status": "error", "output": str(e)}
        except Exception as e:
            decky.logger.error(f"An error occurred: {e}")
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

        # # Check if /bin/piper exists
        # if not os.path.exists(f"{BIN_PATH}/piper"):
        #     # Extract /bin/file to /bin
        #     command = f"tar -xvf {BIN_PATH}/piper_linux_x86_64.tar.gz -C {BIN_PATH}"
        #     result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        #     decky.logger.info(f"Extraction result: {result.stdout}")
        # else:
        #     decky.logger.info("/bin/piper already exists, skipping extraction")

        # Set the TESSDATA_PREFIX environment variable
        # os.environ['TESSDATA_PREFIX'] = BIN_PATH
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
