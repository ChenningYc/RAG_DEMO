const form = document.querySelector("#question-form");
const questionInput = document.querySelector("#question");
const answerBox = document.querySelector("#answer");
const sourcesBox = document.querySelector("#sources");
const chunkCount = document.querySelector("#chunk-count");
const askButton = form.querySelector("button");

async function askQuestion(question) {
  askButton.disabled = true;
  answerBox.textContent = "Searching the knowledge base...";
  sourcesBox.innerHTML = '<p class="empty-state">Loading sources...</p>';
  chunkCount.textContent = "";

  try {
    const response = await fetch("/api/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Request failed");
    }

    answerBox.textContent = data.answer;
    chunkCount.textContent = `${data.chunk_count} chunks indexed`;
    renderSources(data.sources);
  } catch (error) {
    answerBox.textContent = `Error: ${error.message}`;
    sourcesBox.innerHTML = '<p class="empty-state">No sources available.</p>';
  } finally {
    askButton.disabled = false;
    questionInput.focus();
  }
}

function renderSources(sources) {
  if (!sources.length) {
    sourcesBox.innerHTML = '<p class="empty-state">No matching source found.</p>';
    return;
  }

  sourcesBox.innerHTML = sources
    .map(
      (source) => `
        <article class="source-card">
          <div class="source-meta">
            <span>${escapeHtml(source.source)}</span>
            <span>Score ${source.score}</span>
          </div>
          <p>${escapeHtml(source.text)}</p>
        </article>
      `
    )
    .join("");
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const question = questionInput.value.trim();

  if (!question) {
    questionInput.focus();
    return;
  }

  askQuestion(question);
});

document.querySelectorAll("[data-question]").forEach((button) => {
  button.addEventListener("click", () => {
    const question = button.dataset.question;
    questionInput.value = question;
    askQuestion(question);
  });
});
