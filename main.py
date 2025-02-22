import os

# The decky plugin module is located at decky-loader/plugin
# For easy intellisense checkout the decky-loader code repo
# and add the `decky-loader/plugin/imports` path to `python.analysis.extraPaths` in `.vscode/settings.json`
import decky
import asyncio
import subprocess

class Plugin:
    async def ocr_latest(self) -> dict:
        try:
            files = await self.get_file_list()
            decky.logger.info(f"files: {files}")
            # Get the latest file
            latest_file = files["output"].split("\n")[0]
            decky.logger.info(f"latest_file: {latest_file}")

            decky.logger.info("Running OCR")
            # TODO: Move tesseract to bin
            command = f"/home/deck/Downloads/tesseract {latest_file} /home/deck/homebrew/data/decky-rifm/cache -l chi_sim"
            # Execute the command using subprocess.run
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            decky.logger.info(f"result: {result}")

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
            command = "find /home/deck/Desktop/_Screenshot -type f -name '*.png' "
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

    # # A normal method. It can be called from the TypeScript side using @decky/api.
    # async def add(self, left: int, right: int) -> int:
    #     decky.logger.info("33333333")
    #     return left + right

    # async def add2(self, left: int, right: int) -> int:
    #     decky.logger.info("22222229")
    #     return 19

    async def long_running(self):
        await asyncio.sleep(15)
        # Passing through a bunch of random data, just as an example
        await decky.emit("timer_event", "Hello from the backend!", True, 2)

    # Asyncio-compatible long-running code, executed in a task when the plugin is loaded
    async def _main(self):
        self.loop = asyncio.get_event_loop()

        # Set the TESSDATA_PREFIX environment variable
        # TODO: change data path
        os.environ['TESSDATA_PREFIX'] = '/home/deck/Downloads/tessdata'
        decky.logger.info("Hello World!")

    # Function called first during the unload process, utilize this to handle your plugin being stopped, but not
    # completely removed
    async def _unload(self):
        decky.logger.info("Goodnight World!")
        pass

    # Function called after `_unload` during uninstall, utilize this to clean up processes and other remnants of your
    # plugin that may remain on the system
    async def _uninstall(self):
        decky.logger.info("Goodbye World!")
        pass

    async def start_timer(self):
        self.loop.create_task(self.long_running())

    # Migrations that should be performed before entering `_main()`.
    async def _migration(self):
        decky.logger.info("Migrating")
        # Here's a migration example for logs:
        # - `~/.config/decky-template/template.log` will be milgrated to `decky.decky_LOG_DIR/template.log`
        decky.migrate_logs(os.path.join(decky.DECKY_USER_HOME,
                                               ".config", "decky-template", "template.log"))
        # Here's a migration example for settings:
        # - `~/homebrew/settings/template.json` is migrated to `decky.decky_SETTINGS_DIR/template.json`
        # - `~/.config/decky-template/` all files and directories under this root are migrated to `decky.decky_SETTINGS_DIR/`
        decky.migrate_settings(
            os.path.join(decky.DECKY_HOME, "settings", "template.json"),
            os.path.join(decky.DECKY_USER_HOME, ".config", "decky-template"))
        # Here's a migration example for runtime data:
        # - `~/homebrew/template/` all files and directories under this root are migrated to `decky.decky_RUNTIME_DIR/`
        # - `~/.local/share/decky-template/` all files and directories under this root are migrated to `decky.decky_RUNTIME_DIR/`
        decky.migrate_runtime(
            os.path.join(decky.DECKY_HOME, "template"),
            os.path.join(decky.DECKY_USER_HOME, ".local", "share", "decky-template"))