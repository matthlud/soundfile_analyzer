import platform
import psutil
import socket
import pyaudio
import sounddevice as sd
import cv2

class HardwareInfo:
    def __init__(self):
        self.processor = platform.processor()
        self.system = platform.system()
        self.machine = platform.machine()
        self.memory = self.get_memory_info()
        self.disk = self.get_disk_info()
        self.network = self.get_network_info()
        self.audio_devices = self.get_audio_devices()
        self.camera_devices = self.get_camera_devices()

    def get_memory_info(self):
        mem = psutil.virtual_memory()
        memory_info = {
            'total': mem.total,
            'available': mem.available,
            'percent_used': mem.percent
        }
        return memory_info

    def get_disk_info(self):
        disk = psutil.disk_usage('/')
        disk_info = {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent_used': disk.percent
        }
        return disk_info

    def get_network_info(self):
        network_info = []
        for interface, data in psutil.net_if_addrs().items():
            interface_info = {
                'name': interface,
                'ipv4': [],
                'ipv6': []
            }
            for item in data:
                if item.family == socket.AF_INET:
                    interface_info['ipv4'].append(item.address)
                elif item.family == socket.AF_INET6:
                    interface_info['ipv6'].append(item.address)
            network_info.append(interface_info)
        return network_info

    def get_audio_devices(self):
        audio_info = sd.query_devices()
        audio_devices = {
            'input': [],
            'output': []
        }
        for device in audio_info:
            device_type = 'input' if device['max_input_channels'] > 0 else 'output'
            audio_devices[device_type].append(device['name'])
        return audio_devices

    def get_camera_devices(self):
        camera_info = []
        for i in range(0, 10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                camera_info.append(f"Camera {i}")
                cap.release()
        return camera_info

    def display_info(self):
        print("Processor:", self.processor)
        print("System:", self.system)
        print("Machine:", self.machine)
        print("\nMemory:")
        print("Total:", self.memory['total'], "bytes")
        print("Available:", self.memory['available'], "bytes")
        print("Percent Used:", self.memory['percent_used'], "%")
        print("\nDisk:")
        print("Total:", self.disk['total'], "bytes")
        print("Used:", self.disk['used'], "bytes")
        print("Free:", self.disk['free'], "bytes")
        print("Percent Used:", self.disk['percent_used'], "%")
        print("\nNetwork:")
        for interface in self.network:
            print("Interface:", interface['name'])
            print("IPv4 Addresses:", ', '.join(interface['ipv4']))
            print("IPv6 Addresses:", ', '.join(interface['ipv6']))
            print()
        print("\nAudio Devices:")
        print("Input Devices:", ', '.join(self.audio_devices['input']))
        print("Output Devices:", ', '.join(self.audio_devices['output']))
        print("\nCamera Devices:")
        print('\n'.join(self.camera_devices))

# Usage
info = HardwareInfo()
info.display_info()
