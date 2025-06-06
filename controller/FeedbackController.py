import csv
import threading
import time
from datetime import datetime

from .GoogleSheetController import GoogleSheetController

class FeedbackController:
    def __init__(self, delta_time=30):
        creds_path = "/etc/secrets/rugged-filament-455205-m2-4e0d0bd3ebf9.json"
        sheet_id = "1NziTHdKPEoYNoEt9RgYl-j8SQKFSd9Jv706xA-Wb4mI"

        self.sheet_controller_react = GoogleSheetController(creds_path, sheet_id, "Feedbacks")
        self.sheet_controller_text = GoogleSheetController(creds_path, sheet_id, "Feedback-texts")
        
        self.batch = []
        self.lock = threading.Lock()
        self.delta_time = delta_time
        # self.last_updated = time.time()
        # self.flush_thread = threading.Thread(target=self._auto_flush, daemon=True)
        # self.flush_thread.start()

    def log_feedback(self, platform, sender_id, message_id, bot_reply, reaction, emoji):
        feedback_entry = [platform, sender_id, message_id, bot_reply, reaction, emoji, datetime.now().isoformat()]
        self.sheet_controller_react.append_row(feedback_entry)

    def log_feedback_text(self, platform, sender_id, feedback_text):
        # Save feedback text as a special type of feedback
        self.sheet_controller_text.append_row([
            platform,
            sender_id,
            feedback_text,
            datetime.now().isoformat()
        ])

    def remove_feedback(self, message_id):
        row = self.sheet_controller_react.find_row_by_cell_value(message_id)
        if row:
            self.sheet_controller_react.delete_row(row)


    # def _flush(self):
    #     with self.lock:
    #         if self.batch:
    #             for entry in self.batch:
    #                 self.sheet_controller.append_row(entry)
    #             self.batch.clear()
    #             print(f"[FeedbackManager] Flushed feedback batch to Google Sheet.")

    # def _auto_flush(self):
    #     while True:
    #         time.sleep(5)
    #         with self.lock:
    #             if self.batch and (time.time() - self.last_updated > self.delta_time):
    #                 self._flush()
