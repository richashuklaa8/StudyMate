const pdfFile = document.getElementById("pdfFile");
const fileName = document.getElementById("fileName");
const summarizeBtn = document.getElementById("summarizeBtn");
const summary = document.getElementById("summary");


// Show selected file name
pdfFile.addEventListener("change", () => {

    if (pdfFile.files.length > 0) {
        fileName.textContent = pdfFile.files[0].name;
    } else {
        fileName.textContent = "No file selected";
    }

});


// Generate summary
summarizeBtn.addEventListener("click", async () => {

    // Check if a PDF is selected
    if (pdfFile.files.length === 0) {
        summary.textContent = "Please choose a PDF file first.";
        return;
    }


    // Prepare PDF for sending to backend
    const formData = new FormData();
    formData.append("file", pdfFile.files[0]);


    // Loading state
    summarizeBtn.disabled = true;
    summarizeBtn.textContent = "⏳ Generating summary...";

    summary.textContent =
        "StudyMate is reading your PDF and creating your summary...";


    try {

        // Send PDF to Flask backend
        const response = await fetch(
            "https://studymate-05kf.onrender.com/summarize",git add frontend/script.js,
            {
                method: "POST",
                body: formData
            }
        );


        // Convert response to JSON
        const data = await response.json();


        // Check for errors
        if (!response.ok) {
            throw new Error(
                data.error || "Something went wrong."
            );
        }


        // Display AI summary
        summary.textContent = data.summary;


    } catch (error) {

        summary.textContent =
            "❌ " + error.message;

    } finally {

        // Reset button
        summarizeBtn.disabled = false;
        summarizeBtn.textContent =
            "✨ Generate Summary";

    }

});