const state = {
  profile: null,
  projects: [],
};

const selectors = {
  projectGrid: document.querySelector("#project-grid"),
  commandOutput: document.querySelector("#command-output"),
  commandForm: document.querySelector("#command-form"),
  commandInput: document.querySelector("#command-input"),
  quickButtons: document.querySelector("#quick-buttons"),
};

async function fetchJson(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json();
}

function setText(id, value) {
  const element = document.querySelector(id);
  if (element && value) {
    element.textContent = value;
  }
}

function renderProfile(profile) {
  setText("#profile-name", profile.name);
  setText("#profile-role", profile.role_line);
  setText("#profile-intro", profile.intro);

  const emailLink = document.querySelector("#email-link");
  const githubLink = document.querySelector("#github-link");
  const linkedinLink = document.querySelector("#linkedin-link");

  if (emailLink && profile.email && isPlaceholderLink(emailLink)) {
    emailLink.textContent = profile.email;
    emailLink.href = `mailto:${profile.email}`;
  }
  if (githubLink && profile.github_url && isPlaceholderLink(githubLink)) {
    githubLink.href = profile.github_url;
  }
  if (linkedinLink && profile.linkedin_url && isPlaceholderLink(linkedinLink)) {
    linkedinLink.href = profile.linkedin_url;
  }
}

function isPlaceholderLink(link) {
  const href = link.getAttribute("href") || "";
  return !href || href.includes("placeholder");
}

function renderProjects(projects) {
  if (!selectors.projectGrid) {
    return;
  }

  selectors.projectGrid.innerHTML = projects
    .map((project) => {
      const tags = project.tags
        .slice(0, 5)
        .map((tag) => `<span class="tag">${escapeHtml(tag)}</span>`)
        .join("");
      const techStack = listItems(project.tech_stack);
      const keyFeatures = listItems(project.key_features, 5);
      const securityFocus = listItems(project.security_focus, 5);
      return `
        <article class="project-card">
          <h3>${escapeHtml(project.title)}</h3>
          <p>${escapeHtml(project.summary)}</p>
          <div class="tag-row">${tags}</div>
          <span class="case-label">${escapeHtml(project.status)}</span>
          <div class="project-details">
            ${detailBlock("Tech stack", techStack)}
            ${detailBlock("Key features", keyFeatures)}
            ${detailBlock("Security focus", securityFocus)}
            ${noteBlock(project.note_label, project.note)}
          </div>
        </article>
      `;
    })
    .join("");
}

function listItems(items, limit) {
  if (!Array.isArray(items)) {
    return [];
  }
  return typeof limit === "number" ? items.slice(0, limit) : items;
}

function detailBlock(title, items) {
  if (!items.length) {
    return "";
  }

  return `
    <div class="project-detail">
      <h4>${escapeHtml(title)}</h4>
      <ul>
        ${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
      </ul>
    </div>
  `;
}

function noteBlock(label, note) {
  if (!note) {
    return "";
  }

  return `
    <div class="project-note">
      <h4>${escapeHtml(label || "Note")}</h4>
      <p>${escapeHtml(note)}</p>
    </div>
  `;
}

function showCommandOutput(command, output, status = "ok") {
  if (!selectors.commandOutput) {
    return;
  }

  selectors.commandOutput.textContent = `> ${command}: ${output}`;
  selectors.commandOutput.dataset.status = status;
}

async function runCommand(command) {
  const cleanCommand = command.trim();
  if (!cleanCommand) {
    return;
  }

  if (cleanCommand.toLowerCase() === "clear") {
    showCommandOutput("clear", "Try help, projects, skills, or status.");
    if (selectors.commandInput) {
      selectors.commandInput.value = "";
    }
    return;
  }

  try {
    const result = await fetchJson("/api/command", {
      method: "POST",
      body: JSON.stringify({ command: cleanCommand }),
    });
    showCommandOutput(result.command || cleanCommand, result.output, result.status);
  } catch (error) {
    showCommandOutput(cleanCommand, "Command service is unavailable. Please try again later.", "error");
  } finally {
    if (selectors.commandInput) {
      selectors.commandInput.value = "";
    }
  }
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function bindCommandPanel() {
  if (!selectors.commandForm || !selectors.quickButtons || !selectors.commandInput || !selectors.commandOutput) {
    return;
  }

  selectors.commandForm.addEventListener("submit", (event) => {
    event.preventDefault();
    runCommand(selectors.commandInput.value);
  });

  selectors.quickButtons.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-command]");
    if (button) {
      runCommand(button.dataset.command);
    }
  });
}

async function init() {
  bindCommandPanel();

  try {
    const [profile, projects] = await Promise.all([
      fetchJson("/api/profile"),
      fetchJson("/api/projects"),
    ]);

    state.profile = profile;
    state.projects = projects;

    renderProfile(profile);
    renderProjects(projects);
  } catch (error) {
    if (selectors.projectGrid) {
      selectors.projectGrid.innerHTML = "<p>Portfolio data could not be loaded.</p>";
    }
  }
}

init();
