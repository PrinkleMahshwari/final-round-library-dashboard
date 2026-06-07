const API_BASE = window.location.origin;

let categoryChartInstance = null;
let statusChartInstance = null;
let topStudentsChartInstance = null;
let copiesChartInstance = null;

// This function changes page without refreshing the website
function showPage(pageId, button) {
  document.querySelectorAll(".page").forEach(page => {
    page.classList.remove("active");
  });

  document.getElementById(pageId).classList.add("active");

  document.querySelectorAll(".nav-btn").forEach(btn => {
    btn.classList.remove("active-btn");
  });

  button.classList.add("active-btn");
}

// This is common API function so we don't repeat fetch code again and again
async function fetchData(endpoint) {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: "GET",
      headers: {
        // This header is needed because localtunnel sometimes shows warning page
        "Bypass-Tunnel-Reminder": "true",
        "Content-Type": "application/json"
      }
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${endpoint}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error fetching data:", error);
    return null;
  }
}

// This function creates dynamic table from any API data
function renderTable(data, headId, bodyId) {
  const tableHead = document.getElementById(headId);
  const tableBody = document.getElementById(bodyId);

  tableHead.innerHTML = "";
  tableBody.innerHTML = "";

  if (!data || data.length === 0) {
    tableBody.innerHTML = "<tr><td colspan='100'>No data found</td></tr>";
    return;
  }

  const columns = Object.keys(data[0]);

  tableHead.innerHTML = `
    <tr>
      ${columns.map(col => `<th>${formatHeading(col)}</th>`).join("")}
    </tr>
  `;

  tableBody.innerHTML = data.map(row => `
    <tr>
      ${columns.map(col => `<td>${formatCellValue(col, row[col])}</td>`).join("")}
    </tr>
  `).join("");
}

// This makes database column names readable for frontend
function formatHeading(text) {
  return text
    .replaceAll("_", " ")
    .replace(/\b\w/g, char => char.toUpperCase());
}

// This function formats empty values and status badges
function formatCellValue(column, value) {
  if (value === null || value === undefined || value === "") {
    return "-";
  }

  if (column === "status") {
    const status = String(value).toUpperCase();

    if (status === "RETURNED") {
      return `<span class="status-badge status-returned">RETURNED</span>`;
    }

    if (status === "LATE") {
      return `<span class="status-badge status-late">LATE</span>`;
    }

    return `<span class="status-badge status-issued">ISSUED</span>`;
  }

  return value;
}

// This loads all dashboard cards and graphs
async function loadDashboard() {
  const stats = await fetchData("/api/dashboard/stats");
  const booksByCategory = await fetchData("/api/reports/books-by-category") || [];
  const issueStatus = await fetchData("/api/reports/issue-status") || [];
  const topStudents = await fetchData("/api/reports/top-students") || [];
  const availableCopies = await fetchData("/api/reports/available-copies") || [];

  if (stats) {
    document.getElementById("totalStudents").innerText = stats.total_students ?? 0;
    document.getElementById("totalCategories").innerText = stats.total_categories ?? 0;
    document.getElementById("totalBooks").innerText = stats.total_books ?? 0;
  }

  // Important fix: database has uppercase status like ISSUED, RETURNED, LATE
  const issued = issueStatus.find(item => item.status?.toUpperCase() === "ISSUED");
  const returned = issueStatus.find(item => item.status?.toUpperCase() === "RETURNED");
  const late = issueStatus.find(item => item.status?.toUpperCase() === "LATE");

  document.getElementById("issuedBooks").innerText = issued?.total ?? 0;
  document.getElementById("returnedBooks").innerText = returned?.total ?? 0;
  document.getElementById("lateBooks").innerText = late?.total ?? 0;

  document.getElementById("totalIssues").innerText =
    issueStatus.reduce((sum, item) => sum + Number(item.total), 0);

  document.getElementById("topStudent").innerText =
    topStudents.length > 0 ? topStudents[0].student_name : "-";

  renderCategoryChart(booksByCategory);
  renderStatusChart(issueStatus);
  renderTopStudentsChart(topStudents);
  renderCopiesChart(availableCopies);
}

// Graph 1: Books by category
function renderCategoryChart(data) {
  if (categoryChartInstance) {
    categoryChartInstance.destroy();
  }

  categoryChartInstance = new Chart(document.getElementById("categoryChart"), {
    type: "bar",
    data: {
      labels: data.map(item => item.category_name),
      datasets: [{
        label: "Total Books",
        data: data.map(item => item.total_books),
        backgroundColor: "#bfdbfe",
        borderColor: "#60a5fa",
        borderWidth: 1,
        borderRadius: 8
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

// Graph 2: Issue status
function renderStatusChart(data) {
  if (statusChartInstance) {
    statusChartInstance.destroy();
  }

  statusChartInstance = new Chart(document.getElementById("statusChart"), {
    type: "doughnut",
    data: {
      labels: data.map(item => item.status),
      datasets: [{
        label: "Issue Status",
        data: data.map(item => item.total),
        backgroundColor: ["#fde68a", "#bbf7d0", "#fecaca", "#ddd6fe"],
        borderColor: "#ffffff",
        borderWidth: 3
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "bottom"
        }
      }
    }
  });
}

// Graph 3: Top students report
function renderTopStudentsChart(data) {
  if (topStudentsChartInstance) {
    topStudentsChartInstance.destroy();
  }

  topStudentsChartInstance = new Chart(document.getElementById("topStudentsChart"), {
    type: "bar",
    data: {
      labels: data.map(item => item.student_name),
      datasets: [{
        label: "Total Issued",
        data: data.map(item => item.total_issued),
        backgroundColor: "#ddd6fe",
        borderColor: "#a78bfa",
        borderWidth: 1,
        borderRadius: 8
      }]
    },
    options: {
      responsive: true,
      indexAxis: "y",
      scales: {
        x: {
          beginAtZero: true
        }
      }
    }
  });
}

// Graph 4: Available copies report
function renderCopiesChart(data) {
  if (copiesChartInstance) {
    copiesChartInstance.destroy();
  }

  copiesChartInstance = new Chart(document.getElementById("copiesChart"), {
    type: "bar",
    data: {
      labels: data.map(item => item.title),
      datasets: [
        {
          label: "Available Copies",
          data: data.map(item => item.available_copies),
          backgroundColor: "#bbf7d0"
        },
        {
          label: "Issued Copies",
          data: data.map(item => item.issued_copies),
          backgroundColor: "#fecaca"
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

// This loads all tables in different sections
async function loadTables() {
  const books = await fetchData("/api/books") || [];
  const issues = await fetchData("/api/issues") || [];
  const categories = await fetchData("/api/reports/books-by-category") || [];
  const issueStatus = await fetchData("/api/reports/issue-status") || [];
  const topStudents = await fetchData("/api/reports/top-students") || [];
  const availableCopies = await fetchData("/api/reports/available-copies") || [];
  const dashboardDetails = await fetchData("/api/dashboard/details-table") || [];

  renderTable(books, "booksHead", "booksBody");
  renderTable(issues, "issuesHead", "issuesBody");
  renderTable(categories, "categoriesHead", "categoriesBody");
  renderTable(issueStatus, "statusHead", "statusBody");
  renderTable(topStudents, "topStudentsHead", "topStudentsBody");
  renderTable(availableCopies, "copiesHead", "copiesBody");
  renderTable(dashboardDetails, "dashboardHead", "dashboardBody");
}

// Website starts from here
loadDashboard();
loadTables();