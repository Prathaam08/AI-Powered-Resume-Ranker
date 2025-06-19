document.addEventListener('DOMContentLoaded', function() {
    // Auto-resize textarea for job description
    const jobDescTextarea = document.getElementById('job_desc');
    if (jobDescTextarea) {
        jobDescTextarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
        
        // Trigger initial resize
        setTimeout(() => {
            jobDescTextarea.dispatchEvent(new Event('input'));
        }, 100);
    }
    
    // Add file names to upload input
    const resumeInput = document.getElementById('resumes');
    if (resumeInput) {
        resumeInput.addEventListener('change', function() {
            const fileNames = Array.from(this.files).map(file => file.name).join(', ');
            const label = this.nextElementSibling;
            if (label && label.classList.contains('form-text')) {
                label.textContent = fileNames || 'Select multiple files using Ctrl+Click or Cmd+Click';
            }
        });
    }
});