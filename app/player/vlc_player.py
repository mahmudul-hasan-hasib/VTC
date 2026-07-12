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