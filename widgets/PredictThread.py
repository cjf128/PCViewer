from PySide6.QtCore import QThread, Signal

class PredictThread(QThread):
    finished = Signal()

    def __init__(self, predictor, predict_path, save_path):
        super().__init__()
        self.predictor = predictor
        self.predict_path = predict_path
        self.save_path = save_path

    def run(self):
        self.predictor.predict_from_files(
            self.predict_path,
            self.save_path,
            save_probabilities=True,
            overwrite=True,
            num_processes_preprocessing=2,
            num_processes_segmentation_export=2,
            folder_with_segs_from_prev_stage=None,
            num_parts=1,
            part_id=0
        )
        self.finished.emit()


