# run correctly
import asyncio
import comtypes
from comtypes import cast, POINTER, windll
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

if __name__ == "__main__":
    import sys
    import os
    # 獲取父目錄的絕對路徑
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../'*1)))
from library.manager import ModuleManager
from library.manager import environment_manager

class VolumeManager(ModuleManager):
    def __init__(self):
        self._volume_control_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._volume_control_loop)

        self._minimum_volume_limit: float = 0.3
        self._maximum_volume_limit: float = 0.5

        # Variable to check if the controller is running
        self._is_running: bool = False

        # Initialize COM at the beginning of your script
        comtypes.CoInitialize()

        # Get the audio output (speakers) device
        self._devices = AudioUtilities.GetSpeakers()

        # Activate the interface to control audio volume
        self._interface = self._devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self._volume = cast(self._interface, POINTER(IAudioEndpointVolume))

    async def volume_monitoring(self):
        while True:
            # Get the current volume level as a scalar (0.0 to 1.0)
            self.current_volume = self._volume.GetMasterVolumeLevelScalar()
            print("Current: " + str(self.current_volume) )

            if abs(round(self.current_volume - self._minimum_volume_limit, 2)) > 0.01:
                # Check if the current volume exceeds the minimum limit
                if self.current_volume < self._minimum_volume_limit:
                    # If it does, set the volume to the minimum limit
                    self._volume.SetMasterVolumeLevelScalar(self._minimum_volume_limit, None)
                    print("Mini limit start: " + str(self._minimum_volume_limit))

                # Check if the current volume exceeds the maximum limit
                if self.current_volume > self._maximum_volume_limit:
                    # If it does, set the volume to the maximum limit
                    self._volume.SetMasterVolumeLevelScalar(self._maximum_volume_limit, None)
                    print("Max limit start: " + str(self._maximum_volume_limit))

            # Wait for a period (1 second) before checking again
            await asyncio.sleep(1)  # Adjust volume every second

    def start(self):
        if self._is_running:
            return
        self._is_running = True

        if not environment_manager.is_admin():
            print("This script requires administrative privileges to modify audio settings.")
            return
        print("Volume monitoring started. Press Ctrl+C to stop.")

        asyncio.run_coroutine_threadsafe(self.volume_monitoring(), self._volume_control_loop)
        self._volume_control_loop.run_forever()

    def stop(self):
        if not self._is_running:
            return
        self._is_running = False

        self._volume_control_loop.stop()
        print()
        print("Volume monitoring stopped")

    def is_running(self):
        return self._is_running

volume_manager = VolumeManager()

if __name__ == "__main__":
    try:
        volume_manager.start()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")
    finally:
        volume_manager.stop()