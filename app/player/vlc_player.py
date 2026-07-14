import sys
import vlc


class VLCPlayer:
    def __init__(self, video_widget):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        self.video_widget = video_widget
        self._set_video_output()

    def _set_video_output(self):
        win_id = int(self.video_widget.winId())

        if sys.platform.startswith("linux"):
            self.player.set_xwindow(win_id)

        elif sys.platform == "win32":
            self.player.set_hwnd(win_id)

        elif sys.platform == "darwin":
            self.player.set_nsobject(win_id)

    def open(self, file_path):
        media = self.instance.media_new(file_path)
        self.player.set_media(media)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def is_playing(self):
        return self.player.is_playing()

    def get_length(self):
        return self.player.get_length()

    def get_time(self):
        return self.player.get_time()

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
        """Return the current media FPS or a safe default."""
        try:
            fps = self.player.get_fps()
            if fps and fps > 0:
                return fps
        except Exception:
            pass
        return 30

    def _frame_duration(self):
        return max(1, int(1000 / self.get_fps()))

    def next_frame(self):
        """Step one frame forward using native VLC support when available."""
        if hasattr(self.player, "next_frame"):
            try:
                self.player.next_frame()
                return
            except Exception:
                pass

        current = self.get_time()
        if current < 0:
            current = 0
        self.set_time(current + self._frame_duration())

    def previous_frame(self):
        """Step one frame backward using native VLC support when available."""
        if hasattr(self.player, "previous_frame"):
            try:
                self.player.previous_frame()
                return
            except Exception:
                pass

        current = self.get_time()
        if current <= 0:
            return
        self.set_time(max(0, current - self._frame_duration()))