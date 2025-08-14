// Get references to the DOM elements
const questionInput = document.getElementById('question-input');
const askButton = document.getElementById('ask-button');
const responseOutput = document.getElementById('response-output');
const loadingIndicator = document.getElementById('loading');

// --- Event Listener ---
askButton.addEventListener('click', handleApiCall); // Renamed function for clarity

// Add listener for Enter key in textarea (optional convenience)
questionInput.addEventListener('keypress', function (e) {
    // Check if Enter is pressed (without Shift, which usually means new line)
    // Allow Shift+Enter for multiline input
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault(); // Prevent default Enter behavior (new line)
        handleApiCall(); // Trigger the button click function
    }
});


// --- Function to Handle API Call ---
async function handleApiCall() {
    const inputText = questionInput.value.trim(); // Changed variable name

    if (!inputText) {
        responseOutput.innerHTML = '<p style="color: red;">Please enter text to validate.</p>';
        return;
    }

    // Show loading indicator and clear previous response
    loadingIndicator.style.display = 'block';
    responseOutput.innerHTML = ''; // Clear previous content
    askButton.disabled = true; // Disable button during request

    try {
        // ***** IMPORTANT: Adjust the URL to your specific endpoint *****
        const apiUrl = '/examples/books';

        // ***** IMPORTANT: Adjust the request body structure *****
        // This assumes your GenerateDrValidator model expects a field named 'text_to_validate'.
        // Change 'text_to_validate' to the actual field name(s) required by your Pydantic model.
        const requestBody = {
            query: inputText
            // Add other fields required by GenerateDrValidator if necessary
            // e.g., some_other_field: "some value"
        };

        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        // Improved error handling to get details from FastAPI
        if (!response.ok) {
            let errorDetail = `HTTP error! Status: ${response.status}`;
            try {
                 // FastAPI often returns error details in JSON format
                 const errorData = await response.json();
                 // Use the 'detail' field if it exists, otherwise stringify the whole error object
                 errorDetail = errorData.detail || JSON.stringify(errorData);
            } catch (e) {
                 // If response is not JSON or reading JSON fails
                 errorDetail += ` - ${response.statusText || 'Could not retrieve error details'}`;
            }
            throw new Error(errorDetail); // Throw an error with the detailed message
        }

        const data = await response.json();

        // ***** IMPORTANT: Adjust the response parsing *****
        // This assumes the markdown result is in a key named 'answer'.
        // Change 'answer' to the actual key name returned by your endpoint.
        if (data && data.answer) {
            // Render the Markdown to HTML using marked.js
            const rawHtml = marked.parse(data.answer);
            // Sanitize the HTML before inserting it into the DOM (Security)
            const cleanHtml = DOMPurify.sanitize(rawHtml);
            responseOutput.innerHTML = cleanHtml;
        } else {
            // Handle cases where the expected key is missing or the response structure is different
            console.warn("Received response data structure might be unexpected:", data);
            responseOutput.innerHTML = '<p style="color: orange;">Received a response, but could not find the expected answer field.</p>';
        }

    } catch (error) {
        console.error('Error calling API or processing result:', error);
        // Display the potentially detailed error message from the 'throw new Error' above
        // Sanitize error message before displaying
        responseOutput.innerHTML = DOMPurify.sanitize(`<p style="color: red;">Error: ${error.message}</p>`);
    } finally {
        // Hide loading indicator and re-enable button
        loadingIndicator.style.display = 'none';
        askButton.disabled = false;
    }
}