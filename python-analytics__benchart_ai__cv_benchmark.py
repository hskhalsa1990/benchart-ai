from __future__ import annotations
import time

def image_pipeline_benchmark(image_path: str, size: tuple[int, int] = (640, 640), iterations: int = 20) -> dict:
    try:
        import cv2
    except ImportError as exc:
        raise RuntimeError("OpenCV is optional. Install opencv-python to use this endpoint.") from exc
    if iterations < 1 or iterations > 1000:
        raise ValueError("iterations must be between 1 and 1000")
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image could not be read")
    start = time.perf_counter()
    for _ in range(iterations):
        _ = cv2.resize(image, size)
    elapsed = time.perf_counter() - start
    avg_ms = elapsed * 1000 / iterations
    return {"iterations": iterations, "width": size[0], "height": size[1],
            "average_ms": avg_ms, "fps": 1000 / avg_ms if avg_ms else None}
