"""Optional PyTorch helpers. PyTorch is intentionally not a core dependency."""
def backend_status():
    try:
        import torch
        return {"available": True, "version": torch.__version__,
                "cuda_available": bool(torch.cuda.is_available()),
                "device": "cuda" if torch.cuda.is_available() else "cpu"}
    except ImportError:
        return {"available": False, "install": "Install a PyTorch build matching your OS/device from pytorch.org"}
