const pdfjsLib = window['pdfjs-dist/build/pdf'];

const pdfContainer = document.querySelector('.pdf-container');
const boxContent = document.getElementById('box-content');
let canvas = document.getElementById('pdf-canvas');
let rectCanvas = document.getElementById('rect-canvas');
let tempCanvas = document.getElementById('temp-canvas');
const pdfUrl = 'test.pdf'; // Replace with the actual path to your PDF file

let pdfDoc = null;
let pageNum = 1;
let scale = 1.3;


let boxesData = [];
let pageWidths = [];

// 使用fetch获取JSON文件
fetch('text.json')
  .then(response => response.json())
  .then(jsonData => {
    try {
      // 使用你之前提供的代码来解析数据
      for (const key in jsonData) {
        if (jsonData.hasOwnProperty(key)) {
          const entry = jsonData[key];
          for (let i = 0; i < entry.bbox.length; i++) {
            const bbox = entry.bbox[i];
            const [left, top, width, height] = bbox;
            boxesData.push({
              left: left / 2.08 * scale,
              top: top / 2.08 * scale,
              width: width / 2.08 * scale,
              height: height / 2.08 * scale,
              page: entry.pageNum,
              content: entry.text[i],
            });
          }
        }
      }

      return loadPDF(pdfUrl);
    } catch (parseError) {
      console.error('Error parsing JSON:', parseError);
    }
  })
.then(() => {
  // read every pagewidth from pdf
  const promises = [];
  for (let i = 0; i < pdfDoc.numPages; i++) {
    promises.push(pdfDoc.getPage(i + 1).then(function(page) {
      const viewport = page.getViewport(scale);
      pageWidths.push(viewport.viewBox[2]);
    }));
  }
  return Promise.all(promises);
})
.then(() => {
  boxesData = boxesData.sort((a, b) => {
      // Sort by page number
      if (a.page !== b.page) {
        return a.page - b.page;
      }
      const pageWidth = pageWidths[a.page - 1];
      
      // Sort by column (left position)
      // console.log(pageWidths)
      // console.log(pageWidths[a.page - 1])
      const aColumn = a.left < pageWidth / 3 ? 'left' : 'right';
      const bColumn = b.left < pageWidth / 3 ? 'left' : 'right';
    
      if (aColumn !== bColumn) {
        return aColumn === 'left' ? -1 : 1;
      }
    
      // Sort by vertical position within the same column
      return a.top - b.top;
    }) 
  })
  .then(() => {
    console.log(boxesData);
    initPDFViewer();
  })
  .catch(error => {
    console.error('Error fetching the file:', error);
  });


function clearCanvasAndListeners(canvasElement) {
    const newCanvas = canvasElement.cloneNode(true); // Create a new canvas element with the same attributes
    canvasElement.parentNode.replaceChild(newCanvas, canvasElement); // Replace the old canvas with the new one
    return newCanvas;
}

function drawRect(currentRenderContext, box, color, lineWidth, fillColor = null) {
  currentRenderContext.canvasContext.beginPath();
  currentRenderContext.canvasContext.rect(box.left, box.top, box.width, box.height);
  currentRenderContext.canvasContext.lineWidth = lineWidth;
  currentRenderContext.canvasContext.strokeStyle = color;
  currentRenderContext.canvasContext.stroke();
  if (fillColor) {
    currentRenderContext.canvasContext.fillStyle = fillColor;
    currentRenderContext.canvasContext.fillRect(box.left, box.top, box.width, box.height);
  }
}

