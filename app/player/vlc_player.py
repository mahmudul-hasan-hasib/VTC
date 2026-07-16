import sys
import time
import vlc


class VLCPlayer:
    def __init__(self, video_widget):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.video_widget = video_widget
        self._set_video_output()
        self._is_playing = False
        self._was_paused = False

    def _set_video_output(self):
        win_id = int(self.video_widget.winId())
        if sys.platform.startswith("linux"):
            self.player.set_xwindow(win_id)
        elif sys.platform == "win32":
            self.player.set_hwnd(win_id)
        elif sys.platform == "darwin":
            self.player.set_nsobject(win_id)

    def open(self, file_path):
        if isinstance(file_path, str):
            file_path = file_path.encode('utf-8')
        if isinstance(file_path, bytes):
            file_path = file_path.decode('utf-8')
        media = self.instance.media_new(file_path)
        self.player.set_media(media)

    def play(self):
        self.player.play()
        self._is_playing = True
        self._was_paused = False

    def pause(self):
        self.player.pause()
        self._is_playing = self.player.is_playing()
        self._was_paused = True

    def play_pause(self):
        if self.is_playing():
            self.pause()
        else:
            self.play()

    def stop(self):
        self.player.stop()
        self._is_playing = False
        self._was_paused = False

    def is_playing(self):
        return self.player.is_playing()

    def get_length(self):
        length = self.player.get_length()
        return max(length, 0)

    def get_time(self):
        time = self.player.get_time()
        return max(time, 0)

    def set_time(self, ms):
        self.player.set_time(ms)

    def set_position(self, pos):
        self.player.set_position(pos)

    def get_position(self):
        return self.player.get_position()

    def set_speed(self, speed):
        self.player.set_rate(speed)

    def get_speed(self):
        return self.player.get_rate()

    def get_fps(self):
        try:
            # Try to get fps via VLC API
            media = self.player.get_media()
            if media is not None:
                tracks = media.get_Tracks()
                for track in tracks:
                    if track.type == 'video':
                        fps = track.get_frameRate()
                        if fps:
                            return fps
            # Fallback: use fps command
            result = self.player.get_fps()
            if result and result > 0:
                return result
        except Exception:
            pass
        return 30.0

    def _frame_duration(self):
        return max(1, int(1000 / self.get_fps()))

    def next_frame(self):
        # Peaceful mode: pause then step one frame
        was_playing = self.is_playing()
        try:
            self.player.play()
            passed = 0
            start_time = time.time()
            orig_time = self.get_time()
            self.player.next_frame()
            while self.get_time() <= orig_time and passed < 1000:
                for _ in range(10):
                    pass
                passed = (time.time() - start_time) * 1000
            if not was_playing:
                self.player.pause()
        except:
            current = self.get_time()
            if current < 0:
                current = 0
            duration = self._frame_duration()
            self.set_time(current + duration)
            if not was_playing:
                self.player.pause()

    def previous_frame(self):
        # Step one frame backward
        # VLC does not directly support previous_frame for non-stream, so we seek
        was_playing = self.is_playing()
        self.player.pause()
        if self.get_time() < self._frame_duration():
            self.set_time(0)
            return
        self.set_time(self.get_time() - self._frame_duration())
        if not was_playing:
            self.player.pause()
