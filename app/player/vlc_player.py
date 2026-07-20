import sys
import time
import vlc


class VLCPlayer:
    def __init__(self, video_widget):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.video_widget = video_widget
        self._fps = 30.0
        self._media_loaded = False
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
        self._media_loaded = False
        self._fps = 30.0
        self._set_video_output()
        media = self.instance.media_new(file_path)
        media.parse_with_options(vlc.MediaParseFlag.local, 5000)
        deadline = time.time() + 5.0
        while time.time() < deadline:
            parsed_status = media.get_parsed_status()
            if parsed_status in (
                vlc.MediaParsedStatus.done,
                vlc.MediaParsedStatus.failed,
                vlc.MediaParsedStatus.skipped,
                vlc.MediaParsedStatus.timeout,
            ):
                break
            time.sleep(0.01)
        self.player.set_media(media)
        self._detect_fps(media)
        self._media_loaded = True

    def _detect_fps(self, media):
        try:
            tracks = media.tracks_get()
            if tracks is not None:
                for track in tracks:
                    if track.type == vlc.TrackType.video:
                        fps = track.frame_rate
                        if fps and fps > 0:
                            self._fps = float(fps) / 1000.0 if fps > 1000 else float(fps)
                            return
        except Exception:
            pass
        try:
            result = self.player.get_fps()
            if result and result > 0:
                self._fps = float(result)
                return
        except Exception:
            pass
        self._fps = 30.0

    @property
    def fps(self):
        try:
            result = self.player.get_fps()
            if result and result > 0:
                self._fps = float(result)
        except Exception:
            pass
        return self._fps

    def _frame_duration_ms(self):
        fps = self.fps
        if fps <= 0:
            fps = 30.0
        return max(1, int(1000.0 / fps))

    def play(self):
        if not self._media_loaded:
            return
        self.player.play()

    def pause(self):
        state = self.player.get_state()
        if state in (vlc.State.Playing, vlc.State.Paused):
            self.player.pause()

    def stop(self):
        self.player.stop()

    def play_pause(self):
        if self.is_playing():
            self.pause()
        else:
            self.play()

    def is_playing(self):
        return self.player.is_playing()

    def is_stopped(self):
        return self.player.get_state() == vlc.State.Stopped

    def get_state(self):
        return self.player.get_state()

    def get_length(self):
        length = self.player.get_length()
        return max(length, 0)

    def get_time(self):
        t = self.player.get_time()
        return max(t, 0)

    def set_time(self, ms):
        self.player.set_time(max(0, int(ms)))

    def set_position(self, pos):
        self.player.set_position(max(0.0, min(1.0, pos)))

    def get_position(self):
        return self.player.get_position()

    def set_speed(self, speed):
        self.player.set_rate(max(0.25, min(6.0, speed)))

    def get_speed(self):
        return self.player.get_rate()

    def next_frame(self):
        state = self.player.get_state()
        was_playing = state == vlc.State.Playing
        if was_playing:
            self.player.pause()
            time.sleep(0.03)
        current_time = self.get_time()
        step = self._frame_duration_ms()
        new_time = min(self.get_length(), current_time + step)
        self.player.set_time(new_time)
        if was_playing:
            self.player.pause()

    def previous_frame(self):
        state = self.player.get_state()
        was_playing = state == vlc.State.Playing
        if was_playing:
            self.player.pause()
            time.sleep(0.03)
        current_time = self.get_time()
        step = self._frame_duration_ms()
        new_time = max(0, current_time - step)
        self.player.set_time(new_time)
        if was_playing:
            self.player.pause()

    def get_volume(self):
        return self.player.audio_get_volume()

    def set_volume(self, vol):
        self.player.audio_set_volume(max(0, min(200, vol)))