// Function to render a page
function renderPage(num, highlightBoxIndex = -1) {
  console.log("rendering page: ", num)

  pdfDoc.getPage(num).then(function(page) {
    const viewport = page.getViewport({ scale });
    canvas = clearCanvasAndListeners(canvas);
    tempCanvas = clearCanvasAndListeners(tempCanvas);
    rectCanvas = clearCanvasAndListeners(rectCanvas);
    canvas.height = viewport.height;
    canvas.width = viewport.width;
    rectCanvas.style.position = 'absolute';
    rectCanvas.style.left = canvas.offsetLeft + 'px';
    rectCanvas.style.top = canvas.offsetTop + 'px';
    rectCanvas.height = viewport.height;
    rectCanvas.width = viewport.width;
    tempCanvas.style.position = 'absolute';
    tempCanvas.style.left = canvas.offsetLeft + 'px';
    tempCanvas.style.top = canvas.offsetTop + 'px';
    tempCanvas.height = viewport.height;
    tempCanvas.width = viewport.width;
  
    const renderContext = {
      canvasContext: canvas.getContext('2d'),
      viewport: viewport,
    };

    const rectRenderContext = {
      canvasContext: rectCanvas.getContext('2d'),
    };

    const tempRenderContext = {
      canvasContext: tempCanvas.getContext('2d'),
    };

    // Clear previous boxes
    renderContext.canvasContext.clearRect(0, 0, canvas.width, canvas.height);
    tempRenderContext.canvasContext.clearRect(0, 0, tempCanvas.width, tempCanvas.height);
    rectRenderContext.canvasContext.clearRect(0, 0, rectCanvas.width, rectCanvas.height);

    // Render the page
    page.render(renderContext).promise.then(function() {
      // Draw boxes on the canvas
      if (boxesData) {
        boxesData.forEach((box, index) => {
          if (box.page == num) {
            drawRect(rectRenderContext, box, '#3498db', 2);

            rectCanvas.addEventListener('mousemove', function(event) {
              const mouseX = event.clientX - rectCanvas.getBoundingClientRect().left;
              const mouseY = event.clientY - rectCanvas.getBoundingClientRect().top;
            
              if (
                mouseX >= box.left &&
                mouseX <= box.left + box.width &&
                mouseY >= box.top &&
                mouseY <= box.top + box.height
              ) {
                // Apply the hover style
                drawRect(rectRenderContext, box, '#e74c3c', 2);
              } else {
                // Revert to the original style
                drawRect(rectRenderContext, box, '#3498db', 2);
              }
            });

            rectCanvas.addEventListener('click', function(event) {
              // Check if the click is inside the highlighted box
              const clickX = event.clientX - rectCanvas.getBoundingClientRect().left;
              const clickY = event.clientY - rectCanvas.getBoundingClientRect().top;

              if (
                clickX >= box.left &&
                clickX <= box.left + box.width &&
                clickY >= box.top &&
                clickY <= box.top + box.height
              ) {
                // Perform the desired action, for example, navigate to another page
                const rightSideBox = document.querySelector(`.box[data-box-id="${index}"]`);
  
                // 滚动到右侧框的位置
                if (rightSideBox) {
                  rightSideBox.scrollIntoView({ behavior: 'smooth' });

                  rightSideBox.style.border = '2px solid #e74c3c';
                  rightSideBox.style.backgroundColor = 'rgba(255, 255, 0, 0.5)';

                  // 在一秒后再次恢复原样
                  setTimeout(function() {
                    rightSideBox.style.border = '2px solid #3498db';  // 恢复原始边框颜色
                    rightSideBox.style.backgroundColor = '';  // 移除背景颜色
                  }, 600);
                }
                // console.log(box.left, box.top, box.width, box.height, box.page, box.content);
              }
            });

            // Highlight the specified box
            if (index === highlightBoxIndex) {
              // Draw a highlighted box
              drawRect(tempRenderContext, box, '#e74c3c', 2, 'rgba(255, 255, 0, 0.5)');
              
              // Restore the canvas state
              setTimeout(function() {
                // Revert to the original style
                tempRenderContext.canvasContext.clearRect(0, 0, tempCanvas.width, tempCanvas.height);
              }, 500);
            }
          }
        });
      }

      // Update the content based on the page number
      updateContent(num);
    });
  });
}

// Function to load PDF
function loadPDF(url) {
  return pdfjsLib.getDocument(url).promise
    .then(function(pdfDoc_) {
      pdfDoc = pdfDoc_;
      renderPage(pageNum);
    });
}

// Function to update the content in the right panel based on the selected box
function updateContent(pageNum) {
  // Replace this with your logic to fetch content based on the pageNum from the backend
  const content = `Content for Page ${pageNum}`;
  boxContent.innerHTML = content;
}

// Function to handle box click events
function handleBoxClick(boxIndex) {
  pdfContainer.scrollTop = boxesData[boxIndex].top; // Scroll to the top of the box coordinates
  pageNum = boxesData[boxIndex].page; // Change to the appropriate page number
  renderPage(pageNum, boxIndex);
}

// Function to initialize the PDF viewer
function initPDFViewer() {
  for (let i = 0; i < boxesData.length; i++) {
    const box = document.createElement('div');
    box.className = 'box';
    // box.textContent = `Box ${i + 1} on Page ${boxesData[i].page} `;
    box.textContent = `Box ${i + 1} on Page ${boxesData[i].page} (${boxesData[i].left}, ${boxesData[i].top}, ${boxesData[i].width}, ${boxesData[i].height})\n${boxesData[i].content}`;
    box.setAttribute('data-box-id', i);

    box.addEventListener('click', () => handleBoxClick(i));
    document.querySelector('.content-container').appendChild(box);
  }

}

// Initialize the PDF viewer

