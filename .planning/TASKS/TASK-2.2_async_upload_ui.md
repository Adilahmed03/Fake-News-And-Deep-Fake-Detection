# Task 2.2: Asynchronous Upload UI

## Description
Deepfake video analysis can take minutes, causing standard synchronous HTTP POST form submissions to time out or freeze the user's browser. Implement an asynchronous (AJAX/Fetch API) upload pipeline with visual feedback.

## Files to Modify
- `Unified_Detection_App/templates/deepfake.html`
- `Unified_Detection_App/static/js/main.js` (or inline scripts in the template)
- `Unified_Detection_App/static/css/style.css`

## Implementation Steps
1. **Frontend Hijack**: Prevent the default `<form>` submission event on the deepfake analysis form.
2. **AJAX Upload**: Use the `Fetch` API or `XMLHttpRequest` to send the `FormData` containing the video file to `/api/detect/deepfake`.
3. **Loading State UI**: 
   - Hide the "Analyze" button upon click.
   - Display a spinner or progress bar visualization.
   - Show status text (e.g., "Uploading...", "Analyzing frames (this may take a few minutes)...").
4. **Response Handling**:
   - On HTTP 200 SUCCESS, dynamically render the prediction label (Fake vs Real) and confidence score without reloading the page, or redirect programmatically to `/result/deepfake` passing state via `localStorage` or URL params.
   - On ERROR, hide the loading state and display a user-friendly error toast or banner.

## Validation Criteria
- [ ] Submitting a 50MB video does not freeze the UI or the browser tab during processing.
- [ ] Visual loading indicators correctly map to the pending API request state.
- [ ] Server errors (like unsupported formats) are handled gracefully and displayed to the user without dropping them to an empty JSON screen.
