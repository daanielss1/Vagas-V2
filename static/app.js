async function loadJobs(hours = 24) {
    const q = document.getElementById("search").value;

    const res = await fetch(`/api/jobs?q=${q}&hours=${hours}`);
    const data = await res.json();

    const el = document.getElementById("jobs");
    el.innerHTML = "";

    data.forEach(job => {
        el.innerHTML += `
            <div class="card">
                <b>${job.title}</b><br>
                ${job.company}<br>
                <small>${job.posted_at}</small><br>
                <button onclick='applyJob(${JSON.stringify(job)})'>
                    Já apliquei
                </button>
            </div>
        `;
    });

    loadApplied();
}

async function applyJob(job) {
    await fetch("/api/apply", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(job)
    });

    loadJobs(24);
}

async function loadApplied() {
    const res = await fetch("/api/applied");
    const data = await res.json();

    const el = document.getElementById("applied");
    el.innerHTML = "";

    data.forEach(job => {
        el.innerHTML += `
            <div class="card applied">
                <b>${job.title}</b><br>
                ${job.company}<br>
                <small>${job.applied_at}</small>
            </div>
        `;
    });
}

loadJobs(24);