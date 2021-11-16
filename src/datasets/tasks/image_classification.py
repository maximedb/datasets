from dataclasses import dataclass
from typing import ClassVar, Dict, Optional, Tuple

from ..features import ClassLabel, Features, Value
from .base import TaskTemplate


@dataclass(frozen=True)
class ImageClassification(TaskTemplate):
    task: str = "image-classification"
    input_schema: ClassVar[Features] = Features({"image_file_path": Value("string")})
    # TODO(lewtun): Find a more elegant approach without descriptors.
    label_schema: ClassVar[Features] = Features({"labels": ClassLabel})
    image_file_path_column: str = "image_file_path"
    label_column: str = "labels"
    labels: Optional[Tuple[str]] = None

    def __post_init__(self):
        if self.labels:
            if len(self.labels) != len(set(self.labels)):
                raise ValueError("Labels must be unique")
            # Cast labels to tuple to allow hashing
            self.__dict__["labels"] = tuple(sorted(self.labels))
            self.__dict__["label_schema"] = self.label_schema.copy()
            self.label_schema["labels"] = ClassLabel(names=self.labels)

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {
            self.image_file_path_column: "image_file_path",
            self.label_column: "labels",
        }
