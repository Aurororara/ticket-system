document.getElementById('session-form').addEventListener('submit', function (e) {
    e.preventDefault();
  
    const selectedId = document.getElementById('session').value;
  
    if (!selectedId) {
      alert('請選擇場次！');
      return;
    }
  
    // 存入 localStorage（或你也可以用 hidden input POST 給後端）
    localStorage.setItem('selectedSessionId', selectedId);
  
    // 跳轉到下一頁
    window.location.href = "/select_ticket";
  });

  