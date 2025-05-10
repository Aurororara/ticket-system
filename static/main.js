fetch('/api/tickets')
  .then(res => res.json())
  .then(data => {
    const list = document.getElementById('ticket-list');
    list.innerHTML = '';

    data.tickets.forEach(ticket => {
      const item = document.createElement('div');
      item.innerHTML = `
        <h3>${ticket.title}</h3>
        <p>剩餘票數：${ticket.stock}</p>
        <button onclick="buy(${ticket.id})">搶票</button>
        <hr>
      `;
      list.appendChild(item);
    });
  });

function buy(ticketId) {
  fetch('/api/buy', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ticket_id: ticketId})
  })
  .then(res => res.json())
  .then(data => {
    alert(data.message);
    location.reload(); // 重新載入票數
  })
  .catch(() => alert("搶票失敗"));
}
