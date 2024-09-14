document.getElementById('saveButton').addEventListener('click', async () => {
    const dataInput = document.getElementById('dataInput').value;

    if (dataInput) {
        // POSTリクエストでデータを送信
        const response = await fetch('/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data: dataInput }),
        });

        if (response.ok) {
            // データ保存後にリストを更新
            document.getElementById('dataInput').value = '';
            fetchRecords();
        } else {
            alert('Failed to save data');
        }
    }
});

// サーバーからデータを取得してリストに表示
async function fetchRecords() {
    const response = await fetch('/records');
    const records = await response.json();

    const recordsList = document.getElementById('recordsList');
    recordsList.innerHTML = '';

    records.forEach(record => {
        const li = document.createElement('li');
        li.textContent = record.data;
        recordsList.appendChild(li);
    });
}

// ページが読み込まれたときにリストを表示
window.onload = fetchRecords;
