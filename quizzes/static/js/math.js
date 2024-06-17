(function() {
    // Render the math_text field using KaTeX
    const mathText = "{{ problem.math_text|escapejs }}";
    console.log(mathText);

    const extractDataValue = (htmlString) => {
        // Create a temporary DOM element to parse the HTML string
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = htmlString;

        // Find the span with the class 'ql-formula'
        const formulaSpan = tempDiv.querySelector('.ql-formula');

        // Extract the data-value attribute
        return formulaSpan ? formulaSpan.getAttribute('data-value') : null;
    };

    const mathTextRenderContainer = document.getElementById('math-text-{{ problem.id }}');
    const dataValue = extractDataValue(mathText);

    if (dataValue) {
        // Render the extracted data value using KaTeX
        mathTextRenderContainer.innerHTML = katex.renderToString(dataValue);
        console.log(mathTextRenderContainer);
    } else {
        console.error('No data-value attribute found');
    }
})();