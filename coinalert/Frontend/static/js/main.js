document.addEventListener('DOMContentLoaded', () => {
    const alertForm = document.getElementById('alert-form');
    const stopAlert = document.getElementById('stop-alert');

    alertForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const email = alertForm.elements.email.value;
        const coin = alertForm.elements.coin.value;
        const interval = alertForm.elements.interval.value;

        const response = await fetch('/api/alerts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, coin, interval }),
        });

        const data = await response.json();
        if (data.status === 'success') {
            alert('Alert set!');
        } else {
            alert('Failed to set alert.');
        }
    });

    stopAlert.addEventListener('click', async () => {
        const email = alertForm.elements.email.value;
        const coin = alertForm.elements.coin.value;

        const response = await fetch('/api/alerts', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, coin }),
        });

        const data = await response.json();
        if (data.status === 'success') {
            alert('Alert stopped!');
        } else {
            alert('Failed to stop alert.');
        }
    });
});
