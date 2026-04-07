# Task 3.4: Parallel Frame Processing & GPU Config

## Description
Deepfake inference latency is heavily bottlenecked by sequential frame extraction and face detection. This task optimizes the vision pipeline using multiprocessing and explicit GPU decoding support where available.

## Files to Modify
- `Unified_Detection_App/modules/deepfake_detector.py` (or the equivalent Microservice implementation from Task 3.2)
- `Unified_Detection_App/requirements.txt`

## Implementation Steps
1. **Multiprocessing Threadpool**: Update the `_extract_frames` logic to utilize `concurrent.futures.ThreadPoolExecutor` to extract and process the $N$ required frames in parallel chunks rather than a single sequential loop.
2. **GPU Video Decoding (Optional/Advanced)**: If compiling OpenCV with CUDA support (`python3-opencv` with `cudacodec` enabled) or utilizing `ffmpeg` sub-processes, offload the video decoding to the NVENC/NVDEC silicon on the GPU.
3. **Batch Tensors**: Modify the face extraction logic (`face_recognition`) to collect cropped faces into a single contiguous PyTorch batch tensor (shape: `[Batch, Channels, Height, Width]`), sending it to the CNN in one forward pass rather than $N$ sequential passes.

## Validation Criteria
- [ ] The total duration from video upload to final inference result drops measurably (e.g., > 30% reduction).
- [ ] Resource monitoring shows CPU/GPU utilization spiking efficiently across cores rather than pegging a single core sequentially.
