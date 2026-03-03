async function loadData() {

    // GMV
    const gmvRes = await fetch('/metrics/gmv?days=7');
    const gmvData = await gmvRes.json();

    document.getElementById('gmv').innerText =
        "GMV: " + gmvData.gmv;


    // Trend
    const trendRes = await fetch('/metrics/trend?days=7');
    const trendData = await trendRes.json();

    const ctx = document.getElementById('trendChart').getContext('2d');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: trendData.dates,
            datasets: [{
                label: 'GMV',
                data: trendData.values
            }]
        }
    });


    // Top Users
    const topRes = await fetch('/metrics/top-users?limit=5');
    const topData = await topRes.json();

    const list = document.getElementById('topUsers');
    list.innerHTML = "";

    topData.users.forEach(u => {
        const li = document.createElement('li');
        li.innerText = "User " + u.user_id + " - " + u.gmv;
        list.appendChild(li);
    });
}

loadData();