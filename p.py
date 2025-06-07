import asyncio
import websockets
import threading
import time
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import keyboard

clients = set()

async def ws_handler(websocket, path):
    clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)

def start_ws_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(ws_handler, "localhost", 8765)
    loop.run_until_complete(start_server)
    loop.run_forever()


threading.Thread(target=start_ws_server, daemon=True).start()


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

prev_vol = volume.GetMasterVolumeLevel()

print("Сервер запущен. Нажми Scroll Lock для переключения режима перемотки.")

async def send_ws_message(message):
    if clients:
        await asyncio.wait([asyncio.create_task(ws.send(message)) for ws in clients])


rewind_mode = False
scroll_lock_prev = False

while True:
    time.sleep(0.1)

    # переключение
    if keyboard.is_pressed("scroll lock") and not scroll_lock_prev:
        rewind_mode = not rewind_mode
        scroll_lock_prev = True
        print("🔁 Режим перемотки:", "ВКЛ ✅" if rewind_mode else "ВЫКЛ ❌")
    elif not keyboard.is_pressed("scroll lock"):
        scroll_lock_prev = False

    current_vol = volume.GetMasterVolumeLevel()
    delta = current_vol - prev_vol

    vol_scalar = volume.GetMasterVolumeLevelScalar()
    if vol_scalar >= 0.99:
        print("🔊 Громкость была на 100%, сбрасываю до 98% для захвата прокрутки")
        volume.SetMasterVolumeLevelScalar(0.98, None)
        current_vol = volume.GetMasterVolumeLevel()  
    if rewind_mode and abs(delta) > 0.1:
        direction = "forward" if delta > 0 else "rewind"
        print(f"📤 Отправка команды: {direction}")
        
        asyncio.run(send_ws_message(direction))
        volume.SetMasterVolumeLevel(prev_vol, None)
    elif not rewind_mode:
        prev_vol = current_vol
