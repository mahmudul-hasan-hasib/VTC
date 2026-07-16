import json


class SessionService:

    @staticmethod
    def save(session, filename):

        data = {
            "video_path": session.video_path,
            "incoming": session.incoming,
            "outgoing": session.outgoing,
            "notes": session.notes
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load(filename):

        with open(filename) as f:
            return json.load(f)